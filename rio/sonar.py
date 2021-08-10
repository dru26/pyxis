#Pyxis sonar-driver code
#Written by Zackary Kattermann
from multiprocessing import Thread, Lock
from pins import sonar_right, sonar_back, sonar_left, sonar_front

ESTOP = True

def getDistance(direction):
	if (direction == "front"):
		return (sonar_front.distance*100)
	if (direction == "back"):
		return (sonar_back.distance*100)
	if (direction == "left"):
		return (sonar_left.distance*100)
	if (direction == "right"):
		return (sonar_right.distance*100)

def checkDistance(direction, distance):
	if (direction == "front"):
		if (sonar_front.distance*100 <= distance):
			return True
		else:
			return False
	if (direction == "back"):
		if (sonar_back.distance*100 <= distance):
			return True
		else:
			return False
	if (direction == "left"):
		if (sonar_left.distance*100 <= distance):
			return True
		else:
			return False
	if (direction == "right"):
		if (sonar_right.distance*100 <= distance):
			return True
		else:
			return False

def emergencyDistance(direction, distance):
	if (direction == "front"):
		dist = sonar_front.distance*100
		return (dist - distance)
	if (direction == "back"):
		dist = sonar_back.distance*100
		return (dist - distance)
	if (direction == "left"):
		dist = sonar_left.distance*100
		return (dist - distance)
	if (direction == "right"):
		dist = sonar_right.distance*100
		return (dist - distance)