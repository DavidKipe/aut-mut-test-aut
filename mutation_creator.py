#!/usr/bin/env python3

import re
import xml.etree.ElementTree as ET
from linecache import getline

from config import *
from mutationinfo import *
from utils import get_source_file_path, write_dict_to_file_json

_map_pit_description = {
	r'negated conditional':									    MutatorType.NEGATE_COND,
	r'removed call to':										    MutatorType.REMOVE_CALL,
	r'replaced return value with ""':						    MutatorType.RTN_EMPTY_STR,
	r'replaced return value with null for':					    MutatorType.RTN_NULL,
	r'replaced return value with Collections.emptyList for':	MutatorType.RTN_EMPTY_COLLECTION,
	r'replaced return value with Optional.empty for':           MutatorType.RTN_EMPTY_OPTIONAL,
	r'replaced boolean return with false for':				    MutatorType.RTN_FALSE,
	r'replaced boolean return with true for':				    MutatorType.RTN_TRUE,
	r'replaced int return with 0 for':						    MutatorType.RTN_ZERO_INT,
	r'replaced long return with 0 for':                         MutatorType.RTN_ZERO_LONG,
	r'replaced double return with 0\.0d for':                   MutatorType.RTN_ZERO_DOUBLE,
	r'replaced Integer return value with 0 for':				MutatorType.RTN_ZERO_INTEGER_OBJ,
	r'replaced Long return value with 0L for':                  MutatorType.RTN_ZERO_LONG_OBJ,
	r'replaced Double return value with 0 for':                 MutatorType.RTN_ZERO_DOUBLE_OBJ,
	r'replaced Boolean return with False for':                  MutatorType.RTN_FALSE_OBJ,
	r'replaced Boolean return with True for':                   MutatorType.RTN_TRUE_OBJ,
	r'changed conditional boundary':                            MutatorType.CONDITIONAL_BOUNDARY,
	r'Replaced (?:integer|long|float|double) addition with subtraction':        MutatorType.ARITHMETIC_ADDITION,
	r'Replaced (?:integer|long|float|double) subtraction with addition':        MutatorType.ARITHMETIC_SUBTRACTION,
	r'Replaced (?:integer|long|float|double) multiplication with division':     MutatorType.ARITHMETIC_MULTIPLICATION,
	r'Replaced (?:integer|long|float|double) division with multiplication':     MutatorType.ARITHMETIC_DIVISION,
	r'Replaced (?:integer|long|float|double) modulus with multiplication':      MutatorType.ARITHMETIC_MODULUS,
	r'Replaced bitwise AND with OR':                            MutatorType.ARITHMETIC_AND,
	r'Replaced bitwise OR with AND':                            MutatorType.ARITHMETIC_OR,
	r'Changed increment from \d+ to \-\d+':                     MutatorType.INCREMENT_TO_DECREMENT,
	r'Changed increment from -\d+ to \d+':                      MutatorType.DECREMENT_TO_INCREMENT
}


def _negate_cond(mutation_info):
	mutated_line = mutation_info.original_line
	mutated_line = re.sub(r'(\s*)if\s*\((.*)\)', r'\1if (!(\2))', mutated_line)  # negation for 'if' statement
	mutated_line = re.sub(r'(\s*)return\s*(.*);', r'\1return !(\2);', mutated_line)  # negation for 'return' statement
	mutated_line = re.sub(r'(\s*)while\s*\((.*)\)', r'\1while (!(\2))', mutated_line)  # negation for 'while' statement
	mutated_line = re.sub(r'(\s*)for\s*\((.*);\s*(.*);(.*)\)', r'\1for (\2; !(\3);\4)', mutated_line)  # negation for 'while' statement
	return mutated_line


def _empty_collection(mutation_info):
	# searching for function signature to get the return type of the collection
	collection_type = "List"  # default is List
	with open(_get_source_file_path(mutation_info), 'r') as source_file:
		content_lines = source_file.readlines()
		for line in reversed(content_lines[:mutation_info.line_number]):  # reverse order line iteration
			result = re.search(r"^(?:\s*(?:public|private|protected)\s+|\s*)(Enumeration|Iterator|List|ListIterator|Map|Set)<\w+>\s+[a-zA-Z_$][a-zA-Z_$0-9]*\s*\(", line)
			if result:
				collection_type = result.group(1)
				break

	return f'return Collections.empty{collection_type}();'


