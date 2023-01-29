
import signal
import platform
from enum import Enum
from queue import Queue,Empty
from threading import Thread, ThreadError

# Implements non-blocking getch for Win, Mac and linux
if platform.system() == "Windows":
	import msvcrt
	def getch_nb():
		return msvcrt.getwch()

else:
	import tty, termios, sys, select
	def getch_nb():
		ch = None
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch


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
		print("<Press any key to exit...>")
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

		
		char = getch_nb()
		if char:
			input_queue.put(char)
		#full_char = ""
		#while char:
		#	full_char+=char
		#	char = getch_nb()
		#if full_char:
		#	input_queue.put(full_char)

		#except EOFError:
			#print("thread closing (EOFError)...")
		#	return
		#except TypeError:
		#	print("thread closing (typeError)...")
		#	return
