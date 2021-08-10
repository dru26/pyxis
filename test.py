from multiprocessing import Process
import multiprocessing
import asyncio
from time import sleep

def test():
	while True:
		print("hi")
		sleep(1)

def test2():
	while True:
		print("bye bye")
		sleep(1)

#multiprocessing.set_start_method('spawn')

if __name__ == "__main__":  # confirms that the code is under main function
	
	p1 = Process(target=test)
	p1.start()
	p2 = Process(target=test2)
	p2.start()
	
	while True:
		pass