def _conditional_boundary(mutation_info):
	original_line = mutation_info.original_line
	mutated_line = original_line

	result = re.search(r"(?<!<)[\s)\w\d](?:(<=)|(<)|(>=)|(>))(?!\w*>)", original_line)  # search for the conditional operator

	if result is None:
		print(original_line)
		return original_line

	# mutate the conditional boundary
	if result.group(1):     # <=
		mutated_line = original_line.replace('<=', '<', 1)
	elif result.group(2):   # <
		mutated_line = original_line.replace('<', '<=', 1)
	elif result.group(3):   # >=
		mutated_line = original_line.replace('>=', '>', 1)
	elif result.group(4):   # >
		mutated_line = original_line.replace('>', '>=', 1)

	return mutated_line


def _arithmetic(mutation_info):
	mutator_type = mutation_info.mutator_type
	original_line = mutation_info.original_line
	mutated_line = original_line

	if mutator_type == MutatorType.ARITHMETIC_ADDITION:
		mutated_line = original_line.replace('+', '-', 1)
	elif mutator_type == MutatorType.ARITHMETIC_SUBTRACTION:
		mutated_line = original_line.replace('-', '+', 1)
	elif mutator_type == MutatorType.ARITHMETIC_MULTIPLICATION:
		mutated_line = original_line.replace('*', '/', 1)
	elif mutator_type == MutatorType.ARITHMETIC_DIVISION:
		mutated_line = original_line.replace('/', '*', 1)
	elif mutator_type == MutatorType.ARITHMETIC_MODULUS:
		mutated_line = original_line.replace('%', '*', 1)
	elif mutator_type == MutatorType.ARITHMETIC_AND:
		mutated_line = original_line.replace('&', '|', 1)
	elif mutator_type == MutatorType.ARITHMETIC_OR:
		mutated_line = original_line.replace('|', '&', 1)

	return mutated_line


def _inc_dec(mutation_info):
	mutator_type = mutation_info.mutator_type
	original_line = mutation_info.original_line
	mutated_line = original_line

	if mutator_type == MutatorType.INCREMENT_TO_DECREMENT:
		mutated_line = original_line.replace('++', '--').replace('+=', '-=')
	elif mutator_type == MutatorType.DECREMENT_TO_INCREMENT:
		mutated_line = original_line.replace('--', '++').replace('-=', '+=')

	return mutated_line


_map_mutated_lines = {
	MutatorType.NEGATE_COND:			_negate_cond,
	MutatorType.REMOVE_CALL:			'',
	MutatorType.RTN_EMPTY_STR:			'return "";',
	MutatorType.RTN_NULL:				'return null;',
	MutatorType.RTN_EMPTY_COLLECTION:	_empty_collection,
	MutatorType.RTN_EMPTY_OPTIONAL:     'return Optional.empty();',
	MutatorType.RTN_FALSE:				'return false;',
	MutatorType.RTN_TRUE:				'return true;',
	MutatorType.RTN_ZERO_INT:			'return 0;',
	MutatorType.RTN_ZERO_LONG:          'return 0;',
	MutatorType.RTN_ZERO_DOUBLE:        'return 0.0d;',
	MutatorType.RTN_ZERO_INTEGER_OBJ:   'return 0;',
	MutatorType.RTN_ZERO_LONG_OBJ:      'return 0L;',
	MutatorType.RTN_ZERO_DOUBLE_OBJ:    'return 0;',
	MutatorType.RTN_FALSE_OBJ:          'return Boolean.False;',
	MutatorType.RTN_TRUE_OBJ:           'return Boolean.True;',
	MutatorType.CONDITIONAL_BOUNDARY:   _conditional_boundary,
	MutatorType.ARITHMETIC_ADDITION:    _arithmetic,
	MutatorType.ARITHMETIC_SUBTRACTION:     _arithmetic,
	MutatorType.ARITHMETIC_MULTIPLICATION:  _arithmetic,
	MutatorType.ARITHMETIC_DIVISION:    _arithmetic,
	MutatorType.ARITHMETIC_MODULUS:     _arithmetic,
	MutatorType.ARITHMETIC_AND:         _arithmetic,
	MutatorType.ARITHMETIC_OR:          _arithmetic,
	MutatorType.INCREMENT_TO_DECREMENT:     _inc_dec,
	MutatorType.DECREMENT_TO_INCREMENT:     _inc_dec
}


def _get_source_file_path(mutation_info):
	return get_source_file_path(mutation_info)


def _from_classpath_to_filepath(classpath):
	path = classpath.split('.')[:-1]
	path = '/'.join(path) + '/'
	return path


