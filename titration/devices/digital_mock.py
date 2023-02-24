"""
The file to mock the DigitalInOut class
"""

# pylint: disable = invalid-name, too-few-public-methods


class DigitalInOut:
    """
    The class for the mock DigitalInOut
    """

    def __init__(self, cs):
        """
        The constructor for the DigitalInOut
        """
        self.cs = cs
