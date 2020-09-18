from config import *
from mutationinfo import *

import json
import subprocess
import os
from shutil import copyfile


def read_mut_infos_from_file():
	mut_infos = []

	with open(mut_infos_json_filename) as json_file:
		data = json.load(json_file)
		for mut_info_dict in data['mutations']:
			mut_infos.append(from_dict_to_mut_info(mut_info_dict))

	return mut_infos


def save_mutant(file_mutated, mut_info):
	if not os.path.exists(mutants_dir):
		os.mkdir(mutants_dir)

	cur_mutant_dir = os.path.join(mutants_dir, 'mutant_' + str(mut_info.id))

	if not os.path.exists(cur_mutant_dir):
		os.mkdir(cur_mutant_dir)

	copyfile(file_mutated, os.path.join(cur_mutant_dir, mut_info.source_filename))

	with open(os.path.join(cur_mutant_dir, 'mutant_' + str(mut_info.id) + '.json'), 'w') as mut_info_file:
		json.dump(mut_info.to_dict(), mut_info_file, ensure_ascii=False, indent=4)


def run_mutated_application():
	print("Running mutated application...")
	return subprocess.run([run_app_command], cwd=app_rootdir, shell=True)


def run_testsuite_1(mutant_id, exec_time):
	print("Running test suite 1 for mutant {}".format(mutant_id))

	with open('output_testsuite_1_mutant_{}.txt'.format(mutant_id), 'w') as f:
		completed_process = subprocess.run([run_testsuite_1_command], cwd=testsuite_1_rootdir, shell=True, encoding='utf-8', stderr=subprocess.STDOUT, stdout=f)

	print("Test suite 1 for mutant {} completed".format(mutant_id))

	return completed_process
