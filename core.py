#!/usr/bin/env python3

from mutated_app_manager import MutatedAppManager
from mutator_applier import *
from mutationinfos_converter import convert_pit_xml_to_mut_infos_json

import asyncio
from datetime import datetime


async def main():
	start_time_str = datetime.now().strftime("%Y%m%d-%H%M%S")

	revert_proj_to_orig()
	convert_pit_xml_to_mut_infos_json()
	mut_infos = read_mut_infos_from_file()

	mutated_app_manager = MutatedAppManager()

	for mut_info in mut_infos:
		revert_proj_to_orig()  # revert code to original

		mutate_code([mut_info])  # apply the new mutator

		mutated_app_manager.run()  # run the application mutated

		mutated_app_manager.wait_until_ready()  # wait until application is ready to use

		run_testsuite_selenium(mut_info.id, start_time_str)  # run the test suite and save the result

		mutated_app_manager.stop()  # close application


if __name__ == '__main__':
	asyncio.run(main())
