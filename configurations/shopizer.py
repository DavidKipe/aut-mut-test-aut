
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

# mutants_to_skip = []    # list of ids of the mutants to be skipped

# mutants to be skipped in Recheck implicit computation
# mutations filter "max3", mutants killed by retest explicit or with BUILD_ERRORS
mutants_to_skip = [3, 14, 15, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 46, 47, 48, 49, 50, 52, 53, 54, 55, 57, 58, 59, 62, 64, 65, 67, 68, 74, 77, 78, 80, 81, 85, 86, 91, 93, 94, 96, 101,
                   102, 106, 110, 113, 117, 129, 130, 170, 178, 193, 195, 196, 197, 198, 203, 213, 223, 225, 226, 227, 229, 230, 232, 234, 235, 237, 238, 242, 265, 273, 279, 298, 395, 403, 404, 413, 417, 425, 431, 439, 440, 474, 479, 544, 597,
                   611, 666, 695, 708, 710, 711, 730, 826, 885, 894, 961, 962, 963, 965, 966, 968, 969, 974, 983, 984, 985, 987, 989, 1002, 1011, 1021, 1022, 1023, 1027, 1030, 1036, 1037, 1039, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1049,
                   1052, 1054, 1057, 1059, 1076, 1082, 1085, 1086, 1088, 1093, 1096, 1106, 1108, 1115, 1123, 1134, 1139, 1140, 1141, 1143, 1144, 1145, 1148, 1149, 1150, 1151, 1152, 1153, 1158, 1160, 1163, 1164, 1169, 1179, 1180, 1182, 1183, 1184,
                   1193, 1207, 1208, 1209, 1211, 1214, 1231, 1234, 1253, 1260, 1264, 1265, 1267, 1268, 1272, 1273, 1321, 1328, 1334, 1341, 1350, 1351, 1355, 1374, 1394, 1399, 1518, 1537, 1546, 1553, 1554, 1556, 1561, 1563, 1573, 1582, 1584, 1585,
                   1587, 1590, 1592, 1593, 1594, 1595, 1596, 1597, 1598, 1600, 1602, 1612, 1614, 1617, 1624, 1644, 1647, 1661, 1662, 1663, 1665, 1666, 1673, 1674, 1677, 1686, 1695, 1696, 1698, 1699, 1712, 1715, 1720, 1727, 1729, 1730, 1731, 1732,
                   1733, 1735, 1737, 1740, 1741, 1743, 1744, 1745, 1747, 1749, 1751, 1754, 1755, 1756, 1758, 1759, 1760, 1761, 1764, 1769, 1775, 1777, 1789, 1791, 1792, 1793, 1796, 1798, 1800, 1801, 1844, 1846, 1851, 1852, 1853, 1854, 1876, 1877,
                   1879, 1881]
#  #

# Information about test suites #
# all fields are mandatory
# name: full name of the test suite
# tag: short name of the test suite
# root_dir: root directory of the test suite project
# mvn_opts: options to insert in the Maven command
#   command = 'mvn {mvn_opts} surefire-report:report test -B'
test_suites = [
	# {
	# 	'name': 'Selenium assertions',
	# 	'tag': 'assertions',
	# 	'root_dir': '/home/david/IdeaProjects/shopizer-test-suite',
	# 	'mvn_opts': '-Dtest="assertions.**" -Djava.awt.headless=true'
	# },
	# {
	# 	'name': 'ReTest Recheck explicit check',
	# 	'tag': 'retest_explicit',
	# 	'root_dir': '/home/david/IdeaProjects/shopizer-test-suite',
	# 	'mvn_opts': '-Dtest="recheck.explicit.**" -Djava.awt.headless=true'
	# },
	{
		'name': 'ReTest Recheck implicit check',
		'tag': 'retest_implicit',
		'root_dir': '/home/david/IdeaProjects/shopizer-test-suite',
		'mvn_opts': [
			'-Dtest="recheck.implicit.A_RegistrationTests#testRegisterMemberWithEmptyLastName" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.A_RegistrationTests#testRegisterMemberWithEmptyFirstName" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.A_RegistrationTests#testRegisterMemberWithEmptyEmail" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.A_RegistrationTests#testRegisterMemberWithEmptyPassword" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.A_RegistrationTests#testRegisterMemberWithEmptyRepeatPassword" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.A_RegistrationTests#testRegisterWithPasswordMismatch" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.A_RegistrationTests#testRegisterMemberWithValidData" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.A_RegistrationTests#testRegisterDuplicateMember" -Djava.awt.headless=true',

			'-Dtest="recheck.implicit.B_LoginTests#testLoginWithIncorrectEmail" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.B_LoginTests#testLoginWithIncorrectPassword" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.B_LoginTests#testLoginWithEmptyEmail" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.B_LoginTests#testLoginWithEmptyPassword" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.B_LoginTests#testLoginWithValidData" -Djava.awt.headless=true',

			'-Dtest="recheck.implicit.C_ItemsTests#testDisplayItems" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.C_ItemsTests#testDisplayDetailsOfAnItem" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.C_ItemsTests#testFilterItemsByCollection" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.C_ItemsTests#testSortItemsByName" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.C_ItemsTests#testSortItemsByPrice" -Djava.awt.headless=true',

			'-Dtest="recheck.implicit.D_ShoppingCartTests#testAddOneItemToCart" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.D_ShoppingCartTests#testAddTwoDifferentItemsToCart" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.D_ShoppingCartTests#testIncrementQuantityOfAnItemInTheCart" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.D_ShoppingCartTests#testRemoveAnItemFromTheCart" -Djava.awt.headless=true',

			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderWithoutAccount" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderStorePickUp" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderDifferentShippingAddress" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderWithEmptyFirstName" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderWithEmptyLastName" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderWithEmptyAddress" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderWithEmptyCity" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderWithEmptyPostalCode" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderWithEmptyEmail" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderWithEmptyPhoneNumber" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderDifferentShippingAddressWithEmptyFirstName" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderDifferentShippingAddressWithEmptyLastName" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderDifferentShippingAddressWithEmptyAddress" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderDifferentShippingAddressWithEmptyCity" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderDifferentShippingAddressWithEmptyPostalCode" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderLoggedIn" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.E_CheckoutTests#testCheckoutOrderCreatingAccountEmptyPassword" -Djava.awt.headless=true',

			'-Dtest="recheck.implicit.F_SubmitOrderTests#testSubmitOrder" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.F_SubmitOrderTests#testSubmitOrderWithInvalidEmail" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.F_SubmitOrderTests#testSubmitOrderLoggedIn" -Djava.awt.headless=true',

			'-Dtest="recheck.implicit.G_ItemReviewTests#testReviewAnItemWithEmptyOpinion" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.G_ItemReviewTests#testReviewAnItemWithEmptyRating" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.G_ItemReviewTests#testReviewAnItem" -Djava.awt.headless=true',

			'-Dtest="recheck.implicit.H_AccountManagementTests#testLogout" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.H_AccountManagementTests#testChangePasswordWithIncorrectPassword" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.H_AccountManagementTests#testChangePasswordWithPasswordMismatch" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.H_AccountManagementTests#testChangePasswordWithShortPassword" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.H_AccountManagementTests#testCorrectnessBillingAddresses" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.H_AccountManagementTests#testEditBillingAddress" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.H_AccountManagementTests#testEditShippingAddress" -Djava.awt.headless=true',
			'-Dtest="recheck.implicit.H_AccountManagementTests#testChangePassword" -Djava.awt.headless=true'
		]
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
