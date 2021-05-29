#!/usr/bin/env python3
import re

from utils import *


def _pe_rtn_empty_collection(file_to_change):
	with open(file_to_change, 'r') as mutating_file:
		content_lines = mutating_file.readlines()

	import_match = re.search(r"(^\s*import\s+java.util.Collections;)|(^\s*import\s+static\s+java.util.Collections.emptyList;)", "".join(content_lines), re.MULTILINE)

	if import_match:
		return

	line_num_to_add = 0
	for num, line in enumerate(content_lines):
		package_match = re.search(r"^\s*package\s+.*", line)
		if package_match:
			line_num_to_add = num + 1

	content_lines.insert(line_num_to_add, "import java.util.Collections;\n")
	contents = "".join(content_lines)

	with open(file_to_change, 'w') as mutating_file:
		mutating_file.write(contents)


_map_post_source_elaboration_func = {
	MutatorType.RTN_EMPTY_COLLECTION: _pe_rtn_empty_collection
}


def _post_source_elaboration(file_to_change, mut_type):
	# check whether there is a post elaboration to do in the source code
	if mut_type.needs_post_source_elaboration():
		_map_post_source_elaboration_func[mut_type](file_to_change)


def apply_mutation(file_to_change, mut_info):
	filename_bak = file_to_change + backup_ext  # backup file name

	copyfile(file_to_change, filename_bak)		# backup of the original file

	with open(filename_bak, 'r') as orig_file:  # open the orig file in read mode
		with open(file_to_change, 'w') as mutating_file:  # open the mutated file in write mode
			cur_line_number = 1  # line counter
			for line in orig_file:
				if cur_line_number == mut_info.line_number:  # if this is the line to mutate
					leading_spaces = len(line) - len(line.lstrip())  # calculate the indentation of this line
					indentation = leading_spaces * indentation_format
					mutating_file.write(f"{indentation}//{line.strip()}{orig_line_tag}\n")  # write the orig line commented
					mutating_file.write(f"{indentation}{mut_info.mutated_line}{mutate_line_tag}\n")  # write the mutated line
				else:
					mutating_file.write(line)  # copy the line original line to the mutating file
				cur_line_number += 1

	_post_source_elaboration(file_to_change, mut_info.mutator_type)

	save_mutant_and_mut_info(file_to_change, mut_info)


def revert_proj_to_orig():
	for source_path in source_paths:
		for subdir, dirs, files in os.walk(source_path):
			for f in files:
				if f.endswith('.java' + backup_ext):
					abspath = os.path.join(subdir, f)
					copyfile(abspath, abspath.replace(backup_ext, ''))
					os.remove(abspath)


def mutate_code(mutator_info):
	#apply_mutation(get_source_file_path(mutator_info), mutator_info)
	insert_print_for_coverage(get_source_file_path(mutator_info), mutator_info)


def insert_print_for_coverage(file_to_change, mut_info):
	filename_bak = file_to_change + backup_ext  # backup file name

	copyfile(file_to_change, filename_bak)		# backup of the original file

	print_out_instr = f"System.out.println(\"$#{mut_info.id}#\");"

	with open(filename_bak, 'r') as orig_file:  # open the orig file in read mode
		with open(file_to_change, 'w') as mutating_file:  # open the mutated file in write mode
			cur_line_number = 1  # line counter
			for line in orig_file:
				if cur_line_number == mut_info.line_number:  # if this is the line to mutate
					leading_spaces = len(line) - len(line.lstrip())  # calculate the indentation of this line
					indentation = leading_spaces * indentation_format

					if re.match(r'.*else\s+if.*', mut_info.mutated_line):  # INFO: for "else if" currently it can not fully support coverage
						mutating_file.write(f"{indentation}{mut_info.original_line} {print_out_instr}\n")  # write the original line plus the print out at the end of the line
					else:
						mutating_file.write(f"{indentation}{print_out_instr} {mut_info.original_line}\n")  # write the original line plus the print out at the beginning of the line
				else:
					mutating_file.write(line)  # copy the line original line to the mutating file
				cur_line_number += 1

