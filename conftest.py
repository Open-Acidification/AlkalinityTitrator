"""
The file to configure testing imports
"""
from titration import mock_config

# Set MOCK_ENABLED to true to avoid importing Raspberry Pi
# dependent libraries.
mock_config.MOCK_ENABLED = True
