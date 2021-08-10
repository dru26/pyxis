from time import sleep
import os, sys
from math import pi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rio.pins import LF_motor, RB_motor, LB_motor, RF_motor, ir_FL, ir_BL, ir_FR, ir_BR

from multiprocessing import Thread, Lock
ir_mutex = Lock()

# number of white lines on the wheel
n = 5
# radius of the wheels in cm
r = 4.8
# k value of going forward
k1 = 1
# k value of going side to side
k2 = 0.45

ESTOP = False;
MODE = "IR"
#MODE = "VELOCITY"

SPEED = 0.2

current_position = (0, 0)

def motor_stop():
	LF_motor.stop()
	RB_motor.stop()
	LB_motor.stop()
	RF_motor.stop()

def forward(t, stop = True): # k is the time the robot will move in seconds
	if not ESTOP:
		LF_motor.forward()
		RB_motor.forward()
		LB_motor.forward()
		RF_motor.forward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def backward(t, stop = True):
	if not ESTOP:
		LF_motor.backward()
		RB_motor.backward()
		LB_motor.backward()
		RF_motor.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def left(t, stop = True):
	if not ESTOP:
	    LF_motor.forward()
	    RB_motor.forward()
	    LB_motor.backward()
	    RF_motor.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def right(t, stop = True):
	if not ESTOP:
		LF_motor.backward()
		RB_motor.backward()
		LB_motor.forward()
		RF_motor.forward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def turnRight(t, stop = True):
	if not ESTOP:
		LF_motor.forward()
		RB_motor.backward()
		LB_motor.forward()
		RF_motor.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def turnleft(t, stop = True):
	if not ESTOP:
		LF_motor.backward()
		RB_motor.forward()
		LB_motor.backward()
		RF_motor.forward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def getDistance(k):
	global pi, r, n, ir_n
	ir_mutex.aquire();
	return ((2 * pi * r) / n) * k

ir_FL_old = ir_FL.read()
ir_FR_old = ir_FR.read()
ir_BL_old = ir_BL.read()
ir_BR_old = ir_BR.read()
ir_n = 0
def monitorPosition():
	while True:
		global ir_FL_old, ir_FR_old, ir_BL_old, ir_BR_old, ir_n
		ir_mutex.acquire()
		if (ir_FL.read() < 0.5): # BLACK
			if (ir_FL_old > 0.5): # WHITE
				ir_n += 0.25
				print("FL Moved")
		if (ir_FR.read() < 0.5): # BLACK
			if (ir_FR_old > 0.5): # WHITE
				ir_n += 0.25
				print("FR Moved")
		if (ir_BL.read() < 0.5): # BLACK
			if (ir_BL_old > 0.5): # WHITE
				ir_n += 0.25
				print("BL Moved")
		if (ir_BR.read() < 0.5): # BLACK
			if (ir_BR_old > 0.5): # WHITE
				ir_n += 0.25
				print("BR Moved")
		ir_mutex.release()
		ir_FL_old = ir_FL.read()
		ir_FR_old = ir_FR.read()
		ir_BL_old = ir_BL.read()
		ir_BR_old = ir_BR.read()

'''
check if new_position[0] - current_position[0] + new_position[1] - current_position[1] = 1
'''
def moveTo(new_position):
	global current_position
	'''
	if the speed of the motor is 0.2cm/s, we can just let motor move 5 seconds to reach the destination
	(since we can assume that each position is 1cm apart in a cardinal direction)
	'''
	if MODE == "VELOCITY":
		if new_position[0] - current_position[0] == 1:
			forward(1/VELOCITY)
			current_position[0] += 1
			return
		if new_position[0] - current_position[0] == -1:
			backward(1/VELOCITY)
			current_position[0] -= 1
			return
		if new_position[1] - current_position[1] == 1:
			right(1/VELOCITY)
			current_position[1] += 1
			return
		if new_position[1] - current_position[1] == -1:
			left(1/VELOCITY)
			current_position[1] -= 1
			return
	'''Use odometry to determine where we are'''
	if MODE == "IR":
		distance = 0
		if new_position[0] - current_position[0] > 0:
			while distance < 1:
				forward(0, False)
				# Loop
				while ir_n < 1:
					pass
				motor_stop()
				distance += getDistance(k1)
			current_position[0] += distance
		elif new_position[0] - current_position[0] < 0:
			while distance < 1:
				backward(0, False)
				# Loop
				while ir_n < 1:
					pass
				motor_stop()
				distance += getDistance(k1)
			current_position[0] -= distance
		elif new_position[1] - current_position[1] > 0:
			while distance < 1:
				right(0, False)
				# Loop
				while ir_n < 1:
					pass
				motor_stop()
				distance += getDistance(k2)
			current_position[1] += distance
		elif new_position[1] - current_position[1] < 0:
			while distance < 1:
				left(0, False)
				# Loop
				while ir_n < 1:
					pass
				motor_stop()
				distance += getDistance(k2)
			current_position[1] -= distance

p = Process(target = monitorPosition)
p.start()