#!/usr/bin/env python3

import asyncio
from datetime import datetime

from csv_result_writer import CSVTotalResultWriter
from mutated_app_manager import MutatedAppManager
from mutation_creator import create_mut_infos_json_from_pit_xml
from mutation_selector import selector_max_mutants_per_method
from mutator import *
from testsuite_manager import TestSuiteManager

# TODO change prints to logging


async def main():
	execution_tag = datetime.now().strftime("%Y%m%d-%H%M%S")  # tag of this execution (it is the name of the output directory)

	revert_proj_to_orig()  # ensure the project to be original at the beginning
	map_mut_counters = create_mut_infos_json_from_pit_xml()  # convert the XML mutations info of PIT in our JSON format (it needs a clean app project, not mutated app)
	#print("\n > Mutations created:\n" + json.dumps(map_mut_counters, indent=2))  # print out the mutations creation result

	output_file_mutants_selected = 'resources/shopizer_selected_mutations_max3.json'
	# selector_max_mutants_per_method(output_mut_infos_json_filename, output_file_mutants_selected, 2)
	mutations_info = read_mut_infos_from_file(output_file_mutants_selected)  # read the info about mutations

	mutated_app_manager = MutatedAppManager()
	test_suite_manager = TestSuiteManager()
	csv_result_writer = CSVTotalResultWriter(execution_tag, test_suite_manager.get_test_suite_tags())

	for mut_info in mutations_info[15:]:  # for each mutant

		if mut_info.id in mutants_to_skip:  # check if this mutant must be skipped
			continue

		print(f"Mutant: {mut_info.id}")

		try:
			mutate_code(mut_info)  # run the mutator
			#insert_print_for_mutation_coverage(mut_info)

			for testsuite_tag in test_suite_manager.get_test_suite_tags():  # for each test suite, run the mutated app and then the test suite
				mutated_app_manager.run_async()  # run the application mutated

				mutated_app_manager.wait_until_ready()  # wait until application is ready to use

				if not mutated_app_manager.is_ready():
					if mutated_app_manager.is_build_failure():
						print("[ERROR] Mutated application not running (BUILD FAILURE)")
					else:
						print("[ERROR] Mutated application not running (timeout)")
				# else:
				# 	test_suite_manager.run_test_suite(testsuite_tag, mut_info, execution_tag)  # run the test suite and save the result

				output = mutated_app_manager.stop_and_reset()  # close mutated application and get the output
				mutated_app_manager.reset_application_state()
				save_app_output(mut_info.id, execution_tag, testsuite_tag, output)  # save output
				# csv_result_writer.append_detail_result_for(testsuite_tag, mut_info)  # save in the CSV file a line with a detailed result about test cases

			# save_mut_info(mut_info, execution_tag)  # save JSON with all the info about this mutant
			# csv_result_writer.append_overall_result(mut_info)  # save all the info about this mutant in a CSV line

		finally:
			revert_sourcefile_to_orig(mut_info)  # revert sourcecode to original, whether the execution was ok or threw an exception
			mutated_app_manager.stop_and_reset()  # if the app still running, try to stop it

			print(f"Mutation: {mut_info.id} DONE")
			if mut_info.master_id is not None:
				print(f"(MasterID: {mut_info.master_id})")
			print()


if __name__ == '__main__':
	asyncio.run(main())
