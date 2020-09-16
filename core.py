#!/usr/bin/env python3

from utils import *
from mutationinfos_converter import *
from mutator_applier import *


def func():
    convert()
    mut_infos = read_mut_infos_from_file()
    revert_proj_to_orig()
    mutate_code([mut_infos[0]])
    run_mutated_application()

    run_test_suite_command()

if __name__ == '__main__':
    func()
