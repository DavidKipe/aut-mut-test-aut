#!/usr/bin/env python3

import asyncio
import time
from datetime import datetime

from mutated_app_manager import MutatedAppManager
from mutator import *


# This main mutates the application and executes the mutants, then sleeps for 4 hours leaving the mutant runs in background


async def main():
	time_str = datetime.now().strftime("%Y%m%d-%H%M%S")
	print(f"Starting time: {time_str}\n")

	revert_project_to_orig()  # ensure the project to be original at the beginning

	file_mutants_to_be_read = 'resources/shopizer_selected_mutations_max3.json'
	mutations_info = read_mut_infos_from_file(file_mutants_to_be_read)  # read the info about mutations

	mutated_app_manager = MutatedAppManager()
	mutated_app_manager.reset_application_state()  # ensure to reset the application state before the first mutation

	mutant_to_be_run = 1754

	for i, mut_info in enumerate(mutations_info):  # for each mutant

		if mut_info.id != mutant_to_be_run:
			continue

		print(f"[Counter: {i}] Mutant ID: {mut_info.id} ('MasterID': {mut_info.master_id})")

		try:
			mutate_code(mut_info)  # run the mutator

			mutated_app_manager.run_async()  # run the application mutated

			start_wait_ended_successfully = mutated_app_manager.wait_until_ready()  # wait until application is ready to use

			if start_wait_ended_successfully:
				print(" ###  READY  ###")
				print("Mutant is running")
				time.sleep(14400)  # mutant runs for 4 hours
			else:
				print("ERROR")
				print(mutated_app_manager.stop_and_reset())

		finally:
			revert_sourcefile_to_orig(mut_info)  # revert sourcecode to original, whether the execution was ok or threw an exception
			mutated_app_manager.stop_and_reset()  # if the app still running, try to stop it
			print(f"Mutants: {mut_info.id} TERMINATED\n")


if __name__ == '__main__':
	asyncio.run(main())
