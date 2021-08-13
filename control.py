import drive.drive as drive
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
	sleep(0.1)
	if state == 0: #wait to go to table
		print("STATE 0")
		table_b.wait_for_press()
		destination = table_position
		bindings.findPath(drive.CURRENT_POSITION, destination)
		state = 1

	if state == 1: #move towards destination
		print("STATE 1")
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
		print("STATE 3")
		table_b.wait_for_press()
		destination = (0,0)
		bindings.findPath(drive.CURRENT_POSITION, destination)
		state = 1

	if state == 4: #setup routine
		if forward_b.is_pressed:
			drive.forward(0, False)
			forward_b.wait_for_release()
			drive.motor_stop()
		elif backward_b.is_pressed:
			drive.backward(0, False)
			backward_b.wait_for_release()
			drive.motor_stop()
		elif left_b.is_pressed:
			drive.left(0, False)
			left_b.wait_for_release()
			drive.motor_stop()
		elif right_b.is_pressed:
			drive.right(0, False)
			right_b.wait_for_release()
			drive.motor_stop()
		elif path_b.is_pressed:

			path_b.wait_for_release()
			print("start")
			sleep(0.5)
			print("temp")
			sleep(1)
			sleep(0.5)
			print("end")
		if table_b.is_pressed:
			table_position = drive.CURRENT_POSITION
			state = 3
