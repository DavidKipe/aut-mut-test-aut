
## configurations ##

pit_xml_report_filename = 'mutations.xml'
mut_infos_json_filename = 'mutations.json'

app_rootdir = '/home/david/IdeaProjects/spring-petclinic-mutation/'    # root directory of the application
backup_ext = '.bak'						# this string will be appened to the original filename
orig_line_tag = ' // original line'		# this string will be appened to the original commented line
mutate_line_tag = ' // mutated line'    # this string will be appened to the mutated line
identation_format = '\t'				# could be either '\t' (tab) or ' ' (*one* space)

# derived
source_rootdir = app_rootdir + 'src/main/java/' # root directory of the source code
mutants_dir = app_rootdir + 'mutants/'          # directory of the mutant files
#

run_app_command = 'mvn spring-javaformat:apply spring-boot:run'
run_test_suite_command = ''

##  ##
