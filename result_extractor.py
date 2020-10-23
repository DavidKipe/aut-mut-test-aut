import glob
import os
import xml.etree.ElementTree as ET

from config import *
from mutationinfo import *


def _get_surefire_reports_list(testsuite_rootdir):  # list of names of the surefire reports
	template_reports_path = os.path.join(testsuite_rootdir, surefire_reports_subdir, 'TEST-*.xml')
	return [f for f in glob.glob(template_reports_path)]


def extract_results_from_surefire_reports(testsuite_rootdir, testsuite_tag, testsuite_name):
	mut_result = MutationTestsResult(test_suite_tag=testsuite_tag, test_suite_name=testsuite_name)

	for test_report in _get_surefire_reports_list(testsuite_rootdir):  # parse each XML report file
		tree = ET.parse(test_report)
		root = tree.getroot()

		testsuite_attrib = root.attrib  # get the main info
		mut_result.total_tests += int(testsuite_attrib.get('tests'))
		mut_result.failed_tests += int(testsuite_attrib.get('failures'))
		mut_result.error_tests += int(testsuite_attrib.get('errors'))
		mut_result.skipped_tests += int(testsuite_attrib.get('skipped'))
		mut_result.time_sec = float(testsuite_attrib.get('time'))

		# derived info
		mut_result.passed_tests = mut_result.total_tests - mut_result.failed_tests - mut_result.error_tests - mut_result.skipped_tests
		mut_result.success = mut_result.total_tests == mut_result.passed_tests

		for testcase in root.iter('testcase'):  # get detailed info for each testcase
			status = TestStatus.PASSED
			if testcase.find('failure') is not None:
				status = TestStatus.FAILURE
			elif testcase.find('error') is not None:
				status = TestStatus.ERROR
			mut_result.add_test_result(TestResult(testcase.attrib.get('name'), testcase.attrib.get('classname'), status))

	return mut_result


# reports should be removed after extraction because must not be re-read in next extraction, since different test suites do not overwrite report files each other
def clear_surefire_reports(testsuite_rootdir):
	for test_report in _get_surefire_reports_list(testsuite_rootdir):
		os.remove(test_report)
