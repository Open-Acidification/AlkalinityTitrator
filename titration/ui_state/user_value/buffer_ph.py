"""
The file for the BufferPH class
"""
from titration.ui_state.user_value.user_value import UserValue


class BufferPH(UserValue):
    """
    This is a class for the BufferPH state of the titrator
    """

    def save_value(self, value):
        """
        The function to save the titrator's buffer pH
        """
        self.titrator.nominal_buffer_ph = value

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Enter buffer pH:"
