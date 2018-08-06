#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import mpu9250_1
import time
import threading
import numpy as np
import math

mpu = mpu9250_1.SL_MPU9250(0x69,1)


class Put9axis:

	def __init__(self):
		print("Hello")
		self.accx = 0
		self.accy = 0
		self.accz = 0
                self.gyrx = 0
                self.gyry = 0
                self.gyrz = 0
                self.magx = 0
                self.magy = 0
                self.magz = 0
	def rcv3acc(self, medianx, mediany, medianz):
		self.accx = medianx
              	self.accy = mediany
               	self.accz = medianz
	def rcv6axis(self, g1, g2, g3, m1, m2, m3):
                self.gyrx = g1
                self.gyry = g2
                self.gyrz = g3
                self.magx = m1
                self.magy = m2
                self.magz = m3

	def put_acc(self):
		rawX = self.accx
		rawY = self.accy
		rawZ = self.accz
		return rawX, rawY, rawZ

	def put_gyr(self):
		gyrX = self.gyrx
		gyrY = self.gyry
		gyrZ = self.gyrz
		return gyrX, gyrY, gyrZ

	def put_mag(self):
		magX = self.magx
		magY = self.magy
		magZ = self.magz
		return magX, magY, magZ

Acc = Put9axis
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
		#Acc.rcv6axis(gyr[0], gyr[1], gyr[2], mag[0], mag[1], mag[2])
		data_accx = acc[0]
		data_accy = acc[1]
		data_accz = acc[2]
		i += 1
		if i == 20:
			medianx = np.median(data_accx)
			mediany = np.median(data_accy)
			medianz = np.median(data_accz)
			i = 0
			Acc.rcv3acc(medianx, mediany, medianz)
			sleepTime = 0.01 - (time.time() - now)
		if sleepTime < 0.0:
			continue
		time.sleep(sleepTime)

mputhread = threading.Thread(target=get9axis)
mputhread.demon = True
mputhread.start()

#while True:
#	acc = Acc.put_acc()
#	gyr = Acc.put_gyr()
#	mag = Acc.put_mag()
#
#	print "%+8.7f" % acc[0] + " ",
#	print "%+8.7f" % acc[1] + " ",
#	print "%+8.7f" % acc[2] + " ",
#	print "%+8.7f" % gyr[0] + " ",
#	print "%+8.7f" % gyr[1] + " ",
#	print "%+8.7f" % gyr[2] + " ",
#	print "%+8.7f" % mag[0] + " ",
#	print "%+8.7f" % mag[1] + " ",
#	print "%+8.7f" % mag[2]
#	x_angle = math.degrees( math.atan2( acc[0], math.sqrt(acc[1] ** 2 + acc[2] ** 2 )))
#	y_angle = math.degrees( math.atan2( acc[1], math.sqrt(acc[0] ** 2 + acc[2] ** 2 )))
#	print("X Angle:", x_angle, "Y Angle", y_angle)
#
#	time.sleep(1.0)

