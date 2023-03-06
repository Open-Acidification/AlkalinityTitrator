"""
The file for the PumpVolume class
"""
from titration.ui_state.user_value.user_value import UserValue


class PumpVolume(UserValue):
    """
    This is a class for the PumpVolume state of the titrator
    """

    def save_value(self, value):
        """
        The function to save the titrator's pump volume
        """
        if value not in ("", "."):
            self.titrator.pump_volume = float(value)

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Volume in pump:"
