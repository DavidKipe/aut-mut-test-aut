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
	if (mut_type.value & MutatorType.CONST_POST_SOURCE_ELAB.value) == 0:
		return

	# there is a post elaboration to do in the source code
	_map_post_source_elaboration_func[mut_type](file_to_change)


def apply_mutator(file_to_change, mut_info):
	filename_bak = file_to_change + backup_ext  # backup file name

	copyfile(file_to_change, filename_bak)		# backup of the original file

	with open(filename_bak, 'r') as orig_file:  # open the orig file in read mode
		with open(file_to_change, 'w') as mutating_file:  # open the mutated file in write mode
			cur_line_number = 1  # line counter
			check_instr_end = False  # needed to try to get rid of the entire original instruction and not only the line
			for line in orig_file:
				if cur_line_number == mut_info.line_number:  # if this is the line to mutate
					leading_spaces = len(line) - len(line.lstrip())  # calculate the indentation of this line
					indentation = leading_spaces * indentation_format
					mutating_file.write(indentation + '//' + line.strip() + orig_line_tag + '\n')  # write the orig line commented
					mutating_file.write(indentation + mut_info.mutated_line + mutate_line_tag + '\n')  # write the mutated line
					# if there is no end of instruction (;) at this line and it is not a NEGATE_COND (does not even support multi line mutator)
					if not mut_info.mutator_type == MutatorType.NEGATE_COND and not re.search(r";\s*(//.*)?$", line):
						check_instr_end = True  # flag to check the end of the original instruction for the next lines
				else:
					if check_instr_end:
						if re.search(r";\s*(//.*)?$", line):  # check if there is a semicolon at the end of the line
							check_instr_end = False  # if so stop to check for the end of the instruction
						continue  # continue without write this line
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
	apply_mutator(get_source_file_path(mutator_info), mutator_info)


id = 0
path = 'org/springframework/samples/petclinic/owner'
filename = 'OwnerController.java'
line_to_change = 62
new_line_text = 'return "";'


if __name__ == '__main__':
	mi = MutationInfo(id, filename, path, line_to_change, '', new_line_text, None)
	revert_proj_to_orig()
	mutate_code(mi)
