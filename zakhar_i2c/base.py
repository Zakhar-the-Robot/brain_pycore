import platform

if platform.system().lower().startswith('win'):
    # import windows specific modules
    from fake_rpi.smbus import SMBus
else:
    # import linux specific modules
    from smbus2 import SMBus

import logging
from threading import Lock
from time import sleep
from zakhar_log import *
bus = SMBus(1)  # indicates /dev/ic2-1
i2c_mutex = Lock()

# CONFIG_LOG_LEVEL = logging.DEBUG
CONFIG_LOG_LEVEL = logging.INFO

l = get_logger("I2C")
l.setLevel(CONFIG_LOG_LEVEL)

def i2c_read_byte(addr):
    global i2c_mutex
    with i2c_mutex:
        b = bus.read_byte(addr)
        l.debug('Read byte %s from %s' % (hex(b), hex(addr)))
        return b

def i2c_write_byte(addr, val):
    global i2c_mutex
    with i2c_mutex:
        bus.write_byte(addr, val)
        l.debug('Wrote byte %s to %s' % (hex(val),hex(addr)))

def i2c_write_byte_data(addr, reg, val):
    global i2c_mutex
    with i2c_mutex:
        bus.write_byte_data(addr, reg, val)
        l.debug('Wrote byte %s from %s:%s' % (hex(val), hex(addr), hex(reg)))

def i2c_read_byte_from(addr, reg):
    global i2c_mutex
    with i2c_mutex:
        bus.write_byte(addr, reg)
        b = bus.read_byte(addr)
        l.debug('Read byte %s from %s:%s' % (hex(b), hex(addr), hex(reg)))
        return b