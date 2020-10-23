import asyncio
import os
import subprocess
from signal import SIGTERM
from threading import Event

from config import *


class MutatedAppManagerSingleton(type):

	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(MutatedAppManagerSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class MutatedAppManager(metaclass=MutatedAppManagerSingleton):
	_event_loop = asyncio.get_event_loop()  # get the default event loop

	_proc = None

	_rdy_event = Event()

	_stdout_text = ""

	def run_sync(self):
		if self.is_running():
			print("Mutated application already running")
		else:
			print("Running mutated application...")
			self._proc = subprocess.Popen([run_app_command], cwd=app_root_dir, shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # run the application

			with self._proc.stdout as stdout:  # capture the output
				for stdout_line in stdout:
					line_decoded = stdout_line.decode()
					#print(line_decoded, end='')
					self._stdout_text += line_decoded  # save the output in an internal variable
					if self._rdy_event.is_set() is False and app_ready_stdout_signal in line_decoded:  # check for the "ready signal"
						self._rdy_event.set()  # set the application ready

	def run_async(self):
		self._event_loop.run_in_executor(None, self.run_sync)  # use a separated thread

	def wait_until_ready(self):
		return self._rdy_event.wait(60)

	def stop(self):
		if self.is_running():
			os.killpg(os.getpgid(self._proc.pid), SIGTERM)
			self._proc = None
			self._rdy_event.clear()

			# cancel the task in the event loop
			tasks = asyncio.all_tasks(self._event_loop)
			for t in tasks:
				t.cancel()

			print("Mutated application stopped")
		else:
			print("Mutated application not running")

		stdout_text = self._stdout_text  # reset and return the registered output of the app
		self._stdout_text = ""
		return stdout_text

	def get_output(self):
		return self._stdout_text

	def is_running(self):
		return self._proc is not None

	def is_ready(self):
		return self.is_running() and self._rdy_event.is_set()
