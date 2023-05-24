"""
The file for the Volume class
"""
from titration.ui_state.user_value.user_value import UserValue


class VolumeToMove(UserValue):
    """
    This is a class for the Volume state of the titrator
    """

    def save_value(self):
        """
        The function to save the volume the pump should move.
        """
        self.titrator.volume_to_move = self.value

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        return "Volume to move:"
