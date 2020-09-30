from utils import output_dir

import csv
import os


def append_result(mi, start_time_str):
	out_dir = output_dir(start_time_str)

	row_list = [mi.id, mi.source_filename, mi.mutator_type.name, mi.line_number]

	for mr in mi.mutation_results:
		row_list += [mr.test_suite_tag, mr.success, mr.total_tests, mr.passed_tests, mr.failed_tests, mr.error_tests, mr.skipped_tests]

	with open(os.path.join(out_dir, 'results.csv'), 'a', newline='') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(row_list)
