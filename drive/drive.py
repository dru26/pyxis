from time import sleep
import os, sys
from math import pi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rio.pins import LF_motor, RB_motor, LB_motor, RF_motor, ir_FL, ir_BL, ir_FR, ir_BR
from rio.pins import power
from rio.pins import table1 as bforward
from rio.pins import table2 as bbackward
from rio.pins import table3 as bleft
from rio.pins import table4 as bright

from multiprocessing import Lock
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
POWER = False;
MODE = "IR"
#MODE = "VELOCITY"

SPEED = 0.2

current_position = (0, 0)

def off():
	POWER = False

def on():
	POWER = True

power.when_pressed = on
power.when_released = off

def motor_stop():
	LF_motor.stop()
	RB_motor.stop()
	LB_motor.stop()
	RF_motor.stop()

def forward(t, stop = True): # k is the time the robot will move in seconds
	if not ESTOP and POWER:
		LF_motor.forward()
		RB_motor.forward()
		LB_motor.forward()
		RF_motor.forward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def backward(t, stop = True):
	if not ESTOP and POWER:
		LF_motor.backward()
		RB_motor.backward()
		LB_motor.backward()
		RF_motor.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def left(t, stop = True):
	if not ESTOP and POWER:
	    LF_motor.forward()
	    RB_motor.forward()
	    LB_motor.backward()
	    RF_motor.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def right(t, stop = True):
	if not ESTOP and POWER:
		LF_motor.backward()
		RB_motor.backward()
		LB_motor.forward()
		RF_motor.forward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def turnRight(t, stop = True):
	if not ESTOP and POWER:
		LF_motor.forward()
		RB_motor.backward()
		LB_motor.forward()
		RF_motor.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def turnleft(t, stop = True):
	if not ESTOP and POWER:
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


# Button control
bforward.when_pressed = lambda: forward(0, False)
bbackward.when_pressed = lambda: backward(0, False)
bleft.when_pressed = lambda: left(0, False)
bright.when_pressed = lambda: right(0, False)
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
			if hasPosition():
				fail(DIRECTION, sonar.distance)
			motor_stop()
		else:
			ESTOP = False
		



def unestop():
	ESTOP = False

sonar_right.when_in_range = estop()
sonar_right.when_out_of_range = unestop()
sonar_back.when_in_range = estop()
sonar_back.when_out_of_range = unestop()
sonar_left.when_in_range = estop()
sonar_left.when_out_of_range = unestop()
sonar_front.when_in_range = estop()
sonar_front.when_out_of_range = unestop()

ir_n = 0

def triggerIR():
	global ir_n
	ir_mutex.acquire()
	ir_n += 0.25
	ir_mutex.release()

ir_FL.when_line = triggerIR
ir_FR.when_line = triggerIR
ir_BL.when_line = triggerIR
ir_BR.when_line = triggerIR
