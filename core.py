#!/usr/bin/env python3

import asyncio
from datetime import datetime

from csv_result_writer import CSVTotalResultWriter
from mutated_app_manager import MutatedAppManager
from mutationinfo_converter import convert_pit_xml_to_mut_infos_json
from mutator_applier import *
from testsuite_manager import TestSuiteManager


async def main():
	execution_tag = datetime.now().strftime("%Y%m%d-%H%M%S")  # tag of this execution (it is the name of the output directory)

	revert_proj_to_orig()  # ensure the project to be original at the beginning
	convert_pit_xml_to_mut_infos_json()  # convert the XML mutations info of PIT in our JSON format (it needs a clean app project, not mutated app)
	mutations_info = read_mut_infos_from_file()  # read the info about mutations

	mutated_app_manager = MutatedAppManager()
	test_suite_manager = TestSuiteManager()
	csv_result_writer = CSVTotalResultWriter(execution_tag, test_suite_manager.get_test_suite_tags())

	for mut_info in mutations_info:  # for each mutant

		if mut_info.id in skipped_mutants:  # check if this mutant must be skipped
			continue

		try:
			mutate_code(mut_info)  # run the mutator

			for testsuite_tag in test_suite_manager.get_test_suite_tags():  # for each test suite, run the mutated app and then the test suite
				mutated_app_manager.run_async()  # run the application mutated

				mutated_app_manager.wait_until_ready()  # wait until application is ready to use
				# TODO save an alert (flag) for timeout elapsed or get the 'BUILD ERROR', so stop the execution for this mutant

				test_suite_manager.run_test_suite(testsuite_tag, mut_info, execution_tag)  # run the test suite and save the result

				output = mutated_app_manager.stop()  # close mutated application
				save_app_output(mut_info.id, execution_tag, testsuite_tag, output)  # save output
				csv_result_writer.append_detail_result_for(testsuite_tag, mut_info)  # save in the CSV file a line with a detailed result about test cases

			save_mut_info(mut_info, execution_tag)  # save JSON with all the info about this mutant
			csv_result_writer.append_overall_result(mut_info)  # save all the info about this mutant in a CSV line

		finally:
			revert_proj_to_orig()  # revert code to original, whether the execution was ok or threw an exception
			if mutated_app_manager.is_running():  # if the app still running, try to stop it
				mutated_app_manager.stop()


if __name__ == '__main__':
	asyncio.run(main())
