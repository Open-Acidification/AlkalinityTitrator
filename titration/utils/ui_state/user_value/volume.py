"""
The file for the Volume class
"""

from AlkalinityTitrator.titration.utils.ui_state.user_value.user_value import UserValue


class Volume(UserValue):
    """
    This is a class for the Volume state of the titrator
    """

    def save_value(self, value):
        """
        The function to save the titrator's Volume
        """
        self.titrator.volume = value

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Volume:"
