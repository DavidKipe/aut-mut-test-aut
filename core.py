#!/usr/bin/env python3

import asyncio
from datetime import datetime

from csv_results import CSVTotalResultManager
from mutated_app_manager import MutatedAppManager
from mutationinfos_converter import convert_pit_xml_to_mut_infos_json
from mutator_applier import *


# TODO organize import
# TODO manage exception to shutdown correctly

async def main():
	start_time_str = datetime.now().strftime("%Y%m%d-%H%M%S")

	revert_proj_to_orig()
	convert_pit_xml_to_mut_infos_json()
	mut_infos = read_mut_infos_from_file()

	mutated_app_manager = MutatedAppManager()
	list_of_testsuite_funcs_to_run = [run_testsuite_assertions, run_testsuite_retest_expl]
	list_of_testsuite_tags = ['selenium', 'retest_explicit']
	csv_results_manage = CSVTotalResultManager(start_time_str, list_of_testsuite_tags)

	for mut_info in mut_infos:
		revert_proj_to_orig()  # revert code to original

		mutate_code(mut_info)  # apply the new mutator

		for i in range(0, len(list_of_testsuite_tags)):
			mutated_app_manager.run_async()  # run the application mutated

			mutated_app_manager.wait_until_ready()  # wait until application is ready to use
			# TODO save an alert (flag) for timeout elapsed, thus for the compilation error

			testsuite_tag = list_of_testsuite_funcs_to_run[i](mut_info, start_time_str)  # run the test suite and save the result

			output = mutated_app_manager.stop()  # close application
			save_app_output(mut_info.id, start_time_str, testsuite_tag, output)

		#print(json.dumps(mut_info.to_dict(), ensure_ascii=False, indent=4))
		save_mut_info(mut_info, start_time_str)
		csv_results_manage.append_result(mut_info)

	revert_proj_to_orig()


if __name__ == '__main__':
	asyncio.run(main())
