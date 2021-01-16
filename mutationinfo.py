# Python 3.7+ needed

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class MutatorType(Enum):
	CONST_FUNC_ELAB = 512  # '+ 512' is for mutator that needs function to be elaborated (dynamic mutated line)
	CONST_POST_SOURCE_ELAB = 1024  # '+ 1024' is for mutator that needs post elaborations of the source code after being applied

	UNKNOWN = 255

	NEGATE_COND = 1 + CONST_FUNC_ELAB

	RTN_EMPTY_COLLECTION = 2 + CONST_FUNC_ELAB + CONST_POST_SOURCE_ELAB

	REMOVE_CALL = 3
	RTN_EMPTY_STR = 4
	RTN_NULL = 5
	RTN_FALSE = 6
	RTN_TRUE = 7
	RTN_ZERO_INT = 8
	RTN_ZERO_INTEGER = 9


class TestStatus(Enum):
	SKIPPED = -1
	PASSED = 0
	FAILURE = 1
	ERROR = 2


@dataclass
class TestResult:
	name: str
	class_name: str
	status: TestStatus

	def to_dict(self):
		return {
			'name': self.name,
			'className': self.class_name,
			'status': self.status.name
		}


@dataclass
class MutationTestsResult:
	test_suite_tag: str
	test_suite_name: str = ''
	success: bool = True
	total_tests: int = 0
	passed_tests: int = 0
	failed_tests: int = 0
	error_tests: int = 0
	skipped_tests: int = 0
	time_sec: float = 0.0
	detailed_test_results: List[TestResult] = field(default_factory=list)  # optional

	def add_test_result(self, test_result):
		self.detailed_test_results.append(test_result)

	def sort_detailed_test_results(self):
		self.detailed_test_results.sort(key=lambda tr: tr.class_name + tr.name)

	def to_dict(self):
		self.sort_detailed_test_results()
		mut_test_result_dict = {
			'testSuiteTag': self.test_suite_tag,
			'testSuiteName': self.test_suite_name,
			'success': self.success,
			'totalTests': self.total_tests,
			'passed': self.passed_tests,
			'failed': self.failed_tests,
			'error': self.error_tests,
			'skipped': self.skipped_tests,
			'time_sec': round(self.time_sec, 3)
		}

		if self.detailed_test_results:
			det_test_results_dict = list()
			for det_test_result in self.detailed_test_results:
				det_test_results_dict.append(det_test_result.to_dict())
			mut_test_result_dict['detailedTestResults'] = det_test_results_dict

		return mut_test_result_dict


@dataclass
class MutationInfo:
	id: int = 0
	source_filename: str = ''
	source_root_path: str = ''
	rel_folder_path: str = ''
	line_number: int = 0
	original_line: str = ''
	mutated_line: str = ''
	mutator_type: MutatorType = MutatorType.UNKNOWN
	mutation_results: List[MutationTestsResult] = field(default_factory=list)  # optional

	def add_result(self, mut_result):
		self.mutation_results.append(mut_result)

	def get_mutation_result_of(self, testsuite_tag):
		return next((mut_result for mut_result in self.mutation_results if mut_result.test_suite_tag == testsuite_tag), None)

	def to_dict(self):
		mut_info_dict = {
			'id': self.id,
			'sourceFilename': self.source_filename,
			'sourceRootPath': self.source_root_path,
			'relFolderPath': self.rel_folder_path,
			'lineNumber': self.line_number,
			'originalLine': self.original_line,
			'mutatedLine': self.mutated_line,
			'mutatorTag': self.mutator_type.name
		}

		if self.mutation_results:  # if results exist then copy them into dict
			mut_result_dicts = list()
			for mut_result in self.mutation_results:
				mut_result_dicts.append(mut_result.to_dict())
			mut_info_dict['mutationTestsResults'] = mut_result_dicts

		return mut_info_dict


def from_dict_to_mut_info(mut_info_dict):
	mutation_info = MutationInfo()
	mutation_info.id =				mut_info_dict['id']
	mutation_info.source_filename =	mut_info_dict['sourceFilename']
	mutation_info.rel_folder_path =	mut_info_dict['relFolderPath']
	mutation_info.line_number =		mut_info_dict['lineNumber']
	mutation_info.original_line =	mut_info_dict['originalLine']
	mutation_info.mutated_line =	mut_info_dict['mutatedLine']
	mutation_info.mutator_type =	MutatorType[mut_info_dict['mutatorTag']]
	return mutation_info
