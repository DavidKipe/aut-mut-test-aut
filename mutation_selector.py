from itertools import groupby
from random import sample

import utils


def selector_max_mutants_per_method(input_file_json, output_file_json, max_mutant_per_method):
	mutations_info = utils.read_mut_infos_from_file(input_file_json)

	method_mutants_groups = []
	# group by  (source file path & method name)
	for k, g in groupby(mutations_info, lambda m: utils.get_source_file_path(m) + '#' + m.method_name):
		method_mutants_group = list(g)

		if len(method_mutants_group) < max_mutant_per_method:
			mutants_sample = method_mutants_group
		else:
			mutants_sample = sample(method_mutants_group, max_mutant_per_method)

		method_mutants_groups.append(mutants_sample)

	mutants_selected = {'mutations': [mutation.to_dict() for method_mutants in method_mutants_groups for mutation in method_mutants]}

	utils.write_dict_to_file_json(mutants_selected, output_file_json)
