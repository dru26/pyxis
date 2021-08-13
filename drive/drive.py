from time import sleep
import os, sys
from math import pi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rio.pins import motor_FL, motor_FR, motor_BL, motor_BR, ir_FL, ir_BL, ir_FR, ir_BR
from rio.pins import pwm_FL, pwm_FR, pwm_BL, pwm_BR
from rio.pins import sonar_left, sonar_right
from rio.pins import sonar_left, sonar_right
from rio.pins import power
from rio.pins import table1 as bforward
from rio.pins import table2 as bbackward
from rio.pins import table3 as bleft
from rio.pins import table4 as bright
from rio.pins import table5 as bpath
import bindings
from extra import FRONT, BACK, STEP, LEFT, RIGHT

from multiprocessing import Lock
ir_mutex = Lock()

DIRECTION = None
# number of white lines on the wheel
n = 5
# radius of the wheels in cm
r = 4.8
# k value of going forward
k1 = 1
# k value of going side to side
k2 = 0.45

ESTOP = False
POWER = power.is_pressed
MODE = "IR"
#MODE = "VELOCITY"

SPEED = 0.2
DELTA = (1/SPEED) * STEP

CURRENT_POSITION = (0, 0)

ir_n = 0
def flushIR():
	global ir_mutex, ir_n, CURRENT_POSITION, TARGET_X, TARGET_Y
	ir_mutex.acquire()
	if DIRECTION == FRONT:
		CURRENT_POSITION = (CURRENT_POSITION[0] + (ir_n * getDistance(k1)), CURRENT_POSITION[1])
	elif DIRECTION == BACK:
		CURRENT_POSITION = (CURRENT_POSITION[0] - (ir_n * getDistance(k1)), CURRENT_POSITION[1])
	elif DIRECTION == RIGHT:
		CURRENT_POSITION = (CURRENT_POSITION[0], CURRENT_POSITION[1] + (ir_n * getDistance(k2)))
	elif DIRECTION == LEFT:
		CURRENT_POSITION = (CURRENT_POSITION[0], CURRENT_POSITION[1] - (ir_n * getDistance(k2)))
	else:
		print("Something went terribly, terribly wrong here :(")
	ir_n = 0
	ir_mutex.release()

def updateESTOP():
	global ESTOP
	if DIRECTION == None:
		ESTOP = False
	if DIRECTION == FRONT and sonar_right.distance < sonar_right.threshold_distance:
		ESTOP = True
		motor_stop()
	else:
		ESTOP = False
	if DIRECTION == FRONT and sonar_left.distance < sonar_left.threshold_distance:
		ESTOP = True
		motor_stop()
	else:
		ESTOP = False

def off():
	global POWER
	print("Power OFF")
	POWER = False
	motor_stop()
	flushIR()


def on():
	global POWER
	print("Power ON")
	POWER = True
	motor_stop()
	flushIR()
	updateESTOP()

power.when_pressed = on
power.when_released = off

def motor_stop():
	global DIRECTION
	print("Motor stop!")
	motor_FL.stop()
	motor_BR.stop()
	motor_BL.stop()
	motor_FR.stop()
	#DIRECTION = None

def forward(t, stop = True): # k is the time the robot will move in seconds
	global DIRECTION
	if not DIRECTION == FRONT:
		flushIR()
		DIRECTION = FRONT
	pwm_FL.value = 0.8
	pwm_FR.value = 0.8
	pwm_BL.value = 0.8
	pwm_BR.value = 0.8
	updateESTOP()
	print("Motor forward!")
	if not ESTOP and POWER:
		motor_FL.forward()
		motor_BR.forward()
		motor_BL.forward()
		motor_FR.forward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def backward(t, stop = True):
	global DIRECTION
	print("Motor backward!")
	if not DIRECTION == BACK:
		flushIR()
		DIRECTION = BACK
	pwm_FL.value = 0.8
	pwm_FR.value = 0.8
	pwm_BL.value = 0.8
	pwm_BR.value = 0.8
	updateESTOP()
	if not ESTOP and POWER:
		motor_FL.backward()
		motor_BR.backward()
		motor_BL.backward()
		motor_FR.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def left(t, stop = True):
	global DIRECTION
	print("Motor left!")
	if not DIRECTION == LEFT:
		flushIR()
		DIRECTION = LEFT
	pwm_FL.value = 1
	pwm_FR.value = 1
	pwm_BL.value = 1
	pwm_BR.value = 1
	updateESTOP()
	if not ESTOP and POWER:
	    motor_FL.forward()
	    motor_BR.forward()
	    motor_BL.backward()
	    motor_FR.backward()
	if stop or ESTOP:
		sleep(t) # the waiting time need to be tested
		motor_stop()

def right(t, stop = True):
	global DIRECTION
	print("Motor right!")
	if not DIRECTION == RIGHT:
		flushIR()
		DIRECTION = RIGHT
	pwm_FL.value = 1
	pwm_FR.value = 1
	pwm_BL.value = 1
	pwm_BR.value = 1
	updateESTOP()
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



