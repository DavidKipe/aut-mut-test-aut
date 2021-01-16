
# change this import to load the configuration you want to use
# make sure the import format is "from configurations.{name} import *"
from configurations.petclinic import *


logged = False
if not logged:
	print("Running with configuration:", config_name)
	logged = True
