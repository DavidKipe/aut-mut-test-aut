#!/usr/bin/env python3

from mutated_app_manager import MutatedAppManager
from mutator_applier import *
from mutationinfos_converter import convert_pit_xml_to_mut_infos_json
from csv_results import append_result

import asyncio
from datetime import datetime

# TODO organize import

async def main():
	start_time_str = datetime.now().strftime("%Y%m%d-%H%M%S")

	revert_proj_to_orig()
	#convert_pit_xml_to_mut_infos_json()
	mut_infos = read_mut_infos_from_file()

	mutated_app_manager = MutatedAppManager()
	list_of_testsuite_funcs_to_run = [run_testsuite_assertions, run_testsuite_retest_expl]

	for mut_info in mut_infos:
		revert_proj_to_orig()  # revert code to original

		mutate_code(mut_info)  # apply the new mutator

		for testsuite_func in list_of_testsuite_funcs_to_run:
			mutated_app_manager.run_async()  # run the application mutated

			mutated_app_manager.wait_until_ready()  # wait until application is ready to use
			# TODO save an alert (flag) for timeout elapsed, thus for the compilation error

			testsuite_func(mut_info, start_time_str)  # run the test suite and save the result

			output = mutated_app_manager.stop()  # close application
			save_app_output(mut_info.id, start_time_str, output)

		#print(json.dumps(mut_info.to_dict(), ensure_ascii=False, indent=4))
		save_mut_info(mut_info, start_time_str)
		append_result(mut_info, start_time_str)


if __name__ == '__main__':
	asyncio.run(main())
