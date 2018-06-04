# -*- coding: utf-8 -*-

import smbus
import time
channel = 1
address = 0x68
bus     = smbus.SMBus(channel)

# レジスタをリセットする
bus.write_i2c_block_data(address, 0x6B, [0x80])
time.sleep(0.1)     

# PWR_MGMT_1をクリア
bus.write_i2c_block_data(address, 0x6B, [0x00])
time.sleep(0.1)

# 生データを取得する
while True:
    data    = bus.read_i2c_block_data(address, 0x65 ,2)
    raw     = data[0] << 8 | data[1]
    # 温度の算出式はデータシートから下記の通り
    # ((TEMP_OUT – RoomTemp_Offset)/Temp_Sensitivity) + 21degC
    temp    = (raw / 333.87) + 21 
    print str(temp)
