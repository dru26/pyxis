GPIO Usage Guide



Buttons:

Button List:
power
table1
table2
table3
table4
table5
table6

Useful Methods/Parameters:

.is_pressed
Returns ‘True’ boolean if the button is pressed, returns ‘False’ otherwise.

.value
Returns 1 if the button is pressed, returns 0 otherwise.


Example:
table1.value is 1 when the table1 button is pressed.



IR Sensors:

IR Sensor List:
ir_FL
ir_FR
ir_BL
ir_BR

Useful Methonds/Parameters:

.value
Returns between 0 and 0.5 if black, returns between 0.5 and 1 if white.



Sonars:

Sonar List:
sonar_front
sonar_back
sonar_left
sonar_right

Useful Methods/Parameters:

.distance
Returns the distance measured by the sonar (in meters).



Motors:

Motor List:
motor_FL
motor_FR
motor_BL
motor_BR

Useful Methods/Parameters:

.forward()
Turns the motor forward.

.backward()
Turns the motor backward.

.stop()
Stops the motor.

.is_active
Returns 1 if the motor is active, returns 0 otherwise.

.value
Returns 1 if the motor is moving forward, -1 if the motor is moving backward, 0 otherwise.
