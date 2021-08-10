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
ir_FL = LineSensor(12, sample_rate = 200)
ir_FR = LineSensor(16, sample_rate = 200)
ir_BL = LineSensor(20, sample_rate = 200)
ir_BR = LineSensor(21, sample_rate = 200)

# Ultrasonic Rangers #
sonar_front = DistanceSensor(echo = 25, trigger = 4, max_distance = 4, pin_factory = factory)
sonar_back = DistanceSensor(echo = 8, trigger = 22, max_distance = 4, pin_factory = factory)
sonar_left = DistanceSensor(echo = 7, trigger = 11, max_distance = 4, pin_factory = factory)
sonar_right = DistanceSensor(echo = 1, trigger = 18, max_distance = 4, pin_factory = factory)

# Motor Control #
motor_FL = Motor(2, 3, pwm = False)
motor_FR = Motor(17, 27, pwm = False)
motor_BL = Motor(10, 9, pwm = False)
motor_BR = Motor(14, 15, pwm = False)

# PWM #
pwm = PWMOutputDevice(23, active_high = True, initial_value = 0, frequency = 10000)
pwm.value = 0.5

