#!/usr/bin/env python3

import asyncio
from datetime import datetime

from mutated_app_manager import MutatedAppManager
from mutator import *
from testsuite_manager import TestSuiteManager


# This main is for creating the Golden Masters for the test suite Recheck implicit for Shopizer


async def main():
	time_str = datetime.now().strftime("%Y%m%d-%H%M%S")
	print(f"Starting time: {time_str}\n")
	execution_tag = time_str  # tag of this execution (it is the name of the output directory)

	revert_project_to_orig()  # ensure the project to be original at the beginning

	mutated_app_manager = MutatedAppManager()
	test_suite_manager = TestSuiteManager()

	mutated_app_manager.reset_application_state()  # ensure to reset the application state before the first mutation

	testsuite_tag = 'retest_implicit'

	try:
		mutated_app_manager.run_async()  # run the application mutated

		mutated_app_manager.wait_until_ready()  # wait until application is ready to use

		print("Running test suite '{}' ...".format(testsuite_tag))
		test_suite_manager.run_test_suite_wa_create_golden_master(testsuite_tag)  # run the test suite and save the result

	finally:
		mutated_app_manager.stop_and_reset()  # if the app still running, try to stop it

		print(f"DONE\n")


if __name__ == '__main__':
	asyncio.run(main())
