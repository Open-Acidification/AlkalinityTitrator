"""
The file to test the logger functionality
"""
from unittest import TestCase

from titration.titrator import Titrator


class TestLogger(TestCase):
    """
    Test logger class for testing the use of the titrator's logger
    """

    def test_logging(self):
        """
        Testing the output of the logger file
        """
        with self.assertLogs() as captured:
            Titrator()
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(), "\nNEW TITRATION\n")
