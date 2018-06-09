import mpu9250_1
import time

mpu = mpu9250_1.SL_MPU9250(0x68,1)

mpu.resetRegister()
mpu.powerWakeUp()
mpu.setAccelRange(8,True)
mpu.setGyroRange(1000,True)
mpu.setMagRegister('1000Hz','16bit')
# sensor.selfTestMag()

while True:

	now = time.time()
	acc = mpu.getAccel()
	gyr = mpu.getGyro()
	mag = mpu.getMag()
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
	sleepTime       = 0.5 - (time.time() - now)
	if sleepTime < 0.0:
		continue
	time.sleep(sleepTime)
