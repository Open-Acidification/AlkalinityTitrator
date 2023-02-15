"""
The file for the DegasTime class
"""

from AlkalinityTitrator.titration.utils.ui_state.user_value.user_value import UserValue


class DegasTime(UserValue):
    """
    This is a class for the DegasTime state of the titrator
    """

    def save_value(self, value):
        """
        The function to save the titrator's degas time
        """
        self.titrator.degas_time = value

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Degas time (s):"
