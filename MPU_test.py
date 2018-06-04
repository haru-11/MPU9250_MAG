#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import smbus
import time
1channel = 2
address = 0x68
bus     = smbus.SMBus(channel)

#unsignedを、signedに変換(16ビット限定）
def u2s(unsigneddata):
    if unsigneddata & (0x01 << 15) : 
        return -1 * ((unsigneddata ^ 0xffff) + 1)
    return unsigneddata

# レジスタをリセットする
bus.write_i2c_block_data(address, 0x6B, [0x80])
time.sleep(0.1)     

# PWR_MGMT_1をクリア
bus.write_i2c_block_data(address, 0x6B, [0x00])
time.sleep(0.1)

# 加速度センサのレンジを±8gにする
bus.write_i2c_block_data(address, 0x1C, [0x08])

# 生データを取得する
while True:
    data    = bus.read_i2c_block_data(address, 0x3B ,6)
    rawX    = (8.0 / float(0x8000)) * u2s(data[0] << 8 | data[1])
    rawY    = (8.0 / float(0x8000)) * u2s(data[2] << 8 | data[3])
    rawZ    = (8.0 / float(0x8000)) * u2s(data[4] << 8 | data[5])
    print "%+8.7f" % rawX + "   ",
    print "%+8.7f" % rawY + "   ",
    print "%+8.7f" % rawZ
    time.sleep(1)
