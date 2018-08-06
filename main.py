import MPU_test
import time

mpu = MPU_test.Put9axis()

while True:
	acc = mpu.put_acc()
	print "%+8.7f" % acc[0] + " ",
        print "%+8.7f" % acc[1] + " ",
        print "%+8.7f" % acc[2]

	time.sleep(1.0)
