from config import *
from mutationinfo import *

import json
import subprocess


def read_mut_infos_from_file():
	mut_infos = []

	with open(mut_infos_json_filename) as json_file:
		data = json.load(json_file)
		for mut_info_dict in data['mutations']:
			mut_infos.append(from_dict_to_mut_info(mut_info_dict))

	return mut_infos


def run_mutated_application():
	print("run petclinic")
	return subprocess.run([run_app_command], cwd=app_rootdir, shell=True)


def run_testsuite_1():
	print("run test suite 1")
	with open('output_testsuite_1.txt', 'w') as f:
		completed_process = subprocess.run([run_testsuite_1_command], cwd=testsuite_1_rootdir, shell=True, encoding='ascii', stdout=f)
	return completed_process
