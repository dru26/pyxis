# Imports #
from gpiozero import Button, LineSensor, DistanceSensor, Motor, PWMOutputDevice
from gpiozero.pins.native import NativeFactory

factory = NativeFactory()

# Buttons #
power = Button(24, pull_up = None, active_state = True, bounce_time = .005)
table1 = Button(0, pull_up = None, active_state = True, bounce_time = .005)
table2 = Button(5, pull_up = None, active_state = True, bounce_time = .005)
table3 = Button(6, pull_up = None, active_state = True, bounce_time = .005)
table4 = Button(13, pull_up = None, active_state = True, bounce_time = .005)
table5 = Button(19, pull_up = None, active_state = True, bounce_time = .005)
table6 = Button(26, pull_up = None, active_state = True, bounce_time = .005)

# IR Sensors #
ir_FL = LineSensor(12, sample_rate = 150, queue_len = 9)
ir_FR = LineSensor(16, sample_rate = 150, queue_len = 9)
ir_BL = LineSensor(20, sample_rate = 150, queue_len = 9)
ir_BR = LineSensor(21, sample_rate = 150, queue_len = 9)

# Ultrasonic Rangers #
sonar_left = DistanceSensor(echo = 25, trigger = 7, max_distance = 1.5, threshold_distance = 0.5, partial = True)
sonar_right = DistanceSensor(echo = 8, trigger = 1, max_distance = 1.5, threshold_distance = 0.5, partial = True)

# Motor Control #
motor_FL = Motor(2, 3, pwm = False)
motor_FR = Motor(17, 27, pwm = False)
motor_BL = Motor(10, 9, pwm = False)
motor_BR = Motor(14, 15, pwm = False)

# PWM #
pwm_FL = PWMOutputDevice(4, active_high = True, initial_value = 0, frequency = 400)
pwm_FR = PWMOutputDevice(22, active_high = True, initial_value = 0, frequency = 400)
pwm_BL = PWMOutputDevice(11, active_high = True, initial_value = 0, frequency = 400)
pwm_BR = PWMOutputDevice(18, active_high = True, initial_value = 0, frequency = 400)
pwm_FL.value = 0.8
pwm_FR.value = 0.8
pwm_BL.value = 0.8
pwm_BR.value = 0.8
