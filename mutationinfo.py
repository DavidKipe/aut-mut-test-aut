# Python 3.7+ needed

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class MutatorType(Enum):
	UNKNOWN = 0
	NEGATE_COND = 1001
	REMOVE_CALL = 1
	RTN_EMPTY_STR = 2
	RTN_NULL = 3
	RTN_EMPTY_COLLECTION = 4
	RTN_FALSE = 5
	RTN_TRUE = 6
	RTN_ZERO_INT = 7
	RTN_ZERO_INTEGER = 8


@dataclass
class MutationResult:
	test_suite_name: str
	test_suite_success: bool = True
	total_tests: int = 0
	tests_passed: int = 0
	tests_failed: int = 0
	tests_error: int = 0
	tests_skipped: int = 0


@dataclass
class MutationInfo:
	id: int = 0
	source_filename: str = ''
	rel_folder_path: str = ''
	line_number: int = 0
	original_line: str = ''
	mutated_line: str = ''
	mutator_type: MutatorType = None
	mutation_results: List[MutationResult] = field(default_factory=list)  # optional

	def add_result(self, mut_result):
		self.mutation_results.append(mut_result)

	def to_dict(self):
		mut_info_dict = {}
		mut_info_dict['id'] = 				self.id
		mut_info_dict['sourceFilename'] =	self.source_filename
		mut_info_dict['relFolderPath'] =	self.rel_folder_path
		mut_info_dict['lineNumber'] =		self.line_number
		mut_info_dict['originalLine'] =		self.original_line
		mut_info_dict['mutatedLine'] =		self.mutated_line
		mut_info_dict['mutatorTag'] =		self.mutator_type.name # TODO check if exists

		if self.mutation_results:
			mut_result_dicts = list()
			for mut_result in self.mutation_results:
				mut_result_dict = {}
				mut_result_dict['testSuiteName'] = mut_result.test_suite_name
				mut_result_dict['testSuiteSuccess'] = mut_result.test_suite_success
				mut_result_dict['totalTests'] = mut_result.total_tests
				mut_result_dict['testsPassed'] = mut_result.tests_passed
				mut_result_dict['testsFailed'] = mut_result.tests_failed
				mut_result_dict['testsError'] = mut_result.tests_error
				mut_result_dicts.append(mut_result_dict)
			mut_info_dict['mutationResults'] = mut_result_dicts

		return mut_info_dict


def from_dict_to_mut_info(mut_info_dict):
	mutation_info = MutationInfo()
	mutation_info.id =					mut_info_dict['id']
	mutation_info.source_filename =		mut_info_dict['sourceFilename']
	mutation_info.rel_folder_path =		mut_info_dict['relFolderPath']
	mutation_info.line_number =			mut_info_dict['lineNumber']
	mutation_info.original_line =		mut_info_dict['originalLine']
	mutation_info.mutated_line =		mut_info_dict['mutatedLine']
	mutation_info.mutator_type =		MutatorType[mut_info_dict['mutatorTag']]
	return mutation_info
