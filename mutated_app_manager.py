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

	_ready_event = Event()
	_shutdown_event = Event()
	_is_build_failure = False

	_stdout_text = ""

	_run_path = join(app_root_dir, command_path_run) if command_path_run else app_root_dir

	def run_sync(self):
		if self.is_running():
			print("Mutated application already running")
		else:
			print("Running mutated application...")
			self._proc = subprocess.Popen([command_app_run], cwd=self._run_path, shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # run the application

			with self._proc.stdout as stdout:  # capture the output
				for stdout_line in stdout:
					line_decoded = stdout_line.decode()
					self._stdout_text += line_decoded  # save the output in an internal variable

					if self._ready_event.is_set() is False and "BUILD FAILURE" in line_decoded:  # check for the "BUILD FAILURE"
						self._is_build_failure = True

					if self._ready_event.is_set() is False and app_ready_stdout_signal in line_decoded:  # check for the "ready signal"
						self._ready_event.set()  # set the application ready

					if self._shutdown_event.is_set() is False and "Shutdown completed" in line_decoded:
						self._shutdown_event.set()

	def run_async(self):
		self._event_loop.run_in_executor(None, self.run_sync)  # use a separated thread

	def wait_until_ready(self, timeout_seconds=60):
		return self._ready_event.wait(timeout_seconds)

	def stop_and_reset(self):
		if self._proc is not None:
			os.killpg(os.getpgid(self._proc.pid), SIGTERM)

			self._proc = None
			self._ready_event.clear()
			self._shutdown_event.clear()
			self._is_build_failure = False

			# cancel the task in the event loop
			tasks = asyncio.all_tasks(self._event_loop)
			for t in tasks:
				t.cancel()

			self._shutdown_event.wait(5)
			print("Mutated application stopped")

		stdout_text = self._stdout_text  # reset and return the registered output of the app
		self._stdout_text = ""
		return stdout_text

	@staticmethod
	def reset_application_state():
		if command_app_reset:
			subprocess.Popen([command_app_reset], cwd=app_root_dir, shell=True)  # reset the application
			print("Application reset")

	def get_output(self):
		return self._stdout_text

	def is_build_failure(self):
		return self._is_build_failure

	def is_running(self):
		return self._proc is not None

	def is_ready(self):
		return self.is_running() and self._ready_event.is_set() and not self.is_build_failure()
