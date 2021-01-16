from os.path import join

config_name = "SpringBoot PetClinic"

## configuration ##

# Application (SUT) config #
app_root_dir = '/home/david/IdeaProjects/spring-petclinic-mutation'    # root directory of the application

backup_ext = '.bak'						# this string will be appened to the original filename
orig_line_tag = ' // original line'		# this string will be appened to the original commented line
mutate_line_tag = ' // mutated line'    # this string will be appened to the mutated line
indentation_format = '\t'				# could be either '\t' (tab) or ' ' (*one* space)

source_paths = ['src/main/java']    # root directories of the source code

mutants_dir = 'mutants'             # directory name where the mutated files will be saved inside the root app dir

run_app_command = 'mvn spring-javaformat:apply spring-boot:run -B'  # command to run application
app_ready_stdout_signal = "Started PetClinicApplication in"         # what the application write on stdout when is ready
#  #

# Mutation info #
pit_xml_report_filename = 'resources/mutations.xml'     # input file from PIT
mut_infos_json_filename = 'resources/mutations.json'    # generated file by this tool

skipped_mutants = [51, 55, 88, 104, 105]    # list of ids of the mutants to be skipped
#  #

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
	{
		'name': 'ReTest Recheck implicit check',
		'tag': 'retest_implicit',
		'root_dir': '/home/david/IdeaProjects/petclinic-test-suite',
		'mvn_opts': '-Dtest="recheck.implicit.**" -Djava.awt.headless=true'
	}
]

surefire_reports_subdir = 'target/surefire-reports'     # relative location of surefire reports
#  #


# DO NOT CHANGE THESE LINES #
source_paths = [join(app_root_dir, src_path) for src_path in source_paths]
mutants_dir = join(app_root_dir, mutants_dir)
#  #
