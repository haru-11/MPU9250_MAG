import mpu9250_1

mpu = mpu9250_1()

while True:
    now     = mpu.time.time()
    acc     = mpu.sensor.getAccel()
    gyr     = mpu.sensor.getGyro()
    mag     = mpu.sensor.getMag()
    print "%+8.7f" % acc[0] + " ",
    print "%+8.7f" % acc[1] + " ",
    print "%+8.7f" % acc[2] + " ",
    print " |   ",
    print "%+8.7f" % gyr[0] + " ",
    print "%+8.7f" % gyr[1] + " ",
    print "%+8.7f" % gyr[2] + " ",
    print " |   ",
    print "%+8.7f" % mag[0] + " ",
    print "%+8.7f" % mag[1] + " ",
    print "%+8.7f" % mag[2]
    sleepTime       = 0.1 - (time.time() - now)
    if sleepTime < 0.0:
        continue
    time.sleep(sleepTime)
