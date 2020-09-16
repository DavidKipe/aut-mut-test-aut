# Python 3.7+ needed

from dataclasses import dataclass
from enum import Enum


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
class MutationInfo:
	id: int = 0
	source_filename: str = ''
	rel_folder_path: str = ''
	line_number: int = 0
	original_line: str = ''
	mutated_line: str = ''
	mutator_type: MutatorType = None

	def to_dict(self):
		mut_info_dict = {}
		mut_info_dict['id'] = 				self.id
		mut_info_dict['sourceFilename'] =	self.source_filename
		mut_info_dict['relFolderPath'] =	self.rel_folder_path
		mut_info_dict['lineNumber'] =		self.line_number
		mut_info_dict['originalLine'] =		self.original_line
		mut_info_dict['mutatedLine'] =		self.mutated_line
		mut_info_dict['mutatorTag'] =		self.mutator_type.name
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
