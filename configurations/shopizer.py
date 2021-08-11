
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

mutants_to_skip = []    # list of ids of the mutants to be skipped
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
