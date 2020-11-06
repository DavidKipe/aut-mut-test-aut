import csv
import os

from utils import output_dir


class CSVTotalResultWriter:

	_OVERALL_RESULT_TAG = 'main'

	_map_out_file = dict()

	def __init__(self, execution_tag, test_suite_tags):
		out_dir = output_dir(execution_tag)

		self._map_out_file[self._OVERALL_RESULT_TAG] = os.path.join(out_dir, 'results.csv')  # name of the overall results file

		for testsuite_tag in test_suite_tags:  # save in a map all the pairs (testsuite_tag, file_name) for each test suite
			self._map_out_file[testsuite_tag] = os.path.join(out_dir, 'detail_results_for_{}.csv'.format(testsuite_tag))

	def __init_overall(self):  # create (overwrite if exists) the 'results.csv' file and write the columns header
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
		] * len(self._map_out_file)

		self.__write_csv_row(self._OVERALL_RESULT_TAG, header_row, is_header=True)

	def __init_detail_for(self, mut_result):
		header_row = [  # for the MutationInfo (without test suite tag)
			'Mutant ID',
			'Source file relative path',
			'Source file name',
			'Line number',
			'Mutator type tag',
			'Original line',
			'Mutated line',
			'Test suite success',
			'Total tests',
			'Passed tests',
			'Failed tests',
			'Error tests',
			'Skipped tests',
			'Total execution time (sec)',
		]

		mut_result.sort_detailed_test_results()
		for test_result in mut_result.detailed_test_results:  # for test cases
			header_row.append(test_result.name)

		self.__write_csv_row(mut_result.test_suite_tag, header_row, is_header=True)

	def append_overall_result(self, mutation_info):  # create and append to 'results.csv' a new line with the results of the mutant passed
		if not os.path.exists(self._map_out_file[self._OVERALL_RESULT_TAG]):  # if file for the main result does not exist
			self.__init_overall()  # then init it

		row_list = [
			mutation_info.id,
			mutation_info.rel_folder_path,
			mutation_info.source_filename,
			mutation_info.line_number,
			mutation_info.mutator_type.name,
			mutation_info.original_line,
			mutation_info.mutated_line
		]

		for mut_result in mutation_info.mutation_results:
			row_list += [
				mut_result.test_suite_tag,
				mut_result.success,
				mut_result.total_tests,
				mut_result.passed_tests,
				mut_result.failed_tests,
				mut_result.error_tests,
				mut_result.skipped_tests,
				round(mut_result.time_sec, 3)
			]

		self.__write_csv_row(self._OVERALL_RESULT_TAG, row_list)

	def append_detail_result_for(self, testsuite_tag, mutation_info):
		mutation_result = mutation_info.get_mutation_result_of(testsuite_tag)

		if not os.path.exists(self._map_out_file[testsuite_tag]):  # if file for this test suite does not exist
			self.__init_detail_for(mutation_result)  # then init it with using info about the result (a priori it doesn't know how many and which test cases there are)

		row_list = [  # base info
			mutation_info.id,
			mutation_info.rel_folder_path,
			mutation_info.source_filename,
			mutation_info.line_number,
			mutation_info.mutator_type.name,
			mutation_info.original_line,
			mutation_info.mutated_line,
			mutation_result.success,
			mutation_result.total_tests,
			mutation_result.passed_tests,
			mutation_result.failed_tests,
			mutation_result.error_tests,
			mutation_result.skipped_tests,
			mutation_result.time_sec
		]

		mutation_result.sort_detailed_test_results()
		for test_result in mutation_result.detailed_test_results:  # write info about test cases
			row_list.append(test_result.status.name)

		self.__write_csv_row(testsuite_tag, row_list)

	def __write_csv_row(self, file_tag, row_list, is_header=False):
		with open(self._map_out_file[file_tag], 'w' if is_header else 'a', newline='') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow(row_list)
