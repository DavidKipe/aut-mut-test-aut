from os.path import join

## configurations ##

pit_xml_report_filename = 'resources/mutations.xml'
mut_infos_json_filename = 'resources/mutations.json'

app_root_dir = '/home/david/IdeaProjects/spring-petclinic-mutation'    # root directory of the application

surefire_reports_subdir = 'target/surefire-reports'

backup_ext = '.bak'						# this string will be appened to the original filename
orig_line_tag = ' // original line'		# this string will be appened to the original commented line
mutate_line_tag = ' // mutated line'    # this string will be appened to the mutated line
indentation_format = '\t'				# could be either '\t' (tab) or ' ' (*one* space)

# derived
source_rootdir = join(app_root_dir, 'src/main/java')  # root directory of the source code
mutants_dir = join(app_root_dir, 'mutants')  # directory of the mutant files inside the root app dir
#

run_app_command = 'mvn spring-javaformat:apply spring-boot:run -B'
app_ready_stdout_signal = "Started PetClinicApplication in"


# Information about test suites #
# all fields are mandatory
# name: full name of the test suite
# tag: short name of the test suite
# root_dir: root directory of the test suite project
# mvn_opts: options to insert in the Maven command
#   command = 'mvn {mvn_opts} surefire-report:report test -B'
test_suites = [
	{
		'name': 'Selenium assertions',
		'tag': 'assertions',
		'root_dir': '/home/david/IdeaProjects/petclinic-test-suite',
		'mvn_opts': '-Dtest="assertions.**" -Djava.awt.headless=true'
	},
	{
		'name': 'ReTest Recheck explicit check',
		'tag': 'retest_explicit',
		'root_dir': '/home/david/IdeaProjects/petclinic-test-suite',
		'mvn_opts': '-Dtest="recheck.explicit.**" -Djava.awt.headless=true'
	},
	# {
	# 	'name': 'ReTest Recheck implicit check',
	# 	'tag': 'retest_implicit',
	# 	'root_dir': '/home/david/IdeaProjects/petclinic-test-suite',
	# 	'mvn_opts': '-Dtest="recheck.implicit.**" -Djava.awt.headless=true'
	# }
]

##  ##
