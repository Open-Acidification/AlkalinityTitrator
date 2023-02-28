"""
The file for the PHRefVoltage class
"""
from titration import constants
from titration.ui_state.user_value.user_value import UserValue


class PHRefVoltage(UserValue):
    """
    This is a class for the PHRefVoltage state of the titrator
    """

    def save_value(self, value):
        """
        The function to save the pH probe's reference voltage
        """
        constants.PH_REF_VOLTAGE = float(value)

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "pH Ref Voltage:"
