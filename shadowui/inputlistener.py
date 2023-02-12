
import time
import platform
from enum import Enum
from queue import Empty
from multiprocessing import Queue
from multiprocessing import Process, ProcessError

# Implements non-blocking getch for Win, Mac and linux
if platform.system() == "Windows":
	import msvcrt
	def getch():
		return msvcrt.getwch()

else:
	print("using *nix input")
	import getch
	def getch():
		return getch.getch()


class InputListener:

	input_process : Process = None
	control_queue = Queue()
	input_queue = Queue()

	def __init__(self) -> None:
		pass
	
	def __del__(self):
		if self.input_process:
			if self.input_process.is_alive():
				raise ProcessError("InputListener close method not called! Make sure to match .start() with an .close() method!")

	def start(self):
		print("Starting Input process")

		self.input_process = Process(target=input_worker, args=(self.input_queue, self.control_queue))
		self.input_process.daemon = True
		self.input_process.start()

	def close(self):
		#print("\n<Press any key to exit...>")
		try:
			self.control_queue.put('close')
		finally:
			self.input_process.join()
			#print("InputListener closed.")

	def getInput(self):
		try:
			str = self.input_queue.get(block=False)
			if str:
				return str
		except Empty:
			pass
		return None


def input_worker(input_queue,control_queue):
	"""Input char getter for launching in separate thread."""
	
	print("Input process launched")
	while True:
		try:
			control = control_queue.get(block=False)
			if control == 'close':
				#print("thread closing (control message)...")
				return
		except Empty:
			pass
		#try:
		char = getch()
		if char:
			input_queue.put(char)

		time.sleep(0.01) # restrain loop to 100 fps
