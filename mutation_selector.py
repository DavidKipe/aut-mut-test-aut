from utils import read_mut_infos_from_file, get_source_file_path

from itertools import groupby
from random import sample


def mutator_selector(input_file_json, output_file_json):
	mutations_info = read_mut_infos_from_file(input_file_json)

	max_mut_per_method = 3

	groups = []
	uniquekeys = []
	for k, g in groupby(mutations_info, lambda m: get_source_file_path(m) + '#' + m.method_name):
		l = list(g)
		if len(l) < max_mut_per_method:
			s = l
		else:
			s = sample(l, max_mut_per_method)
		groups.append(s)
		uniquekeys.append(k)

	flat_list = [item for sublist in groups for item in sublist]
	print(len(flat_list))
