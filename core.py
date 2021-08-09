#!/usr/bin/env python3

import asyncio
import time
from datetime import datetime

from csv_result_writer import CSVTotalResultWriter
from mutated_app_manager import MutatedAppManager
from mutation_creator import create_mut_infos_json_from_pit_xml
from mutation_selector import selector_max_mutants_per_method
from mutator import *
from testsuite_manager import TestSuiteManager


# This main represents the "main operation" of the application


async def main():
	time_str = datetime.now().strftime("%Y%m%d-%H%M%S")
	print(f"Starting time: {time_str}\n")
	execution_tag = time_str  # tag of this execution (it is the name of the output directory)

	revert_project_to_orig()  # ensure the project to be original at the beginning
	# map_mut_counters = create_mut_infos_json_from_pit_xml()  # convert the XML mutations info of PIT in our JSON format (it needs a clean app project, not mutated app)
	# print("\n > Mutations created:\n" + json.dumps(map_mut_counters, indent=2))  # print out the mutations creation result

	output_file_mutants_selected = 'resources/shopizer_selected_mutations_max3.json'
	# selector_max_mutants_per_method(output_mut_infos_json_filename, output_file_mutants_selected, 3)

	file_mutants_to_be_read = output_file_mutants_selected
	mutations_info = read_mut_infos_from_file(file_mutants_to_be_read)  # read the info about mutations

	mutated_app_manager = MutatedAppManager()
	test_suite_manager = TestSuiteManager()
	csv_result_writer = CSVTotalResultWriter(execution_tag, test_suite_manager.get_test_suite_tags())

	mutated_app_manager.reset_application_state()  # ensure to reset the application state before the first mutation

	for i, mut_info in enumerate(mutations_info):  # for each mutant
		mutation_id = mut_info.id

		if mutation_id in mutants_to_skip:  # check if this mutant must be skipped
			csv_result_writer.append_only_id(mutation_id)
			continue

		print(f"[Counter: {i}] Mutant ID: {mutation_id} ('MasterID': {mut_info.master_id})")

		try:
			mutate_code(mut_info)  # run the mutator

			for testsuite_tag in test_suite_manager.get_test_suite_tags():  # for each test suite, run the mutated app and then the test suite
				mutated_app_manager.run_async()  # run the application mutated

				start_wait_ended_successfully = mutated_app_manager.wait_until_ready()  # wait until application is ready to use

				if not start_wait_ended_successfully:  # if the start time is timed out something wrong happened
					if mutated_app_manager.is_build_failure():
						print("[ERROR] Mutated application not running (BUILD FAILURE)")
						mut_info.app_mutated_error = AppError.BUILD_ERROR
					else:
						print("[ERROR] Mutated application not running (TIMED OUT)")
						mut_info.app_mutated_error = AppError.START_TIMED_OUT

				if start_wait_ended_successfully or i == 0:  # if this is the first mutation, then run test suite anyway to get the information about the column names for saving the CSV result
					test_suite_manager.run_test_suite(testsuite_tag, mut_info, execution_tag)  # run the test suite and save the result
					csv_result_writer.append_detail_result_for(testsuite_tag, mut_info)  # save in the CSV file a line with a detailed result about test cases

				output = mutated_app_manager.stop_and_reset()  # close mutated application and get the output
				mutated_app_manager.reset_application_state()  # reset the application state to a clean state

				if not start_wait_ended_successfully:  # save the mutated application output only if a problem was encountered
					save_app_output(mutation_id, execution_tag, testsuite_tag, output)
					if i != 0:  # in the first mutations we need to run all the test suite anyway to get the initial information about column names for CSV result
						break

			save_mut_info(mut_info, execution_tag)  # save JSON with all the info about this mutant
			csv_result_writer.append_overall_result(mut_info)  # save all the info about this mutant in a CSV line

		finally:
			revert_sourcefile_to_orig(mut_info)  # revert sourcecode to original, whether the execution was ok or threw an exception
			mutated_app_manager.stop_and_reset()  # if the app still running, try to stop it

			print(f"Mutation: {mutation_id} DONE\n")


if __name__ == '__main__':
	asyncio.run(main())
