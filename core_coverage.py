#!/usr/bin/env python3

from datetime import datetime

from mutator import *


# This main is the core procedure to add all the print instruction for the coverage for the all given mutations


def main():
	time_str = datetime.now().strftime("%Y%m%d-%H%M%S")
	print(f"Starting time: {time_str}\n")

	revert_project_to_orig()  # ensure the project to be original at the beginning

	file_mutants_to_be_read = 'resources/shopizer_all_mutations_sorted.json'
	mutations_info = read_mut_infos_from_file(file_mutants_to_be_read)  # read the info about mutations

	for i, mut_info in enumerate(mutations_info):  # for each mutant

		if mut_info.id in mutants_to_skip:  # check if this mutant must be skipped
			continue

		print(f"[Counter: {i}] Mutant ID: {mut_info.id} ('MasterID': {mut_info.master_id})")

		try:
			insert_print_for_mutation_coverage(mut_info)  # insert the print coverage
		except Exception as exc:
			print(exc)


if __name__ == '__main__':
	main()
