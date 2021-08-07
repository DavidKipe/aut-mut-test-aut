import re
import subprocess

from utils import *


class TestSuiteManagerSingleton(type):

	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(TestSuiteManagerSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class TestSuiteManager(metaclass=TestSuiteManagerSingleton):

	_map_testsuite_info = dict()

	def __init__(self):
		for test_suite in test_suites:
			self._map_testsuite_info[test_suite.get('tag')] = test_suite

	def get_test_suite_tags(self):
		return self._map_testsuite_info.keys()

	@staticmethod
	def get_test_suite_names():
		return [ts.get('name') for ts in test_suites]

	@staticmethod
	def __run_test_suite(mutation_info, execution_tag, testsuite_rootdir, testsuite_mvn_opts, testsuite_name, testsuite_tag):
		mutant_id = mutation_info.id

		test_name_search = re.search(r'-Dtest=".+#(\w+)', testsuite_mvn_opts)
		test_name = ""
		if test_name_search:
			test_name = test_name_search.group(1)
			print(f"Run test '{test_name}'")

		clear_surefire_reports(testsuite_rootdir)

		opt_report_title = '-Dsurefire.report.title="Surefire report. Test suite: {}, Mutant id: {}"'.format(testsuite_tag, mutant_id)
		completed_process = None
		for i in range(10):
			completed_process = subprocess.run(' '.join(['mvn', testsuite_mvn_opts, 'surefire-report:report', opt_report_title, 'surefire:test', '-B']),
					cwd=testsuite_rootdir,
					shell=True,
					encoding='utf-8',
					stderr=subprocess.STDOUT,
					stdout=subprocess.PIPE)

			if "No last expected state to find old element in!" not in completed_process.stdout:
				break

		# copy_surefire_report_html(mutant_id, execution_tag, testsuite_rootdir, testsuite_tag)

		mut_result = extract_results_from_surefire_reports(testsuite_rootdir, testsuite_tag, testsuite_name)
		mutation_info.add_result(mut_result)
		if not mut_result.success:
			save_test_suite_output(mutant_id, execution_tag, f"FAILED-{test_name}", completed_process.stdout)

	@staticmethod
	def __run_test_suite_void_wa(testsuite_rootdir, testsuite_mvn_opts, testsuite_tag):
		clear_surefire_reports(testsuite_rootdir)

		opt_report_title = '-Dsurefire.report.title="Surefire report. Test suite: {}"'.format(testsuite_tag)
		completed_process = None
		for i in range(10):
			completed_process = subprocess.run(' '.join(['mvn', testsuite_mvn_opts, 'surefire-report:report', opt_report_title, 'surefire:test', '-B']),
					cwd=testsuite_rootdir,
					shell=True,
					encoding='utf-8',
					stderr=subprocess.STDOUT,
					stdout=subprocess.PIPE)

			if "No last expected state to find old element in!" not in completed_process.stdout:
				break

	def run_test_suite(self, testsuite_tag, mutation_info, execution_tag):
		test_suite = self._map_testsuite_info[testsuite_tag]
		self.__run_test_suite(mutation_info, execution_tag, test_suite['root_dir'], test_suite['mvn_opts'], test_suite['name'], testsuite_tag)

	def run_test_suite_workaround(self, testsuite_tag, mutation_info, execution_tag):
		test_suite = self._map_testsuite_info[testsuite_tag]
		for mvn_opts in test_suite['mvn_opts']:
			self.__run_test_suite(mutation_info, execution_tag, test_suite['root_dir'], mvn_opts, test_suite['name'], testsuite_tag)

	def run_test_suite_wa_create_golden_master(self, testsuite_tag):
		test_suite = self._map_testsuite_info[testsuite_tag]
		for mvn_opts in test_suite['mvn_opts']:
			self.__run_test_suite_void_wa(test_suite['root_dir'], mvn_opts, testsuite_tag)
