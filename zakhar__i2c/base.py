import platform
from smbus2 import SMBus

import logging
from threading import Lock
from time import sleep
bus = SMBus(1)  # indicates /dev/ic2-1
i2c_mutex = Lock()

# CONFIG_LOG_LEVEL = logging.DEBUG
CONFIG_LOG_LEVEL = logging.INFO

def i2c_read_byte(addr):
    global i2c_mutex
    with i2c_mutex:
        b = bus.read_byte(addr)
        print('Read byte %s from %s' % (hex(b), hex(addr)))
        return b

def i2c_write_byte(addr, val):
    global i2c_mutex
    with i2c_mutex:
        bus.write_byte(addr, val)
        print('Wrote byte %s to %s' % (hex(val),hex(addr)))

def i2c_write_byte_data(addr, reg, val):
    global i2c_mutex
    with i2c_mutex:
        bus.write_byte_data(addr, reg, val)
        print('Wrote byte %s from %s:%s' % (hex(val), hex(addr), hex(reg)))

def i2c_read_byte_from(addr, reg):
    global i2c_mutex
    with i2c_mutex:
        bus.write_byte_data(addr, reg, 0xFF)
        b = bus.read_byte(addr)
        return b

def send_cmd(addr, cmd, arg=0x0):
    if arg:
        i2c_write_byte_data(addr, 0x1, arg)# write
    i2c_write_byte_data(addr, 0, cmd)# write
    while(i2c_read_byte_from(addr,0x0)):
        sleep(.1)
    sleep(.1)

def i2cdetect(bus_num):
    b = SMBus(bus_num)
    devs = []
    for a in range(0xff):
        try:
            b.read_byte(a)
            devs.append(hex(a))
        except IOError:
            pass
    return devs
