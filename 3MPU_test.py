# -*- coding: utf-8 -*-

import mpu9250_1
import time
import threading
import numpy as np
import math

mpu = mpu9250_1.SL_MPU9250(0x68,1)
deltat = 0.001  #秒単位のサンプリング周期 (1msで表示)
gyroMeasError = 3.14159265358979 * (5.0 / 180.0) # rad/s単位のジャイロの測定誤差(shown as 5 deg/s)
beta = math.sqrt(3.0 / 4.0) * gyroMeasError # ベータを計算する

mpu.resetRegister()
mpu.powerWakeUp()
mpu.setAccelRange(8,True)
mpu.setGyroRange(1000,True)
mpu.setMagRegister('1000Hz','16bit')

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

#mputhread = threading.Thread(target=get9axis)
#mputhread.demon = True
#mputhread.start()

SEq_1 = 1.0
SEq_2 = 0.0
SEq_3 = 0.0
SEq_4 = 0.0 # クオータニオンの初期値


def filterUpdate(w_x, w_y, w_z, a_x, a_y, a_z):
    SEq_1 = 1.0
    SEq_2 = 0.0
    SEq_3 = 0.0
    SEq_4 = 0.0 # クオータニオンの初期値

    #ローカルシステム変数

   # f_1, f_2, f_3 #objective関数の要素
   # J_11or24, J_12or23, J_13or22, J_14or21, J_32, J_33 # objective関数のヤコビアン
   # SEqHatDot_1, SEqHatDot_2, SEqHatDot_3, SEqHatDot_4 # ジャイロの誤差の推定方向
    #再計算を防ぐためのAxulirary変数
    halfSEq_1 = 0.5 * SEq_1
    halfSEq_2 = 0.5 * SEq_2
    halfSEq_3 = 0.5 * SEq_3
    halfSEq_4 = 0.5 * SEq_4
    twoSEq_1 = 2.0 * SEq_1
    twoSEq_2 = 2.0 * SEq_2
    twoSEq_3 = 2.0 * SEq_3
    #加速度の測定値の正規化
    norm = math.sqrt(a_x * a_x + a_y * a_y + a_z * a_z) #ベクトルの絶対値（ノルム）
    a_x /= norm
    a_y /= norm
    a_z /= norm
    #  objective関数とヤコビアンの計算
    f_1 = twoSEq_2 * SEq_4 - twoSEq_1 * SEq_3 - a_x
    f_2 = twoSEq_1 * SEq_2 + twoSEq_3 * SEq_4 - a_y
    f_3 = 1.0 - twoSEq_2 * SEq_2 - twoSEq_3 * SEq_3 - a_z
    J_11or24 = twoSEq_3  # J_11は行列の計算を否定
    J_12or23 = 2.0 * SEq_4
    J_13or22 = twoSEq_1; # J_12は行列を取り消す
    J_14or21 = twoSEq_2;
    J_32 = 2.0 * J_14or21 # 行列の乗算を無効
    J_33 = 2.0 * J_11or24 # 行列の乗算を無効
    #gradientの計算（行列乗算）
    SEqHatDot_1 = J_14or21 * f_2 - J_11or24 * f_1
    SEqHatDot_2 = J_12or23 * f_1 + J_13or22 * f_2 - J_32 * f_3
    SEqHatDot_3 = J_12or23 * f_2 - J_33 * f_3 - J_13or22 * f_1
    SEqHatDot_4 = J_14or21 * f_1 + J_11or24 * f_2
    #gradientの正規化
    norm = math.sqrt(SEqHatDot_1 * SEqHatDot_1 + SEqHatDot_2 * SEqHatDot_2 + SEqHatDot_3 * SEqHatDot_3 + SEqHatDot_4 * SEqHatDot_4)#
    SEqHatDot_1 /= norm
    SEqHatDot_2 /= norm
    SEqHatDot_3 /= norm
    SEqHatDot_4 /= norm
    #ジャイロから求めたquaternion　derrivativeを計算 ジャイロから求まるクオータニオン
    SEqDot_omega_1 = -halfSEq_2 * w_x - halfSEq_3 * w_y - halfSEq_4 * w_z
    SEqDot_omega_2 = halfSEq_1 * w_x + halfSEq_3 * w_z - halfSEq_4 * w_y
    SEqDot_omega_3 = halfSEq_1 * w_y - halfSEq_2 * w_z + halfSEq_4 * w_x
    SEqDot_omega_4 = halfSEq_1 * w_z + halfSEq_2 * w_y - halfSEq_3 * w_x
    #ジャイロで測定されたクオータニオンの乗数を計算
    SEq_1 += (SEqDot_omega_1 - (beta * SEqHatDot_1)) * deltat;
    SEq_2 += (SEqDot_omega_2 - (beta * SEqHatDot_2)) * deltat;
    SEq_3 += (SEqDot_omega_3 - (beta * SEqHatDot_3)) * deltat;
    SEq_4 += (SEqDot_omega_4 - (beta * SEqHatDot_4)) * deltat;
    #クオータニオンの正規化
    norm = math.sqrt(SEq_1 * SEq_1 + SEq_2 * SEq_2 + SEq_3 * SEq_3 + SEq_4 * SEq_4);
    SEq_1 /= norm
    SEq_2 /= norm
    SEq_3 /= norm
    SEq_4 /= norm
    x = SEq_2
    y = SEq_3
    z = SEq_4
    w = SEq_1
    print "%8.7f" % SEq_1 + " ",
    print "%8.7f" % SEq_2 + " ",
    print "%8.7f" % SEq_3 + " ",
    print "%8.7f" % SEq_4
    m1_1 = 1 - 2*y*y - 2*z*z
    m1_2 = 2*x*y + 2*w*z
    m1_3 = 2*x*z - 2*w*y
    m1_4 = 0
    m2_1 = 2*x*y - 2*w*z
    m2_2 = 1 - 2*x*x - 2*z*z
    m2_3 = 2*y*z + 2*w*x
    m2_4 = 0
    m3_1 = 2*x*z + 2*w*y
    m3_2 = 2*y*z - 2*w*x
    m3_3 = 1 - 2*x*x -2*y*y
    m3_4 = 0
    m4_1 = 0
    m4_2 = 0
    m4_3 = 0
    m4_4 = 1
    # a_x = math.asin(math.degrees(m3_2))
    print "%8.7f" % m3_2
while True:
	#acc = Acc.put9axis()

	#print "%+8.7f" % acc[0] + " ",
	#print "%+8.7f" % acc[1] + " ",
	#print "%+8.7f" % acc[2]
	#print " |   ",
	#print "%+8.7f" % gyr[0] + " ",
	#print "%+8.7f" % gyr[1] + " ",
	#print "%+8.7f" % gyr[2] + " ",
	#print " |   ",
	#print "%+8.7f" % mag[0] + " ",
	#print "%+8.7f" % mag[1] + " ",
	#print "%+8.7f" % mag[2]
	acc = mpu.getAccel()
	gyr = mpu.getGyro()
	filterUpdate(gyr[0], gyr[1], gyr[2], acc[0], acc[1], acc[2])
	#x_angle = math.degrees( math.atan2( acc[0], math.sqrt(acc[1] ** 2 + acc[2] ** 2 )))
	#y_angle = math.degrees( math.atan2( acc[1], math.sqrt(acc[0] ** 2 + acc[2] ** 2 )))
	#print("X Angle:", x_angle, "Y Angle", y_angle)
	
	time.sleep(1.0)
