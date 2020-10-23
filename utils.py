import json
import subprocess
from shutil import copyfile

from result_extractor import *


# TODO re-organize some of these methods in files

def read_mut_infos_from_file():
	mut_infos = []

	with open(mut_infos_json_filename) as json_file:
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


def output_dir(start_time_str):
	out_dir = "output"
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	out_dir = os.path.join(out_dir, start_time_str)
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	return out_dir


def mutant_output_dir(mutant_id, start_time_str):
	out_dir = output_dir(start_time_str)

	out_dir = os.path.join(out_dir, "mutant_{}".format(mutant_id))
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	return out_dir


def save_app_output(mutant_id, start_time_str, testsuite_tag, output_text):
	out_dir = mutant_output_dir(mutant_id, start_time_str)
	out_file = os.path.join(out_dir, "app_output_for_{}.txt".format(testsuite_tag))

	with open(out_file, 'w') as f:
		f.write(output_text)


def save_test_suite_output(mutant_id, start_time_str, testsuite_tag, output_text):
	out_dir = mutant_output_dir(mutant_id, start_time_str)
	out_file = os.path.join(out_dir, "test_suite_{}_output.txt".format(testsuite_tag))

	with open(out_file, 'w') as f:
		f.write(output_text)


def copy_surefire_report(mutant_id, start_time_str, testsuite_rootdir, testsuite_tag):
	orig_report = os.path.join(testsuite_rootdir, 'target/site', 'surefire-report.html')

	out_dir = mutant_output_dir(mutant_id, start_time_str)
	out_report = os.path.join(out_dir, "test_suite_{}_report.html".format(testsuite_tag))

	copyfile(orig_report, out_report)


def save_mut_info(mut_info, start_time_str):
	out_dir = mutant_output_dir(mut_info.id, start_time_str)
	out_file = os.path.join(out_dir, 'mutant_' + str(mut_info.id) + '.json')

	with open(out_file, 'w') as mut_info_file:
		json.dump(mut_info.to_dict(), mut_info_file, ensure_ascii=False, indent=4)


def run_testsuite(mut_info, start_time_str, testsuite_rootdir, testsuite_mvn_opts, testsuite_name, testsuite_tag):
	mutant_id = mut_info.id

	print("Running test suite '{}' for mutant {} ...".format(testsuite_name, mutant_id))

	clear_surefire_reports(testsuite_rootdir)

	opt_report_title = '-Dsurefire.report.title="Surefire report. Test suite: {}, Mutant id: {}"'.format(testsuite_tag, mutant_id)
	completed_process = subprocess.run(' '.join(['mvn', testsuite_mvn_opts, 'surefire-report:report', opt_report_title, 'test', '-B']),
			cwd=testsuite_rootdir,
			shell=True,
			encoding='utf-8',
			stderr=subprocess.STDOUT,
			stdout=subprocess.PIPE)

	save_test_suite_output(mutant_id, start_time_str, testsuite_tag, completed_process.stdout)
	copy_surefire_report(mutant_id, start_time_str, testsuite_rootdir, testsuite_tag)

	mut_result = extract_results_from_surefire_reports(testsuite_rootdir, testsuite_tag, testsuite_name)
	mut_info.add_result(mut_result)
	# TODO create print method for MutationTestsResult

	print("Test suite '{}' for mutant {} completed".format(testsuite_name, mutant_id))


def run_testsuite_assertions(mutant_id, start_time_str):
	testsuite_tag = "selenium"
	testsuite_name = "Selenium assertions"
	run_testsuite(mutant_id, start_time_str, testsuite_assertions_rootdir, mvn_testsuite_assertions_opts, testsuite_name, testsuite_tag)
	return testsuite_tag


def run_testsuite_retest_expl(mutant_id, start_time_str):
	testsuite_tag = "retest_explicit"
	testsuite_name = "ReTest Recheck explicit check"
	run_testsuite(mutant_id, start_time_str, testsuite_retest_expl_rootdir, mvn_testsuite_retest_expl_opts, testsuite_name, testsuite_tag)
	return testsuite_tag


def run_testsuite_retest_impl(mutant_id, start_time_str):
	testsuite_tag = "retest_implicit"
	testsuite_name = "ReTest Recheck implicit check"
	run_testsuite(mutant_id, start_time_str, testsuite_retest_impl_rootdir, mvn_testsuite_retest_impl_opts, testsuite_name, testsuite_tag)
	return testsuite_tag
