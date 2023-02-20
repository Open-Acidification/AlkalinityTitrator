"""
The file to configure testing imports
"""
from titration import constants

# Set IS_TEST to true to avoid importing Raspberry Pi
# dependent libraries.
constants.IS_TEST = True
