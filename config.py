
## configurations ##

pit_xml_report_filename = 'resources/mutations.xml'
mut_infos_json_filename = 'resources/mutations.json'

app_rootdir = '/home/david/IdeaProjects/spring-petclinic-mutation/'    # root directory of the application
testsuite_1_rootdir = '/home/david/IdeaProjects/petclinic-test-suite-selenium/'
testsuite_2_rootdir = '/home/david/IdeaProjects/petclinic-test-suite-recheck/'

backup_ext = '.bak'						# this string will be appened to the original filename
orig_line_tag = ' // original line'		# this string will be appened to the original commented line
mutate_line_tag = ' // mutated line'    # this string will be appened to the mutated line
indentation_format = '\t'				# could be either '\t' (tab) or ' ' (*one* space)

# derived
source_rootdir = app_rootdir + 'src/main/java/' # root directory of the source code
mutants_dir = app_rootdir + 'mutants/'          # directory of the mutant files inside the root app dir
#

run_app_command = 'mvn spring-javaformat:apply spring-boot:run -B'
app_ready_stdout_signal = "Started PetClinicApplication in"

run_testsuite_1_command = 'mvn test -B'
run_testsuite_2_command = 'mvn test -B'

##  ##
