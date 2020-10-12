#!/usr/bin/env python3

from config import *
from mutationinfo import *

import xml.etree.ElementTree as ET
import json
from linecache import getline
import re


_map_pit_description = {
	'negated conditional':									MutatorType.NEGATE_COND,
	'removed call to':										MutatorType.REMOVE_CALL,
	'replaced return value with ""':						MutatorType.RTN_EMPTY_STR,
	'replaced return value with null for':					MutatorType.RTN_NULL,
	'replaced return value with Collections.emptyList for':	MutatorType.RTN_EMPTY_COLLECTION,
	'replaced boolean return with false for':				MutatorType.RTN_FALSE,
	'replaced boolean return with true for':				MutatorType.RTN_TRUE,
	'replaced int return with 0 for':						MutatorType.RTN_ZERO_INT,
	'replaced Integer return value with 0 for':				MutatorType.RTN_ZERO_INTEGER
}


def _negate_cond(s):
	s = re.sub(r'(\s*)if\s*\((.*)\)', r'\1if (!(\2))', s)  # negation for 'if' statement
	s = re.sub(r'(\s*)return\s*(.*);', r'\1return !(\2);', s)  # negation for 'return' statement
	return s


_map_mutated_lines = {
	MutatorType.NEGATE_COND:			_negate_cond,
	MutatorType.REMOVE_CALL:			'',
	MutatorType.RTN_EMPTY_STR:			'return "";',
	MutatorType.RTN_NULL:				'return null;',
	MutatorType.RTN_EMPTY_COLLECTION:	'return Collections.emptyList();',  # TODO currently support only List
	MutatorType.RTN_FALSE:				'return false;',
	MutatorType.RTN_TRUE:				'return true;',
	MutatorType.RTN_ZERO_INT:			'return 0;',
	MutatorType.RTN_ZERO_INTEGER:		'return 0;'
}


def _from_classpath_to_filepath(classpath):
	path = classpath.split('.')[:-1]
	path = '/'.join(path) + '/'
	return path


def _get_orig_line(mutation_info):
	path = source_rootdir + mutation_info.rel_folder_path + mutation_info.source_filename
	return getline(path, mutation_info.line_number)


def _get_mutator_type(pit_mutator_description):
	mutator_type = MutatorType.UNKNOWN

	for pit_descr_init in _map_pit_description:
		if pit_mutator_description.startswith(pit_descr_init):
			mutator_type = _map_pit_description[pit_descr_init]
			break

	if mutator_type == MutatorType.UNKNOWN:
		print("Warning: mutator UNKNOWN")

	return mutator_type


def _create_mutated_line(mutator_type, orig_line):
	if mutator_type == MutatorType.UNKNOWN:
		return #TODO

	if (mutator_type.value & MutatorType.CONST_FUNC_ELAB.value) > 0:  # TODO create func for this bitwise op
		mutator_func = _map_mutated_lines[mutator_type]
		mutated_line = mutator_func(orig_line)
	else:
		mutated_line = _map_mutated_lines[mutator_type]

	return mutated_line


def convert_pit_xml_to_mut_infos_json():
	map_mut_type_counters = {mut_type.name: 0 for mut_type in _map_mutated_lines}

	tree = ET.parse(pit_xml_report_filename)
	xml_root = tree.getroot()  # root = mutations tag

	mutations_dict = {'mutations': []}

	counter = 0
	for mutation in xml_root:
		mutation_info = MutationInfo()
		mutation_info.id = counter

		counter += 1

		mutator_type = _get_mutator_type(mutation.find('description').text)

		mutation_info.source_filename =	mutation.find('sourceFile').text
		mutation_info.rel_folder_path =	_from_classpath_to_filepath(mutation.find('mutatedClass').text)
		mutation_info.line_number =		int(mutation.find('lineNumber').text)
		mutation_info.original_line =	_get_orig_line(mutation_info).strip()
		mutation_info.mutated_line =	_create_mutated_line(mutator_type, mutation_info.original_line)
		mutation_info.mutator_type =	mutator_type

		mutations_dict['mutations'].append(mutation_info.to_dict())

		map_mut_type_counters[mutator_type.name] += 1

	with open(mut_infos_json_filename, 'w', encoding='utf-8') as f:
		json.dump(mutations_dict, f, ensure_ascii=False, indent=4)

	return map_mut_type_counters


if __name__ == '__main__':
	print(convert_pit_xml_to_mut_infos_json())
