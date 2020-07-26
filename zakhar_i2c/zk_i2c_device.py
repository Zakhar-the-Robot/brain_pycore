import threading
import time
import rospy
import zakhar_log
import zakhar_common as com
import logging
from zakhar_msgs import srv, msg

from .node import NAME_SRV
import time

REG_CMD = 0
REG_MODE = 1

CMD_NONE = 0xFF
CMD_DONE = 0x00
CMD_STOP = 0xA0

CONFIG_MAX_RETRY = 16
CONFIG_DEFAULT_LOG_LEVEL = logging.INFO


class ZkI2cDevice(object):
    def __init__(self, dev_name, address, poll_dict={},
                log_level=CONFIG_DEFAULT_LOG_LEVEL):
        """
        [summary]

        Parameters
        ----------
        dev_name : str
        address : int
        req_poll_list : dict
            {
                (register) : (poll freq, hz),
                (register) : (poll freq, hz),
                ...
            }
            e.g.:
            {
                0x1: 10,
                0x2: 1
            }
        log_level : int, optional
        """

        self._name = dev_name
        self._address = address
        self.subscriber = None
        self.client = None
        self.publisher = None
        self._started = False
        self.l = zakhar_log.get_logger(self._name)
        self.l.setLevel(log_level)
        self.poll_dict = poll_dict
        self.poll_threads = []


    def set_log_level(self, level):
        self.l.setLevel(level)


    def _srv_handle(req):
        self.l.debug("handle")
        return device_serviceResponse(r)

        if (req.command == "w"):
            self.write(req.address, req.argument)
            return (0xFF, 'done')
        elif (req.command == "r"):
            r = i2c_read_byte_from(req.addr, req.reg)
            return device_serviceResponse(r)
        else:
            l.error("Wrong I2C cmd. Variants: w, r")
            return 0x0EFF


    def subscriber_callback(self, data):
        if((data.target==self._name) or (data.target=='all')):
            self.l.info(
                "Got [ %s -> %s ]: `%s`, %x, %x, %x, %x, `%s`" %
                    (   rospy.get_caller_id(),
                        data.target, data.msg, data.argumentA, data.argumentB,
                        data.argumentC, data.argumentD, data.argumentString )
                )
            if (data.argumentString == 'w') or (data.argumentString == 'write'):
                self.write(reg=data.argumentA, val=data.argumentB)
            if (data.argumentString == 'r') or (data.argumentString == 'read'):
                self.read(reg=data.argumentA)

    def publish(self, dtype="", valA=0, valB=0, valC=0, valD=0, valString="", msg_note=""):
        to_send = msg.SensorData()
        to_send.type = dtype
        to_send.valA = valA
        to_send.valB = valB
        to_send.valC = valC
        to_send.valD = valD
        to_send.valString = valString
        to_send.message = msg_note
        self.publisher.publish(to_send)
        # self.l.info("Send with type of %s: `%s`, %x, %x, %x, `%s`, `%s`" %
        #             (dtype, valA, valB, valC, valD, valString, msg_note))

    def poll_process(self, register, freq):
        while(1):
            try:
                d = self.read(reg=register)
            except Exception as e:
                d = None
            if d is None:
                d = -1
                continue
            self.publish(   dtype=self._name,
                            valA=register,
                            valB=d,
                            valC=0,
                            valD=0,
                            valString="",
                            msg_note="A:reg, B:val")
            # self.l.info("Polled (%dHz) register 0x%x, result: 0x%x" % (freq, register, d))
            time.sleep(1/freq)


    def _start_poll(self):
        for poll in self.poll_dict:
            t = threading.Thread(target=self.poll_process,args=(poll,self.poll_dict[poll]))
            t.daemon = True
            t.start()
            self.poll_threads.append(t)



    def _start(self):
        self.l.info("Node \'%s\' is starting..." % self._name)
        rospy.init_node(self._name, anonymous=False)
        ###
        self.l.info("  Waiting for the service %s", NAME_SRV)
        rospy.wait_for_service(NAME_SRV)
        ###
        self.client = com.get.client(name=NAME_SRV,
                                     service=srv.I2c,
                                     logger=self.l)
        self.subscriber = com.get.subscriber(topic_name=com.topics.DeviceCmd,
                                             data_class=msg.DeviceCmd,
                                             callback=self.subscriber_callback,
                                             logger=self.l)
        self.publisher = com.get.publisher(topic_name=com.topics.SensorData,
                                           data_class=msg.SensorData,
                                           logger=self.l)
        self._start_poll()
        ###
        self.l.info("Node \'%s\' is ready..." % self._name)


    def _start_new_proc(self):
        self.l.info("Starting...")
        from multiprocessing import Process
        p = Process(target=self._start)
        p.start()
        self.l.info("Done")


    def start(self, new_process=False):
        if new_process:
            self._start_new_proc()
        else:
            self._start()


    def write(self, reg, val):
        self.l.debug("write(%x, %x)" % (reg, val))
        if not self.client:
            raise rospy.ServiceException
        try:
            resp = self.client("w", self._address, reg, val)
            return resp.reg_value
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)


    def read(self, reg):
        self.l.debug("read(%x)" % (reg))
        if not self.client:
            raise rospy.ServiceException
        try:
            resp = self.client("r", self._address, reg, 0)
            return resp.reg_value
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)


    def mode(self):
        s = self.read_byte_from(REG_MODE)
        return s


    def cmd(self, val):
         self.l.debug("Send a command :%s" % hex(val))
         self.write(REG_CMD,val)


    def cmd_stop(self):
        self.cmd(0xA0)
