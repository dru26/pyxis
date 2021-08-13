import drive
import sonar
import bindings
import extra
from drive.drive import ESTOP
from time import sleep
from rio.pins import power as power_b
from rio.pins import table1 as forward_b
from rio.pins import table2 as backward_b
from rio.pins import table3 as left_b
from rio.pins import table4 as right_b
from rio.pins import table5 as path_b
from rio.pins import table6 as table_b


flag = False
state = 4
retry = 0
while True:

	if state == 0: #wait to go to table
		table_b.wait_for_press()
		destination = table_position
		bindings.findPath(drive.CURRENT_POSITION, destination)
		state = 1

	if state == 1: #move towards destination
		while bindings.hasPosition():
			if state != 1:
				break
			if not retry:
				next_position = nextPosition()
			retry = 0
			moveStatus = drive.moveto(next_position)
			if not moveStatus:
				if FAILED:
					if bindings.hasPosition():
						bindings.findPath(drive.CURRENT_POSITION, destination)
						if not bindings.hasPosition:
							extra.clearFails()
							bindings.findPath(drive.CURRENT_POSITION, destination)
					else: #close enough to destination
						retry = 0
						break
				else:
					retry = 1

		if destination == (0,0): #destination was home
			state = 3
		else:
			state = 0

	if state == 3: #wait for return to home
		table_b.wait_for_press()
		destination = (0,0)
		bindings.findPath(drive.CURRENT_POSITION, destination)
		state = 1

	if state == 4: #setup routine
		if forward_b.is_pressed():
			sleep(1)
			drive.motor_forward(1)
		if backward_b.is_pressed():
			sleep(1)
			drive.motor_backward(1)
		if left_b.is_pressed():
			sleep(1)
			drive.motor_left(1)
		if right_b.is_pressed():
			sleep(1)
			drive.motor_right(1)
		if table_b.is_pressed():
			sleep(1)
			table_position = drive.CURRENT_POSITION
			state = 3
