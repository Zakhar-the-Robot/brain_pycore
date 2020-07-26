# from zk_mind.zk_ros import *
import rospy
import zakhar_common as com
import zakhar_log as log
from zakhar_msgs import msg, srv
from time import sleep
from . import base

NAME_SRV = "i2c"


class I2cNode:
    def __init__(self, name):
        self.name = name  # TODO make a hardcoded name
        self.l = log.get_logger(name)
        self.server = None

    def handle(self, req):
        self.l.debug("handle")
        try:
            if (req.node_cmd == "w"):
                base.i2c_write_byte_data(req.addr, req.reg, req.reg_value)
                return srv.I2cResponse(0x0AFF)
            elif (req.node_cmd == "r"):
                read_byte = base.i2c_read_byte_from(req.addr, req.reg)
                return srv.I2cResponse(read_byte)
            else:
                self.l.error("Wrong I2C cmd. Variants: w, r")
                return srv.I2cResponse(0x0EFF)
        except IOError:
            if (req.node_cmd == "w"):
                self.l.error("Can't write")
            if (req.node_cmd == "r"):
                self.l.error("Can't read")
            sleep(.1)

    def _start_server(self):
        rospy.init_node(self.name, anonymous=False)
        self.server = com.get.server(name=self.name,
                                     service=srv.I2c,
                                     handle=self.handle,
                                     logger=self.l)

    def _start_new_proc(self):
        self.l.info("Starting...")
        from multiprocessing import Process
        p = Process(target=self._start_server)
        p.start()
        self.l.info("Done")

    def start(self, new_process=False):
        if new_process:
            self._start_new_proc()
        else:
            self._start_server()
