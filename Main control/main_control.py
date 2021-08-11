import drive
import sonar
from rio import power as power_b
from rio import table1 as forward_b
from rio import table2 as backward_b
from rio import table3 as left_b
from rio import table4 as right_b
from rio import table5 as path_b
from rio import table6 as table_b


Position table_position
flag = False
state = 0;
While True:
	
	if state == 0: #waiting state
		table_b.wait_for_press()
		#generate path here
		path_status = #bool
		if(path_status):#path OK
			state = 1
		else: #path not OK

			#wait and refresh temporary obstacles
			#generate new path again
	if state == 1: #move towards destination
		drive.moveTo(destination)
		if(): #at destination
			state = 0







	##############
	#Manual movement/set table location code
	position temp = current_position
	while forward_b.is_pressed:
		flag = True
		motor_forward1()
	if flag:
		motor_stop()
		flag = false
		current_position.y+=updateposition(?,?,?)/0.02   #update the current location by distance
	while backward_b.is_pressed:
		flag = True
		motor_backward1()
	if flag:
		motor_stop()
		flag = false
		current_position.y-=updateposition(?,?,?)/0.02
	while left_b.is_pressed:
		flag = ture
		motor_left1()
	if flag:
		motor_stop()
		flag = false
		current_position.x-=updateposition(?,?,?)/0.02
	while right_b.is_pressed:
		flag = ture
		motor_right1()
	if flag:
		motor_stop()
		flag = false
		current_position.x+=updateposition(?,?,?)/0.02
	
	if table6.is_pressed:
		table_position = current_position
		exit()

Findpath(table_position,(0,0))
while hasPosition():
    moveto(nextPosition())
	