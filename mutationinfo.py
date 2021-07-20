# Python 3.7+ needed

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class MutatorType(Enum):
	# these values are reserved and used for logic operations
	_CONST_FUNC_ELAB = 512  # '+ 512' is for mutator that needs function to be elaborated (dynamic mutated line)
	_CONST_POST_SOURCE_ELAB = 1024  # '+ 1024' is for mutator that needs post elaborations of the source code after being applied

	UNKNOWN = 255

	# NegateConditionalsMutator
	NEGATE_COND = 1 + _CONST_FUNC_ELAB

	# EmptyObjectReturnValsMutator
	RTN_EMPTY_COLLECTION = 2 + _CONST_FUNC_ELAB + _CONST_POST_SOURCE_ELAB
	RTN_EMPTY_OPTIONAL = 30
	RTN_EMPTY_STR = 3
	RTN_ZERO_INTEGER_OBJ = 4
	RTN_ZERO_LONG_OBJ = 5
	RTN_ZERO_DOUBLE_OBJ = 6

	# VoidMethodCallMutator
	REMOVE_CALL = 7

	# NullReturnValsMutator
	RTN_NULL = 8

	# BooleanFalseReturnValsMutator
	RTN_FALSE = 9
	RTN_FALSE_OBJ = 28

	# BooleanTrueReturnValsMutator
	RTN_TRUE = 10
	RTN_TRUE_OBJ = 29

	# PrimitiveReturnsMutator
	RTN_ZERO_INT = 11
	RTN_ZERO_LONG = 12
	RTN_ZERO_DOUBLE = 13

	# ConditionalsBoundaryMutator
	CONDITIONAL_BOUNDARY = 14 + _CONST_FUNC_ELAB

	# MathMutator
	ARITHMETIC_ADDITION = 15 + _CONST_FUNC_ELAB
	ARITHMETIC_SUBTRACTION = 16 + _CONST_FUNC_ELAB
	ARITHMETIC_MULTIPLICATION = 17 + _CONST_FUNC_ELAB
	ARITHMETIC_DIVISION = 18 + _CONST_FUNC_ELAB
	ARITHMETIC_MODULUS = 19 + _CONST_FUNC_ELAB
	ARITHMETIC_AND = 20 + _CONST_FUNC_ELAB
	ARITHMETIC_OR = 21 + _CONST_FUNC_ELAB
	ARITHMETIC_EXOR = 22 + _CONST_FUNC_ELAB
	ARITHMETIC_LSHIFT = 23 + _CONST_FUNC_ELAB
	ARITHMETIC_RSHIFT = 24 + _CONST_FUNC_ELAB
	ARITHMETIC_URSHIFT = 25 + _CONST_FUNC_ELAB

	# IncrementsMutator
	INCREMENT_TO_DECREMENT = 26 + _CONST_FUNC_ELAB
	DECREMENT_TO_INCREMENT = 27 + _CONST_FUNC_ELAB

	def needs_func_elaboration(self):
		return (self.value & MutatorType._CONST_FUNC_ELAB.value) > 0

	def needs_post_source_elaboration(self):
		return (self.value & MutatorType._CONST_POST_SOURCE_ELAB.value) > 0

	def is_return_type(self):
		return self.value in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 28, 29, 30]


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
	exec_order: int = -1

	def to_dict(self):
		test_result_dict = {
			'name': self.name,
			'className': self.class_name,
			'status': self.status.name
		}

		if self.exec_order >= 0:
			test_result_dict['execOrder'] = self.exec_order

		return test_result_dict


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
		self.detailed_test_results.sort(key=lambda tr: (tr.class_name, tr.exec_order))

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
	master_id: int = None  # optional
	method_name: str = ''  # optional
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

		if self.master_id is not None:
			mut_info_dict['MasterID'] = self.master_id

		if self.method_name:
			mut_info_dict['methodName'] = self.method_name

		if self.mutation_results:  # if results exist then copy them into dict
			mut_result_dicts = list()
			for mut_result in self.mutation_results:
				mut_result_dicts.append(mut_result.to_dict())
			mut_info_dict['mutationTestsResults'] = mut_result_dicts

		return mut_info_dict

	def is_in_same_code_line(self, other_mut_info):
		return self.rel_folder_path == other_mut_info.rel_folder_path and \
			self.source_filename == other_mut_info.source_filename and \
			self.line_number == other_mut_info.line_number

	def short_print(self):
		print(f"id: {self.id}")
		print(f"Rel folder: {self.rel_folder_path}")
		print(f"File: {self.source_filename}")
		print(f"Line number: {self.line_number}")
		print(f"Type: {self.mutator_type.name}")
		print(f"Original line: {self.original_line}")
		print(f"Mutated line: {self.mutated_line}")


def from_dict_to_mut_info(mut_info_dict):
	mutation_info = MutationInfo()
	mutation_info.id =				mut_info_dict['id']
	mutation_info.source_filename =	mut_info_dict['sourceFilename']
	mutation_info.rel_folder_path =	mut_info_dict['relFolderPath']
	mutation_info.line_number =		mut_info_dict['lineNumber']
	mutation_info.original_line =	mut_info_dict['originalLine']
	mutation_info.mutated_line =	mut_info_dict['mutatedLine']
	mutation_info.mutator_type =	MutatorType[mut_info_dict['mutatorTag']]
	mutation_info.master_id =       mut_info_dict['MasterID']
	mutation_info.method_name =     mut_info_dict['methodName']
	return mutation_info
