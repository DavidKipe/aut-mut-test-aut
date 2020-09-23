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


def output_file(mutant_id, start_time_str, testsuite_name):
	out_file = "output"
	if not os.path.exists(out_file):
		os.mkdir(out_file)

	out_file = os.path.join(out_file, start_time_str)
	if not os.path.exists(out_file):
		os.mkdir(out_file)

	out_file = os.path.join(out_file, "mutant_{}".format(mutant_id))
	if not os.path.exists(out_file):
		os.mkdir(out_file)

	out_file = os.path.join(out_file, "{}.txt".format(testsuite_name))

	return out_file


def run_testsuite(mutant_id, start_time_str, testsuite_rootdir, testsuite_command, testsuite_name, testsuite_tag):
	out_file = output_file(mutant_id, start_time_str, testsuite_tag)

	print("Running test suite '{}' for mutant {} ...".format(testsuite_name, mutant_id))

	with open(out_file, 'w') as f:
		completed_process = subprocess.run([testsuite_command], cwd=testsuite_rootdir, shell=True, encoding='utf-8', stderr=subprocess.STDOUT, stdout=f)

	print("Test suite '{}' for mutant {} completed".format(testsuite_name, mutant_id))

	return completed_process


def run_testsuite_assertions(mutant_id, start_time_str):
	return run_testsuite(mutant_id, start_time_str, testsuite_assertions_rootdir, run_testsuite_assertions_command, "Selenium assertions", "selenium")


def run_testsuite_retest_expl(mutant_id, start_time_str):
	return run_testsuite(mutant_id, start_time_str, testsuite_retest_expl_rootdir, run_testsuite_retest_expl_command, "ReTest Recheck explicit check", "retest_explicit")


def run_testsuite_retest_impl(mutant_id, start_time_str):
	return run_testsuite(mutant_id, start_time_str, testsuite_retest_impl_rootdir, run_testsuite_retest_impl_command, "ReTest Recheck implicit check", "retest_implicit")
