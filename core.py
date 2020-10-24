#!/usr/bin/env python3

import asyncio
from datetime import datetime

from csv_result_manager import CSVTotalResultManager
from mutated_app_manager import MutatedAppManager
from mutationinfo_converter import convert_pit_xml_to_mut_infos_json
from mutator_applier import *
from testsuite_manager import TestSuiteManager


# TODO manage exception to shutdown correctly

async def main():
	execution_tag = datetime.now().strftime("%Y%m%d-%H%M%S")

	revert_proj_to_orig()  # ensure the project to be original at the beginning
	convert_pit_xml_to_mut_infos_json()
	mut_infos = read_mut_infos_from_file()

	mutated_app_manager = MutatedAppManager()
	test_suite_manager = TestSuiteManager()
	csv_results_manager = CSVTotalResultManager(execution_tag, test_suite_manager.get_test_suite_tags())

	for mut_info in mut_infos:
		revert_proj_to_orig()  # revert code to original

		mutate_code(mut_info)  # apply the new mutator

		for testsuite_tag in test_suite_manager.get_test_suite_tags():
			mutated_app_manager.run_async()  # run the application mutated

			mutated_app_manager.wait_until_ready()  # wait until application is ready to use
			# TODO save an alert (flag) for timeout elapsed, thus for the compilation error

			test_suite_manager.run_test_suite(testsuite_tag, mut_info, execution_tag)  # run the test suite and save the result

			output = mutated_app_manager.stop()  # close mutated application
			save_app_output(mut_info.id, execution_tag, testsuite_tag, output)  # save output
			csv_results_manager.append_detail_result_for(testsuite_tag, mut_info)  # save in the CSV file a line with a detailed result about test cases

		save_mut_info(mut_info, execution_tag)  # save json with all the info about this mutant
		csv_results_manager.append_main_result(mut_info)  # save all the info about this mutant in a CSV line

	revert_proj_to_orig()  # at the end revert the project to original


if __name__ == '__main__':
	asyncio.run(main())
