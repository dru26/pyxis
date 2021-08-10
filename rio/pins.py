# Imports #
from gpiozero import Button, LineSensor, DistanceSensor, Motor, PWMOutputDevice

# Buttons #
power = Button(24, pull_up = None, active_state = True, bounce_time = .005)
table1 = Button(0, pull_up = None, active_state = True, bounce_time = .005)
table2 = Button(5, pull_up = None, active_state = True, bounce_time = .005)
table3 = Button(6, pull_up = None, active_state = True, bounce_time = .005)
table4 = Button(13, pull_up = None, active_state = True, bounce_time = .005)
table5 = Button(19, pull_up = None, active_state = True, bounce_time = .005)
table6 = Button(26, pull_up = None, active_state = True, bounce_time = .005)

# IR Sensors #
ir_FL = LineSensor(12, sample_rate = 200)
ir_FR = LineSensor(16, sample_rate = 200)
ir_BL = LineSensor(20, sample_rate = 200)
ir_BR = LineSensor(21, sample_rate = 200)

# Ultrasonic Rangers #
sonar_front = DistanceSensor(echo = 25, trigger = 4, max_distance = 4)
sonar_back = DistanceSensor(echo = 8, trigger = 22, max_distance = 4)
sonar_left = DistanceSensor(echo = 7, trigger = 11, max_distance = 4)
sonar_right = DistanceSensor(echo = 1, trigger = 18, max_distance = 4)

# Motor Control #
motor_FL = Motor(2, 3, pwm = False)
motor_FR = Motor(17, 27, pwm = False)
motor_BL = Motor(10, 9, pwm = False)
motor_BR = Motor(14, 15, pwm = False)

# PWM #
pwm_FL_1 = PWMOutputDevice(2, active_high = True, initial_value = 0, frequency = 1000)
pwm_FL_1.value = 0.5
pwm_FL_2 = PWMOutputDevice(3, active_high = True, initial_value = 0, frequency = 1000)
pwm_FL_2.value = 0.5
pwm_FR_1 = PWMOutputDevice(17, active_high = True, initial_value = 0, frequency = 1000)
pwm_FR_1.value = 0.5
pwm_FR_2 = PWMOutputDevice(27, active_high = True, initial_value = 0, frequency = 1000)
pwm_FR_2.value = 0.5
pwm_BL_1 = PWMOutputDevice(10, active_high = True, initial_value = 0, frequency = 1000)
pwm_BL_1.value = 0.5
pwm_BL_2 = PWMOutputDevice(9, active_high = True, initial_value = 0, frequency = 1000)
pwm_BL_2.value = 0.5
pwm_BR_1 = PWMOutputDevice(14, active_high = True, initial_value = 0, frequency = 1000)
pwm_BR_1.value = 0.5
pwm_BR_2 = PWMOutputDevice(15, active_high = True, initial_value = 0, frequency = 1000)
pwm_BR_2.value = 0.5
