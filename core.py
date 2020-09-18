#!/usr/bin/env python3

from utils import *
from mutationinfos_converter import *
from mutator_applier import *

import time
import asyncio


async def main():
	#convert()
	#mut_infos = read_mut_infos_from_file()
	revert_proj_to_orig()
	#mutate_code([mut_infos[0]])

	event_loop = asyncio.get_event_loop()
	event_loop.run_in_executor(None, run_mutated_application)

	time.sleep(10)
	run_testsuite_1(0, None)

	# tasks = asyncio.all_tasks(event_loop)
	# for t in tasks:
	# 	print("cancel task" + str(t))
	# 	t.cancel()
	# 	print(t.cancelled())
	#
	# event_loop.stop()
	# event_loop.close()


if __name__ == '__main__':
	asyncio.run(main())