def _get_orig_line(mutation_info):  # TODO try to get the entire instruction, not just the line
	return getline(_get_source_file_path(mutation_info), mutation_info.line_number)


def _get_mutator_type(pit_mutator_description):
	mutator_type = MutatorType.UNKNOWN

	for pit_description_regex_key, mutator_type_value in _map_pit_description.items():
		if re.search(pit_description_regex_key, pit_mutator_description):
			mutator_type = mutator_type_value
			break

	if mutator_type == MutatorType.UNKNOWN:
		print(f"\nWARNING: mutator UNKNOWN with description \"{pit_mutator_description}\"")

	return mutator_type


def _create_mutated_line(mut_info):
	mutator_type = mut_info.mutator_type
	if mutator_type == MutatorType.UNKNOWN:
		return #TODO

	if mutator_type.needs_func_elaboration():
		mutated_line = _map_mutated_lines[mutator_type](mut_info)
	else:
		mutated_line = _map_mutated_lines[mutator_type]

	return mutated_line


# convert information from XML output of PIT tool in a new JSON code adding or dropping information
def create_mut_infos_json_from_pit_xml(output_mut_file_json=output_mut_infos_json_filename):
	map_mut_counters = {mut_type.name: 0 for mut_type in _map_mutated_lines}
	skipped_mutants = []

	tree = ET.parse(input_pit_xml_report_filename)
	xml_root = tree.getroot()  # root = <mutations> tag in XML

	mutations_dict = {'mutations': []}

	last_mutation_info = MutationInfo()

	counter = 0
	for mutation in xml_root:
		mutation_info = MutationInfo()

		# search in XML file for 'MasterID', that is a custom ID
		master_id_elem = mutation.find('MasterID')
		if master_id_elem is not None:
			mutation_info.master_id = int(master_id_elem.text)

		# created ID by sequence
		mutation_info.id = counter
		counter += 1

		mutator_type = _get_mutator_type(mutation.find('description').text)

		mutation_info.source_filename =	mutation.find('sourceFile').text
		mutation_info.rel_folder_path =	_from_classpath_to_filepath(mutation.find('mutatedClass').text)
		mutation_info.line_number =		int(mutation.find('lineNumber').text)
		mutation_info.original_line =	_get_orig_line(mutation_info).strip()
		mutation_info.mutator_type =	mutator_type
		mutation_info.mutated_line =	_create_mutated_line(mutation_info)  # lastly create the modified line

		try:  # optional field
			mutation_info.method_name = mutation.find('mutatedMethod').text
		except AttributeError:
			pass

		if mutation_info.mutator_type == MutatorType.UNKNOWN:
			print(f"\n >>> Skipped mutation {mutation_info.id} because the mutation is UNKNOWN")
			mutation_info.short_print()
			skipped_mutants.append(mutation_info.id)
			continue

		if mutation_info.original_line == mutation_info.mutated_line:
			print(f"\n >>> Skipped mutation {mutation_info.id} because it DID NOT PERFORM MUTATION")
			mutation_info.short_print()
			skipped_mutants.append(mutation_info.id)
			continue

		if mutation_info.is_in_same_code_line(last_mutation_info) and mutation_info.mutated_line == last_mutation_info.mutated_line:  # currently this tool does not support more than one mutator of the same type per line)
			print(f"\n >>> Skipped mutation {mutation_info.id} because is EQUAL TO THE LAST ONE")
			print(" > LAST MUTATION")
			last_mutation_info.short_print()
			print(" > CURRENT MUTATION")
			mutation_info.short_print()
			skipped_mutants.append(mutation_info.id)
			continue

		if (mutation_info.mutator_type.is_return_type() and "return" not in mutation_info.original_line) or \
			(mutation_info.mutator_type == MutatorType.REMOVE_CALL and mutation_info.original_line.startswith('.')):
			print(f"\n >>> Skipped mutation {mutation_info.id} because is an INCONSISTENT MUTATION")
			mutation_info.short_print()
			skipped_mutants.append(mutation_info.id)
			continue

		mutations_dict['mutations'].append(mutation_info.to_dict())

		last_mutation_info = mutation_info

		map_mut_counters[mutator_type.name] += 1

	write_dict_to_file_json(mutations_dict, output_mut_file_json)

	map_mut_counters['total_mutants'] = sum(map_mut_counters.values())
	map_mut_counters['total_skipped_mutants'] = len(skipped_mutants)
	map_mut_counters['skipped_mutants'] = skipped_mutants

	return map_mut_counters


if __name__ == '__main__':
	print(create_mut_infos_json_from_pit_xml())
