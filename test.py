from multiprocessing import Process

def test():
	while True:
		print("hi")
def test2():
	while True:
		print("bye bye")

if __name__ == "__main__":  # confirms that the code is under main function
	p1 = Process(target=test)
	p1.start()
	p2 = Process(target=test2)
	p2.start()
	while True:
		pass