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
	def __run_test_suite(mutation_info, execution_tag, testsuite_rootdir, testsuite_mvn_opts, testsuite_name, testsuite_tag):
		mutant_id = mutation_info.id

		print("[Mutant id: {}] Running test suite '{}' ...".format(mutant_id, testsuite_name))

		clear_surefire_reports(testsuite_rootdir)

		opt_report_title = '-Dsurefire.report.title="Surefire report. Test suite: {}, Mutant id: {}"'.format(testsuite_tag, mutant_id)
		completed_process = subprocess.run(' '.join(['mvn', testsuite_mvn_opts, 'surefire-report:report', opt_report_title, 'surefire:test', '-B']),
				cwd=testsuite_rootdir,
				shell=True,
				encoding='utf-8',
				stderr=subprocess.STDOUT,
				stdout=subprocess.PIPE)

		save_test_suite_output(mutant_id, execution_tag, testsuite_tag, completed_process.stdout)
		copy_surefire_report_html(mutant_id, execution_tag, testsuite_rootdir, testsuite_tag)

		mut_result = extract_results_from_surefire_reports(testsuite_rootdir, testsuite_tag, testsuite_name)
		mutation_info.add_result(mut_result)

		print("[Mutant id: {}] Test suite '{}' has finished computation".format(mutant_id, testsuite_name))
		# TODO print method for MutationTestsResult

	def run_test_suite(self, testsuite_tag, mutation_info, execution_tag):
		test_suite = self._map_testsuite_info[testsuite_tag]
		self.__run_test_suite(mutation_info, execution_tag, test_suite['root_dir'], test_suite['mvn_opts'], test_suite['name'], testsuite_tag)

