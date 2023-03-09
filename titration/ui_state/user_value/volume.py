"""
The file for the Volume class
"""
from titration.ui_state.user_value.user_value import UserValue


class Volume(UserValue):
    """
    This is a class for the Volume state of the titrator
    """

    def save_value(self):
        """
        The function to save the titrator's Volume
        """
        self.titrator.volume = self.value

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Volume:"
