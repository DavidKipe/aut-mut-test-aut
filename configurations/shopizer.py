
config_name = "Shopizer"

# -- configuration -- #

# Application (SUT) config #
app_root_dir = '/home/david/IdeaProjects/shopizer-mutations'    # root directory of the application

backup_ext = '.bak'						# this string will be appended to the original filename
orig_line_tag = ' // original line'		# this string will be appended to the original commented line
mutate_line_tag = ' // mutated line'    # this string will be appended to the mutated line
indentation_format = '\t'				# could be either '\t' (tab) or ' ' (*one* space)

source_paths = ['sm-core/src/main/java', 'sm-core-model/src/main/java', 'sm-core-modules/src/main/java', 'sm-shop/src/main/java', 'sm-shop-model/src/main/java']  # directories of the source code in the app root dir

mutants_dir = 'mutants'             # directory name where the mutated files will be saved inside the app root dir

command_path_run = 'sm-shop'    # path relative for the run command
command_app_run = 'mvn spring-boot:run -B'  # command to run application
app_ready_stdout_signal = "Started ShopApplication in"  # what the application write on stdout when is ready
app_shutdown_stdout_signal = "Shutdown completed"       # what the application write on shutdown completed

command_app_reset = 'git checkout -- sm-shop/SALESMANAGER.h2.db sm-shop/SALESMANAGER.trace.db sm-shop/files/store/DownlaodRepository.dat'     # this command will be run to reset the app to the initial state (optional)
#  #

# Mutation info # (path relative to root of this tool)
input_pit_xml_report_filename = 'resources/shopizer_mutations_coverage_sorted.xml'     # input file from PIT
output_mut_infos_json_filename = 'resources/shopizer_mutations_coverage_sorted.json'    # generated file by this tool

# mutants survived
survived = [4, 6, 8, 9, 10, 13, 16, 17, 20, 44, 45, 51, 56, 60, 61, 63, 66, 69, 73, 83, 95, 97, 105, 112, 116, 119, 120, 121, 122, 123, 124, 125, 126, 128, 132, 133, 134, 135, 159, 185, 188, 190, 199, 200, 201, 202, 206, 212, 216, 218, 231, 233, 236,
           250, 320, 378, 382, 383, 385, 399, 402, 411, 434, 441, 455, 524, 532, 534, 536, 551, 553, 567, 609, 626, 628, 630, 646, 675, 700, 701, 706, 712, 715, 732, 733, 736, 739, 740, 752, 779, 781, 801, 808, 809, 816, 819, 835, 840, 849, 852,
           856, 858, 879, 882, 884, 886, 913, 938, 943, 956, 967, 980, 986, 1008, 1017, 1018, 1024, 1025, 1026, 1029, 1048, 1050, 1053, 1056, 1058, 1063, 1071, 1105, 1107, 1109, 1110, 1111, 1118, 1137, 1138, 1155, 1156, 1159, 1161, 1166, 1168, 1175,
           1199, 1213, 1236, 1241, 1244, 1246, 1255, 1258, 1269, 1270, 1286, 1306, 1312, 1316, 1317, 1319, 1335, 1336, 1337, 1338, 1340, 1370, 1397, 1427, 1447, 1481, 1498, 1534, 1545, 1557, 1620, 1625, 1626, 1627, 1628, 1633, 1643, 1645, 1646,
           1650, 1651, 1669, 1675, 1676, 1680, 1682, 1684, 1688, 1691, 1697, 1704, 1707, 1709, 1710, 1711, 1713, 1714, 1716, 1717, 1718, 1725, 1736, 1738, 1746, 1753, 1767, 1780, 1795, 1802, 1803, 1804, 1805, 1806, 1809, 1811, 1812, 1822, 1831,
           1832, 1837, 1838, 1840, 1842, 1843, 1845, 1847, 1848, 1849, 1850, 1855, 1860, 1861, 1869, 1871, 1872, 1875, 1878, 1880]

build_errors = [14, 18, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 49, 50, 53, 54, 55, 57, 59, 64, 67, 68, 225, 1143, 1145, 1152, 1158, 1182, 1183, 1594, 1715, 1758, 1844, 1846, 1876]

mutants_to_skip = survived + build_errors  # list of ids of the mutants to be skipped
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
		'root_dir': '/home/david/IdeaProjects/shopizer-test-suite',
		'mvn_opts': '-Dtest="assertions.**" -Djava.awt.headless=true'
	},
	{
		'name': 'ReTest Recheck explicit check',
		'tag': 'retest_explicit',
		'root_dir': '/home/david/IdeaProjects/shopizer-test-suite',
		'mvn_opts': '-Dtest="recheck.explicit.**" -Djava.awt.headless=true'
	},
	# {
	# 	'name': 'ReTest Recheck implicit check',
	# 	'tag': 'retest_implicit',
	# 	'root_dir': '/home/david/IdeaProjects/shopizer-test-suite',
	# 	'mvn_opts': '-Dtest="recheck.implicit.**" -Djava.awt.headless=true'
	# }
]

surefire_reports_subdir = 'target/surefire-reports'     # relative location of surefire reports
#  #
