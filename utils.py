import json
from shutil import copyfile

from result_extractor import *


# TODO re-organize some of these methods in a new file "files manager"

def read_mut_infos_from_file():
	mut_infos = []

	with open(output_mut_infos_json_filename) as json_file:
		data = json.load(json_file)
		for mut_info_dict in data['mutations']:
			mut_infos.append(from_dict_to_mut_info(mut_info_dict))

	return mut_infos


def save_mutant_and_mut_info(file_mutated, mut_info):
	if not os.path.exists(mutants_dir):
		os.mkdir(mutants_dir)

	cur_mutant_dir = os.path.join(mutants_dir, 'mutant_' + str(mut_info.id))

	if not os.path.exists(cur_mutant_dir):
		os.mkdir(cur_mutant_dir)

	copyfile(file_mutated, os.path.join(cur_mutant_dir, mut_info.source_filename))

	with open(os.path.join(cur_mutant_dir, 'mutant_' + str(mut_info.id) + '.json'), 'w') as mut_info_file:
		json.dump(mut_info.to_dict(), mut_info_file, ensure_ascii=False, indent=4)


def output_dir(execution_tag):
	out_dir = "output"
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	out_dir = os.path.join(out_dir, execution_tag)
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	return out_dir


def mutant_output_dir(mutant_id, execution_tag):
	out_dir = output_dir(execution_tag)

	out_dir = os.path.join(out_dir, "mutant_{}".format(mutant_id))
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	return out_dir


def save_app_output(mutant_id, execution_tag, testsuite_tag, output_text):
	out_dir = mutant_output_dir(mutant_id, execution_tag)
	out_file = os.path.join(out_dir, "app_output_for_{}.txt".format(testsuite_tag))

	with open(out_file, 'w') as f:
		f.write(output_text)


def save_test_suite_output(mutant_id, execution_tag, testsuite_tag, output_text):
	out_dir = mutant_output_dir(mutant_id, execution_tag)
	out_file = os.path.join(out_dir, "test_suite_{}_output.txt".format(testsuite_tag))

	with open(out_file, 'w') as f:
		f.write(output_text)


def copy_surefire_report(mutant_id, execution_tag, testsuite_rootdir, testsuite_tag):
	orig_report = os.path.join(testsuite_rootdir, 'target/site', 'surefire-report.html')

	out_dir = mutant_output_dir(mutant_id, execution_tag)
	out_report = os.path.join(out_dir, "test_suite_{}_report.html".format(testsuite_tag))

	copyfile(orig_report, out_report)


def save_mut_info(mut_info, execution_tag):
	out_dir = mutant_output_dir(mut_info.id, execution_tag)
	out_file = os.path.join(out_dir, 'mutant_' + str(mut_info.id) + '.json')

	with open(out_file, 'w') as mut_info_file:
		json.dump(mut_info.to_dict(), mut_info_file, ensure_ascii=False, indent=4)


def get_source_file_path(mut_info):
	if not mut_info.source_root_path:  # this is for support multiple root paths of the source code
		for source_path in source_paths:  # search for the file existing in one of the source paths in the configuration
			file_path = os.path.join(source_path, mut_info.rel_folder_path, mut_info.source_filename)
			if os.path.isfile(file_path):
				mut_info.source_root_path = source_path
				return file_path

		raise FileNotFoundError
	else:
		return os.path.join(mut_info.source_root_path, mut_info.rel_folder_path, mut_info.source_filename)


def backup_source_file(file_path_to_change):  # back up the original source file and return the backed up file path
	backup_file_path = file_path_to_change + backup_ext  # backup file name

	if not os.path.exists(backup_file_path):
		copyfile(file_path_to_change, backup_file_path)  # backup of the original file if not already exists

	return backup_file_path


def copyfile_in_place_as_tmp(file_to_copy):
	tmp_file_path = file_to_copy + '.tmp'  # temporary file name
	copyfile(file_to_copy, tmp_file_path)  # create the temporary copying the original
	return tmp_file_path


def remove_file(file_path):
	try:
		os.remove(file_path)
	except OSError:
		pass
