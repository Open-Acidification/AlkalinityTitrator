"""
The file for the AnalogIn class
"""


class AnalogIn:
    """
    The mock class for the analog peripheral in
    """

    def __init__(self, ads, p_0, p_1):
        """
        The constructor function for the AnalogIn class
        """
        self.ads = ads
        self.p_0 = p_0
        self.p_1 = p_1

        self.voltage = 0
