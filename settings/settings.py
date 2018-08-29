import sys
import pickle

#from screen.utils import screenshot

# Template matching tolerance
# if no matches are found under this threshold,
# consider it not on the screen
MAX_DISTANCE = 0.2 # [0, 1]

# state directory name inside robot directory
STATE_DIR = "state"

TEMPLATE_DIR = "templates"

# state filename inside robot directory
STATEFILENAME = "state.pickle"

# Run without saving or reading state
STATELESS = False

# Local environment flag, set in robot's local_settings, if set
LOCAL = False

# Logging format
# LOGGING_FORMAT = '%(asctime)s - %(filename)s:%(lineno)d\n%(levelname)s: %(message)s\n'
LOGGING_FORMAT = "%(message)s"

# Set in local_settings
ROBOTS_DIRECTORY = ""

# Fake everything
FAKE = False

VERBOSE = False

# load local_settings if exists
try:
    from .local_settings import *
except ImportError:
    pass