def checkDirection(pos):
	if pos[0] - round(CURRENT_POSITION[0]) > 0:
		return FRONT
	if pos[0] - round(CURRENT_POSITION[0]) < 0:
		return BACK
	if pos[1] - round(CURRENT_POSITION[1]) > 0:
		return RIGHT
	if pos[1] - round(CURRENT_POSITION[1]) < 0:
		return LEFT

'''
check if new_position[0] - CURRENT_POSITION[0] + new_position[1] - CURRENT_POSITION[1] = 1
'''
def moveTo(new_position):
	global CURRENT_POSITION
	print("Moving to", new_position)
	'''
	if the speed of the motor is 0.2cm/s, we can just let motor move 5 seconds to reach the destination
	(since we can assume that each position is 1cm apart in a cardinal direction)
	'''
	if MODE == "VELOCITY":
		if checkDirection(new_position) == FRONT:
			forward(DELTA)
			return
		if checkDirection(new_position) == BACK:
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
		if checkDirection(new_position) == FRONT:
			forward(0, False)
			while abs(abs(start_x) - abs(CURRENT_POSITION[0])) < STEP:
				print(abs(abs(start_x) - abs(CURRENT_POSITION[0])), STEP, "FRONT")
				if ESTOP or POWER:
					return False
				sleep(0.1)
			motor_stop()
		elif checkDirection(new_position) == BACK:
			backward(0, False)
			while abs(abs(start_x) - (CURRENT_POSITION[0])) < STEP:
				print(abs(abs(start_x) - abs(CURRENT_POSITION[0])), STEP, "BACK")
				if ESTOP or POWER:
					return False
				sleep(0.1)
			motor_stop()
		elif checkDirection(new_position) == RIGHT:
			right(0, False)
			while abs(abs(start_y) - abs(CURRENT_POSITION[1])) < STEP:
				if ESTOP or POWER:
					return False
				sleep(0.1)
			motor_stop()
			distance += getDistance(k2)
		elif checkDirection(new_position) == LEFT:
			right(0, False)
			while abs(abs(start_y) - abs(CURRENT_POSITION[1])) < STEP:
				if ESTOP or POWER:
					return False
				sleep(0.1)
			motor_stop()
	return True

# Button control
'''
bforward.when_pressed = lambda: forward(1)
bbackward.when_pressed = lambda: backward(1)
bleft.when_pressed = lambda: left(1)
bright.when_pressed = lambda: right(1)
bforward.when_released = motor_stop
bbackward.when_released = motor_stop
bleft.when_released = motor_stop
bright.when_released = motor_stop
'''

'''
# Preset path
def presetPath():
	sleep(5)
	moveTo((100, 0))
	sleep(5)
	moveTo((0, 100))
	sleep(2)
	moveTo((0, 100))
	sleep(2)
	moveTo((100, 100))
	sleep(2)
	moveTo((0, 100))
	sleep(2)
	moveTo((0, 0))

bpath.when_pressed = presetPath
'''
# Monitors
def estop(sonarDirection, sonar):
	global ESTOP
	if sonarDirection == DIRECTION:
		ESTOP = True
		motor_stop()
		print("ESTOPed!!")
		sleep(3)
		if sonar.distance < sonar.threshold_distance:
			if bindings.hasPosition():
				extra.fail(CURRENT_POSITION, DIRECTION, sonar.distance)
			motor_stop()
		else:
			ESTOP = False

def unestop(sonarDirection, sonar):
	global ESTOP
	if sonarDirection == DIRECTION and ESTOP == True:
		ESTOP = False
		print("UNESTOP!")

sonar_right.when_in_range = lambda: estop(FRONT, sonar_right)
sonar_right.when_out_of_range = lambda: unestop(FRONT, sonar_right)
#sonar_back.when_in_range = lambda: estop(BACK, sonar_back)
#sonar_back.when_out_of_range = lambda: unestop(BACK, sonar_back)
sonar_left.when_in_range = lambda: estop(FRONT, sonar_left)
sonar_left.when_out_of_range = lambda: unestop(FRONT, sonar_left)
#sonar_front.when_in_range = lambda: estop(FRONT, sonar_front)
#sonar_front.when_out_of_range = lambda: unestop(FRONT, sonar_front)

def triggerIR(ir, v):
	#print("IR", ir.value, v);
	global ir_n
	ir_mutex.acquire()
	ir_n += 0.25
	ir_mutex.release()
	if ir_n >= 1:
		print("IR Line detected; moving from", CURRENT_POSITION, "...")
		flushIR()
		print("    Now at ", CURRENT_POSITION)

ir_FL.when_line = lambda: triggerIR(ir_FL, "FL")
ir_FR.when_line = lambda: triggerIR(ir_FR, "FR")
ir_BL.when_line = lambda: triggerIR(ir_BL, "BL")
ir_BR.when_line = lambda: triggerIR(ir_BR, "BR")
