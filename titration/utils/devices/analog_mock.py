"""
The file for the AnalogIn class
"""


class AnalogIn:
    """
    The mock class for the analog peripheral in
    """

    def __init__(self, ads, p0, p1):
        """
        The constructor function for the AnalogIn class
        """
        self.ads = ads
        self.p0 = p0
        self.p1 = p1

        self.voltage = 0
