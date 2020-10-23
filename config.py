from os.path import join

## configurations ##

pit_xml_report_filename = 'resources/mutations.xml'
mut_infos_json_filename = 'resources/mutations.json'

app_rootdir = '/home/david/IdeaProjects/spring-petclinic-mutation'    # root directory of the application
testsuite_assertions_rootdir = '/home/david/IdeaProjects/petclinic-test-suite'
testsuite_retest_expl_rootdir = '/home/david/IdeaProjects/petclinic-test-suite'
testsuite_retest_impl_rootdir = '/home/david/IdeaProjects/petclinic-test-suite'
surefire_reports_subdir = 'target/surefire-reports'

backup_ext = '.bak'						# this string will be appened to the original filename
orig_line_tag = ' // original line'		# this string will be appened to the original commented line
mutate_line_tag = ' // mutated line'    # this string will be appened to the mutated line
indentation_format = '\t'				# could be either '\t' (tab) or ' ' (*one* space)

# derived
source_rootdir = join(app_rootdir, 'src/main/java')  # root directory of the source code
mutants_dir = join(app_rootdir, 'mutants')  # directory of the mutant files inside the root app dir
#

run_app_command = 'mvn spring-javaformat:apply spring-boot:run -B'
app_ready_stdout_signal = "Started PetClinicApplication in"

# options for Maven for each test suite
# command: 'mvn {your-options-here} surefire-report:report test -B'
mvn_testsuite_assertions_opts = '-Dtest="assertions.**" -Djava.awt.headless=true'
mvn_testsuite_retest_expl_opts = '-Dtest="recheck.explicit.**" -Djava.awt.headless=true'
mvn_testsuite_retest_impl_opts = '-Dtest="recheck.implicit.**" -Djava.awt.headless=true'

##  ##
