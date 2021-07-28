## Configuration

Here are listed the variables needed to configure the application. The configuration file is a Python source code file, thus the configuration is directly in the source code.

`config_name`: This is the name of this configuration. It is just the name shown at the start of the application.

#### Application Under Test

`app_root_dir`: This is the root directory of the Application Under Test

`source_paths`: List of relative paths of the source code directories inside the root directory

`command_path_run`: The relative path for the run command

`command_app_run`: The Maven command used to run the Application Under Test

`app_ready_stdout_signal`: A string that the Application Under Test prints when it is ready

`app_shutdown_stdout_signal`: A string that the Application Under Test prints when the shutdown is completed

`command_app_reset`: (optional) This command will be run to reset the app to the initial state

`mutants_dir`: Directory name where the mutated files will be saved as backup inside the app root dir

`backup_ext`: This string will be appended to the original filename. Must be an extension starting with a dot.

`orig_line_tag`: This string will be appended to the original commented line

`mutate_line_tag`: This string will be appended to the mutated line. Must be a comment.

`indentation_format`: Binary value, tabulations or spaces. It could be either '\t' (tab) or ' ' (one space)

#### Mutations information

`input_pit_xml_report_filename`: Input file with the information from Pitest tool in XML format

`output_mut_infos_json_filename`: Name of the JSON file generated in output

`mutants_to_skip`: List of IDs of the mutants that must be skipped by the application

#### Test suite

`test_suites`: List of "test suite" objects that define the test suite configuration

Fields description of the test suite configuration

`name`: full name of the test suite

`tag`: short name of the test suite

`root_dir`: root directory of the test suite project

`mvn_opts`: options to insert in the Maven command

The command format is `mvn {mvn_opts} surefire-report:report test -B`

Example
```
test_suites = [
	{
		'name': 'Selenium assertions',
		'tag': 'assertions',
		'root_dir': '/home/path/to/test-suite',
		'mvn_opts': '-Dtest="assertions.**" -Djava.awt.headless=true'
	},
	{
		'name': 'Selenium assertions 2',
		'tag': 'assertions_2',
		'root_dir': '/home/path/to/test-suite-2',
		'mvn_opts': '-Dtest="assertions.**" -Djava.awt.headless=true'
	},
	...
]
```
