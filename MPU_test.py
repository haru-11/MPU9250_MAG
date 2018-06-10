import mpu9250_1
import time
import threading
import numpy as np
import math

mpu = mpu9250_1.SL_MPU9250(0x68,1)


class Put9axis():

	def __init__(self):
		print("Hello")
		self.accx = 0
		self.accy = 0
		self.accz = 0
	def rcv9axis(self, medianx, mediany, medianz):
		self.accx = medianx
		self.accy = mediany
		self.accz = medianz
		return

	def put9axis(self):
		rawX = self.accx
		rawY = self.accy
		rawZ = self.accz
		return rawX, rawY, rawZ

Acc = Put9axis()

def get9axis():

	mpu.resetRegister()
	mpu.powerWakeUp()
	mpu.setAccelRange(8,True)
	mpu.setGyroRange(1000,True)
	mpu.setMagRegister('1000Hz','16bit')
	# sensor.selfTestMag()
	i = 0

	while True:

		now = time.time()
		acc = mpu.getAccel()
		gyr = mpu.getGyro()
		mag = mpu.getMag()

		data_accx = acc[0]
		data_accy = acc[1]
		data_accz = acc[2]
		i += 1
		if i == 20:
			medianx = np.median(data_accx)
			mediany = np.median(data_accy)
			medianz = np.median(data_accz)
			i = 0
			Acc.rcv9axis(medianx, mediany, medianz)

		sleepTime       = 0.01 - (time.time() - now)
		if sleepTime < 0.0:
			continue
		time.sleep(sleepTime)

mputhread = threading.Thread(target=get9axis)
mputhread.demon = True
mputhread.start()

while True:
	acc = Acc.put9axis()

	print "%+8.7f" % acc[0] + " ",
	print "%+8.7f" % acc[1] + " ",
	print "%+8.7f" % acc[2]
	#print " |   ",
	#print "%+8.7f" % gyr[0] + " ",
	#print "%+8.7f" % gyr[1] + " ",
	#print "%+8.7f" % gyr[2] + " ",
	#print " |   ",
	#print "%+8.7f" % mag[0] + " ",
	#print "%+8.7f" % mag[1] + " ",
	#print "%+8.7f" % mag[2]
	x_angle = math.degrees( math.atan2( acc[0], math.sqrt(acc[1] ** 2 + acc[2] ** 2 )))
	y_angle = math.degrees( math.atan2( acc[1], math.sqrt(acc[0] ** 2 + acc[2] ** 2 )))
	print("X Angle:", x_angle, "Y Angle", y_angle)
	
	time.sleep(0.5)
