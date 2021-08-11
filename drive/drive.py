from time import sleep
import os, sys
from math import pi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rio.pins import motor_FL, motor_FR, motor_BL, motor_BR, ir_FL, ir_BL, ir_FR, ir_BR
from rio.pins import sonar_back, sonar_front, sonar_left, sonar_right
from rio.pins import power
from rio.pins import table1 as bforward
from rio.pins import table2 as bbackward
from rio.pins import table3 as bleft
from rio.pins import table4 as bright
import bindings

from multiprocessing import Lock
ir_mutex = Lock()

DIRECTION = None

LEFT = 0
RIGHT = 1
FORWARD = 2
BACKWARD = 3

STEP = 5

# number of white lines on the wheel
n = 5
# radius of the wheels in cm
r = 4.8
# k value of going forward
k1 = 1
# k value of going side to side
k2 = 0.45
	
LEFT = 0
RIGHT = 1
FORWARD = 2
BACKWARD = 3

ESTOP = False
POWER = False
MODE = "IR"
#MODE = "VELOCITY"

SPEED = 0.2
DELTA = (1/SPEED) * STEP

CURRENT_POSITION = (0, 0)

def off():
	POWER = False

def on():
	POWER = True

power.when_pressed = on
power.when_released = off

def motor_stop():
	motor_FL.stop()
	motor_BR.stop()
	motor_BL.stop()
	motor_FR.stop()
	DIRECTION = None

def forward(t, stop = True): # k is the time the robot will move in seconds
	DIRECTION = FORWARD
	if not ESTOP and POWER:
		motor_FL.forward()
		motor_BR.forward()
		motor_BL.forward()
		motor_FR.forward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def backward(t, stop = True):
	DIRECTION = BACKWARD
	if not ESTOP and POWER:
		motor_FL.backward()
		motor_BR.backward()
		motor_BL.backward()
		motor_FR.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def left(t, stop = True):
	DIRECTION = LEFT
	if not ESTOP and POWER:
	    motor_FL.forward()
	    motor_BR.forward()
	    motor_BL.backward()
	    motor_FR.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def right(t, stop = True):
	DIRECTION = RIGHT
	if not ESTOP and POWER:
		motor_FL.backward()
		motor_BR.backward()
		motor_BL.forward()
		motor_FR.forward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def turnRight(t, stop = True):
	if not ESTOP and POWER:
		motor_FL.forward()
		motor_BR.backward()
		motor_BL.forward()
		motor_FR.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def turnleft(t, stop = True):
	if not ESTOP and POWER:
		motor_FL.backward()
		motor_BR.forward()
		motor_BL.backward()
		motor_FR.forward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def getDistance(k):
	global pi, r, n
	return ((2 * pi * r) / n) * k

ir_n = 0
def flushIR():
	global ir_mutex, ir_n, CURRENT_POSITION, TARGET_X, TARGET_Y
	ir_mutex.acquire()
	if DIRECTION == FORWARD:
		CURRENT_POSITION[0] += ir_n * getDistance(k1)
	elif DIRECTION == BACKWARD:
		CURRENT_POSITION[0] -= ir_n * getDistance(k1)
	elif DIRECTION == RIGHT:
		CURRENT_POSITION[1] += ir_n * getDistance(k2)
	elif DIRECTION == LEFT:
		CURRENT_POSITION[1] -= ir_n * getDistance(k2)
	else:
		print("Something went terribly, terribly wrong here :(")
	ir_n = 0
	ir_mutex.release()

def checkDirection(pos):
	if pos[0] - round(CURRENT_POSITION[0]) > 0:
		return FORWARD
	if pos[0] - round(CURRENT_POSITION[0]) < 0:
		return BACKWARD
	if pos[1] - round(CURRENT_POSITION[1]) > 0:
		return RIGHT
	if pos[1] - round(CURRENT_POSITION[1]) < 0:
		return LEFT

'''
check if new_position[0] - CURRENT_POSITION[0] + new_position[1] - CURRENT_POSITION[1] = 1
'''
def moveTo(new_position):
	global CURRENT_POSITION
	'''
	if the speed of the motor is 0.2cm/s, we can just let motor move 5 seconds to reach the destination
	(since we can assume that each position is 1cm apart in a cardinal direction)
	'''
	if MODE == "VELOCITY":
		if checkDirection(new_position) == FORWARD:
			forward(DELTA)
			return
		if checkDirection(new_position) == BACKWARD:
			backward(DELTA)
			return
		if checkDirection(new_position) == RIGHT:
			right(DELTA)
			return
		if checkDirection(new_position) == LEFT:
			left(DELTA)
			return
	'''Use odometry to determine where we are'''
	if MODE == "IR":
		start_x = CURRENT_POSITION[0]
		start_y = CURRENT_POSITION[1]
		if checkDirection(new_position) == FORWARD:
			forward(0, False)
			while abs(start_x - CURRENT_POSITION[0]) < STEP: 
				if ESTOP or POWER:
					return False
			motor_stop()
			distance += getDistance(k1)
		elif checkDirection(new_position) == BACKWARD:
			backward(0, False)
			while abs(start_x - CURRENT_POSITION[0]) < STEP:
				if ESTOP or POWER:
					return False
			motor_stop()
			distance += getDistance(k1)
		elif checkDirection(new_position) == RIGHT:
			right(0, False)
			while abs(start_y - CURRENT_POSITION[1]) < STEP:
				if ESTOP or POWER:
					return False
			motor_stop()
			distance += getDistance(k2)
		elif checkDirection(new_position) == LEFT:
			right(0, False)
			while abs(start_y - CURRENT_POSITION[1]) < STEP:
				if ESTOP or POWER:
					return False
			motor_stop()
			distance += getDistance(k2)
	return True

# Button control
bforward.when_pressed = lambda: forward(1)
bbackward.when_pressed = lambda: backward(1)
bleft.when_pressed = lambda: left(1)
bright.when_pressed = lambda: right(1)
bforward.when_released = motor_stop
bbackward.when_released = motor_stop
bleft.when_released = motor_stop
bright.when_released = motor_stop

# Monitors
def estop(sonarDirection, sonar):
	global ESTOP
	if sonarDirection == DIRECTION:
		ESTOP = True
		sleep(3)
		if sonar.distance < sonar.threshold_distance:
			if bindings.hasPosition():
				bindings.fail(DIRECTION, sonar.distance)
			motor_stop()
		else:
			ESTOP = False
		
def unestop(sonarDirection, sonar):
	if sonarDirection == DIRECTION and ESTOP == True:
		ESTOP = False

sonar_right.when_in_range = lambda: estop(RIGHT, sonar_right)
sonar_right.when_out_of_range = lambda: unestop(RIGHT, sonar_right)
sonar_back.when_in_range = lambda: estop(BACKWARD, sonar_back)
sonar_back.when_out_of_range = lambda: unestop(BACKWARD, sonar_back)
sonar_left.when_in_range = lambda: estop(LEFT, sonar_left)
sonar_left.when_out_of_range = lambda: unestop(LEFT, sonar_left)
sonar_front.when_in_range = lambda: estop(FORWARD, sonar_front)
sonar_front.when_out_of_range = lambda: unestop(FORWARD, sonar_front)

def triggerIR():
	global ir_n
	ir_mutex.acquire()
	ir_n += 0.25
	ir_mutex.release()
	if ir_n >= 1:
		flushIR()

ir_FL.when_line = triggerIR
ir_FR.when_line = triggerIR
ir_BL.when_line = triggerIR
ir_BR.when_line = triggerIR
