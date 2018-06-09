#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import smbus
import time
channel = 1
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
bus.write_i2c_block_data(address, 0x1C, [0x10])

# 較正値を算出する
print "Accel calibration start"
_sum    = [0,0,0]

# 実データのサンプルを取る
for _i in range(1000):
    data    = bus.read_i2c_block_data(address, 0x3B ,6)
    _sum[0] += (8.0 / float(0x8000)) * u2s(data[0] << 8 | data[1])
    _sum[1] += (8.0 / float(0x8000)) * u2s(data[2] << 8 | data[3])
    _sum[2] += u2s(data[4] << 8 | data[5])/4096.0

# 平均値をオフセットにする
offsetAccelX    = -1.0 * _sum[0] / 1000
offsetAccelY    = -1.0 * _sum[1] / 1000
# Z軸は重力分を差し引く 本当に1.0かは怪しい
offsetAccelZ    = (-1.0 * _sum[2] / 1000)-1.0
print "%+8.7f" % offsetAccelX
print "%+8.7f" % offsetAccelY
print "%+8.7f" % offsetAccelZ
print "Accel calibration complete"
# 生データを取得する
while True:
    data    = bus.read_i2c_block_data(address, 0x3B ,6)
    rawX    = (8.0 / float(0x8000)) * u2s(data[0] << 8 | data[1]) + offsetAccelX
    rawY    = (8.0 / float(0x8000)) * u2s(data[2] << 8 | data[3]) + offsetAccelY
    rawZ    = (u2s(data[4] << 8 | data[5])/4096.0) + offsetAccelZ
    print "%+8.7f" % rawX + "   ",
    print "%+8.7f" % rawY + "   ",
    print "%+8.7f" % rawZ
    time.sleep(1)
