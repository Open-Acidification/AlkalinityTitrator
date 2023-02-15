"""
The file for the ReferenceTemperature class
"""

from AlkalinityTitrator.titration.utils.ui_state.user_value.user_value import UserValue


class ReferenceTemperature(UserValue):
    """
    This is a class for the ReferenceTemperature state of the titrator
    """

    def save_value(self, value):
        """
        The function to save the titrator's reference temperature
        """
        self.titrator.reference_temperature = value

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Ref solution temp:"
