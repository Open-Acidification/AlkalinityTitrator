"""
The file for the TempRefResistance class
"""
from titration import constants
from titration.ui_state.user_value.user_value import UserValue


class TempRefResistance(UserValue):
    """
    This is a class for the TempRefResistance state of the titrator
    """

    def save_value(self, value):
        """
        The function to save the temperature probe's reference resistance
        """
        if value not in ("", "."):
            constants.TEMPERATURE_REF_RESISTANCE = float(value)

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Temp Ref Resistance:"
