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
    return subprocess.run([run_app_command], cwd=app_rootdir, shell=True)


def run_test_suite():
    # with open('out-file.txt', 'w') as f:
    #     subprocess.run(['program'], stdout=f)
    return subprocess.run([run_test_suite_command], cwd=app_rootdir, shell=True, capture_output=True)
