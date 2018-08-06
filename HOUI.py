import mpu9250_1
import time
import math
import numpy as np

mpu = mpu9250_1.SL_MPU9250(0x69,1)

mpu.resetRegister()
mpu.powerWakeUp()
mpu.setAccelRange(8,True)
mpu.setGyroRange(1000,True)
mpu.setMagRegister('1000Hz','16bit')


while True:

	now = time.time()
	i = 0
	data_accx = [0]
	data_accy = [0]
	data_accz = [0]
	while True:

		acc = mpu.getAccel()
                data_accx.append(acc[0])
                data_accy.append(acc[1])
                data_accz.append(acc[2])

		if i == 30:
                        medianx = np.median(data_accx)
                        mediany = np.median(data_accy)
                        medianz = np.median(data_accz)
			break
		i = i + 1
		time.sleep(0.02)
	gyr = mpu.getGyro()
	mag = mpu.getMag()


	#x_angle = math.degrees( math.atan2( acc[0], math.sqrt(acc[1] ** 2 + acc[2] ** 2 )))
	#y_angle = math.degrees( math.atan2( acc[1], math.sqrt(acc[0] ** 2 + acc[2] ** 2 )))
	x_angle = math.degrees( math.atan2( medianx, math.sqrt(mediany ** 2 + medianz ** 2 )))
	y_angle = math.degrees( math.atan2( mediany, math.sqrt(medianx ** 2 + medianz ** 2 )))
	sita = math.degrees( math.atan( math.sqrt(medianx**2 + mediany**2)/medianz ) )
	print('x:'+ str(x_angle))
	print('y:'+ str(y_angle))
#	print('s:'+ str(sita))
#	print ('%+8.7f,%+8.7f,%+8.7f' % (mag[0],mag[1],mag[2]))
#	time.sleep(1.0)

	sleepTime = 1 - (time.time() - now)
	if sleepTime < 0.0:
		continue
	time.sleep(sleepTime)
