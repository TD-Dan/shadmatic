
import time
import platform
from enum import Enum
from queue import Queue,Empty
from threading import Thread, ThreadError

# Implements non-blocking getch for Win, Mac and linux
if platform.system() == "Windows":
	import msvcrt
	def getch():
		if msvcrt.kbhit():
			return msvcrt.getwch()
		else:
			return None

else:
	print("using *nix input")
	import getch
	def getch():
		return getch.getch()


class InputListener:

	input_thread : Thread = None
	control_queue = Queue()
	input_queue = Queue()

	def __init__(self) -> None:
		pass
	
	def __del__(self):
		if self.input_thread:
			if self.input_thread.is_alive():
				raise ThreadError("InputListener close method not called! Make sure to match .start() with an .close() method!")

	def start(self):
		
		self.input_thread = Thread(target=thread_input, args=(self.input_queue, self.control_queue))
		self.input_thread.daemon = True
		self.input_thread.start()

	def close(self):
		#print("\n<Press any key to exit...>")
		try:
			self.control_queue.put('close')
		finally:
			self.input_thread.join()
			#print("InputListener closed.")

	def getInput(self):
		try:
			str = self.input_queue.get(block=False)
			if str:
				return str
		except Empty:
			pass
		return None


def thread_input(input_queue,control_queue):
	"""Input char getter for launching in separate thread."""
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

		#except EOFError:
			#print("thread closing (EOFError)...")
		#	return
		#except TypeError:
		#	print("thread closing (typeError)...")
		#	return
