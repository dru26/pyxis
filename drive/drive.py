from time import sleep
import os, sys
from math import pi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import rio.pins

# number of black lines on the wheel
n = 4
# radius of the wheels in cm
r = 5
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
	global pi, r, n
	return ((2 * pi * r) / n) * k

ir_old = ir.read()
def updatePosition():
	if (ir.read() < 0.5): # BLACK
		if (ir_old > 0.5): # WHITE
			return True
	ir_old = ir.read()
	return False

'''
check if new_position.x - current_position.x + new_position.y - current_position.y = 1
'''
def moveTo(new_position):
	global current_position
	'''
	if the speed of the motor is 0.2cm/s, we can just let motor move 5 seconds to reach the destination
	(since we can assume that each position is 1cm apart in a cardinal direction)
	'''
	if MODE == "VELOCITY":
		if new_position.x - current_position.x == 1:
			forward(1/VELOCITY)
			current_position.x += 1
			return
		if new_position.x - current_position.x == -1:
			backward(1/VELOCITY)
			current_position.x -= 1
			return
		if new_position.y - current_position.y == 1:
			right(1/VELOCITY)
			current_position.y += 1
			return
		if new_position.y - current_position.y == -1:
			left(1/VELOCITY)
			current_position.y -= 1
			return
	'''Use odometry to determine where we are'''
	if MODE == "IR":
		distance = 0
		if new_position.x - current_position.x > 0:
			while distance < 1:
				forward(0, False)
				# Loop
				while not updatePosition():
					pass
				distance += getDistance(k1)
			motor_stop()
			current_position.x += distance
		elif new_position.x - current_position.x < 0:
			while distance < 1:
				backward(0, False)
				# Loop
				while not updatePosition():
					pass
				distance += getDistance(k1)
			motor_stop()
			current_position.x -= distance
		elif new_position.y - current_position.y > 0:
			while distance < 1:
				right(0, False)
				# Loop
				while not updatePosition():
					pass
				distance += getDistance(k2)
			motor_stop()
			current_position.y += distance
		elif new_position.y - current_position.y < 0:
			while distance < 1:
				left(0, False)
				# Loop
				while not updatePosition():
					pass
				distance += getDistance(k2)
			motor_stop()
			current_position.y -= distance
