#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import smbus
import time
channel = 1
address = 0x68
bus     = smbus.SMBus(channel)

def u2s(unsigneddata):
    if unsigneddata & (0x01 << 15) :
        return -1 * ((unsigneddata ^ 0xffff) + 1)
    return unsigneddata


bus.write_i2c_block_data(address, 0x6B, [0x80])
time.sleep(0.1)


bus.write_i2c_block_data(address, 0x6B, [0x00])
time.sleep(0.1)


while True:
    data    = bus.read_i2c_block_data(address, 0x3B ,6)
    rawX    = (2.0 / float(0x8000)) * u2s(data[0] << 8 | data[1])
    rawY    = (2.0 / float(0x8000)) * u2s(data[2] << 8 | data[3])
    rawZ    = (2.0 / float(0x8000)) * u2s(data[4] << 8 | data[5])
    print "%+8.7f" % rawX + "   ",
    print "%+8.7f" % rawY + "   ",
    print "%+8.7f" % rawZ
    time.sleep(1)
