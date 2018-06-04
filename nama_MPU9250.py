import smbus
import time
channel = 1
address = 0x68
bus     = smbus.SMBus(channel)

bus.write_i2c_block_data(address, 0x6B, [0x80])
time.sleep(0.1)     

bus.write_i2c_block_data(address, 0x6B, [0x00])
time.sleep(0.1)

while True:
    data    = bus.read_i2c_block_data(address, 0x3B ,6)
    rawX    = data[0] << 8 | data[1]
    rawY    = data[2] << 8 | data[3]
    rawZ    = data[4] << 8 | data[5]
    print "%x" % rawX + "   ",
    print "%f" % rawY + "   ",
    print "%f" % rawZ
    time.sleep(1)
