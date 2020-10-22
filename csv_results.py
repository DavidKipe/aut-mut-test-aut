from utils import output_dir

import csv
import os


class CSVTotalResultManager:

	def __init__(self, start_time_str, number_of_test_suites):
		out_dir = output_dir(start_time_str)
		self._out_file = os.path.join(out_dir, 'results.csv')
		self._init_and_write_header(number_of_test_suites)

	def _init_and_write_header(self, number_of_test_suites):  # create (overwrite if exists) the 'results.csv' file and write the columns header
		header_row = [  # for the MutationInfo
			'Mutant ID',
			'Source file relative path',
			'Source file name',
			'Line number',
			'Mutator type tag',
			'Original line',
			'Mutated line'
		]

		header_row += [  # for the MutationTestsResult, one for each test suite
			'Test suite tag',
			'Test suite success',
			'Total tests',
			'Passed tests',
			'Failed tests',
			'Error tests',
			'Skipped tests',
			'Total execution time (sec)',
		] * number_of_test_suites

		with open(self._out_file, 'w', newline='') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow(header_row)

	def append_result(self, mi):  # create and append to 'results.csv' a new line with the results of the mutant passed
		row_list = [
			mi.id,
			mi.rel_folder_path,
			mi.source_filename,
			mi.line_number,
			mi.mutator_type.name,
			mi.original_line,
			mi.mutated_line
		]

		for mr in mi.mutation_results:
			row_list += [
				mr.test_suite_tag,
				mr.success,
				mr.total_tests,
				mr.passed_tests,
				mr.failed_tests,
				mr.error_tests,
				mr.skipped_tests,
				mr.time_sec
			]

		with open(self._out_file, 'a', newline='') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow(row_list)
