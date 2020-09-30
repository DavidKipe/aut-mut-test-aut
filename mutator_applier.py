#!/usr/bin/env python3

from utils import *

from shutil import copyfile
import os


def apply_mutator(file_to_change, mut_info):
	filename_bak = file_to_change + backup_ext	# backup file name

	copyfile(file_to_change, filename_bak)		# backup of the original file

	with open(filename_bak, 'r') as orig_file: # open the orig file in read mode
		with open(file_to_change, 'w') as mutating_file: # open the mutated file in write mode
			cur_line_number = 1 # line counter
			for line in orig_file:
				if cur_line_number == mut_info.line_number: # if this is the line to mutate
					leading_spaces = len(line) - len(line.lstrip()) # calculate the identation of this line
					indentation = leading_spaces * indentation_format #
					mutating_file.write(indentation + '//' + line.strip() + orig_line_tag + '\n') # write the orig line commented
					mutating_file.write(indentation + mut_info.mutated_line + mutate_line_tag + '\n') # write the mutated line
				else:
					mutating_file.write(line) # otherwise copy the line
				cur_line_number += 1

	save_mutant_and_mut_info(file_to_change, mut_info)


def revert_proj_to_orig():
	for subdir, dirs, files in os.walk(source_rootdir):
		for f in files:
			if f.endswith('.java' + backup_ext):
				abspath = os.path.join(subdir, f)
				copyfile(abspath, abspath.replace(backup_ext, ''))
				os.remove(abspath)


def mutate_code(mutator_info):
	apply_mutator(os.path.join(source_rootdir, mutator_info.rel_folder_path, mutator_info.source_filename), mutator_info)


id = 0
path = 'org/springframework/samples/petclinic/owner'
filename = 'OwnerController.java'
line_to_change = 62
new_line_text = 'return "";'


if __name__ == '__main__':
	mi = MutationInfo(id, filename, path, line_to_change, '', new_line_text, None)
	revert_proj_to_orig()
	mutate_code(mi)
