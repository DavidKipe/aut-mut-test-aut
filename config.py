from os.path import join

# change this import to load the configuration you want to use
# make sure the import format is "from configurations.{name} import *"
from configurations.shopizer import *


# DO NOT CHANGE THESE LINES #

logged = False
if not logged:
	print(f"Running with configuration: {config_name}\n")
	logged = True

source_paths = [join(app_root_dir, src_path) for src_path in source_paths]
mutants_dir = join(app_root_dir, mutants_dir)

#  #
