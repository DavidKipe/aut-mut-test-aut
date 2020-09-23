from config import *

import asyncio
import os
import subprocess
from signal import SIGTERM
from threading import Event


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

	def _run_sync(self):
		if self.is_running():
			print("Mutated application already running")
		else:
			print("Running mutated application...")
			self._proc = subprocess.Popen([run_app_command], cwd=app_rootdir, shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

			with self._proc.stdout as stdout:
				for stdout_line in stdout:
					line_decoded = stdout_line.decode()
					#print(line_decoded, end='')
					if self._rdy_event.is_set() is False and app_ready_stdout_signal in line_decoded:
						self._rdy_event.set()

	def run(self):
		self._event_loop.run_in_executor(None, self._run_sync)  # run the application mutated

	def wait_until_ready(self):
		self._rdy_event.wait(60)

	def stop(self):
		if self.is_running():
			os.killpg(os.getpgid(self._proc.pid), SIGTERM)
			self._proc = None
			self._rdy_event.clear()

			# cancel the task in the event lopp
			tasks = asyncio.all_tasks(self._event_loop)
			for t in tasks:
				t.cancel()

			print("Mutated application stopped")
		else:
			print("Mutated application not running")

	def is_running(self):
		return self._proc is not None

	def is_ready(self):
		return self.is_running() and self._rdy_event.is_set()
