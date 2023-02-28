"""
The file for the PHRefpH class
"""
from titration import constants
from titration.ui_state.user_value.user_value import UserValue


class PHRefpH(UserValue):
    """
    This is a class for the PHRefpH state of the titrator
    """

    def save_value(self, value):
        """
        The function to save the pH probe's reference pH
        """
        if value not in ("", "."):
            constants.PH_REF_PH = float(value)

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "pH Ref pH:"
