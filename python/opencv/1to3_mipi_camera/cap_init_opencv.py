#
#  Author: yan <yan-wyb@foxmail.com>
#  github: https://github.com/yan-wyb
#



import os
import time
import logging
import io
import datetime
import numpy as np
import cv2
import threading
import signal

def quit(signum, frame):
	print('Choose to stop.')
	os._exit(0)


def cap_init():
	os.system('cap_check 1')
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
	a,frame = cap.read()
	time.sleep(1)
	os.system('cap_check 2')
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
	a,frame = cap.read()
	time.sleep(1)
	os.system('cap_check 3')
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
	a,frame = cap.read()
	time.sleep(1)

try:
	signal.signal(signal.SIGINT, quit)
	signal.signal(signal.SIGTERM, quit)
	print('Starting Camera')
	cap = cv2.VideoCapture(0)
	if not cap.isOpened():
		print("Cannot open camera")
		exit()
	print('---------------------------')
	cap_init()

	print('cap_init success -----------------------')
	print('Set Brightness')

	num = 1
	counter = 1
	os.system('cap_check 1')
	while counter :
		print(counter)
		starttime = time.time()
		a,frame = cap.read()
		if a == False :
			print('Read camera data faile ... ')
			os._exit(0)
#		cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
		endtime = time.time()
#		cv2.imwrite('/test_{}.png'.format(counter), frame)
		print("Frame time: {}".format(endtime-starttime))

		num+=1
		if num > 3:
			num = 1
		cmd = ('cap_check1 ' + str(num))
		print(cmd)
		os.system(cmd)
		counter+=1

	cap.release()

except Exception as ex:
	print(ex)
	cap.release()
	os._exit(0)
