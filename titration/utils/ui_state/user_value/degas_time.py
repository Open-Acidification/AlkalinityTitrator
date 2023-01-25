"""
The file for the DegasTime class
"""

from titration.utils.ui_state.user_value.user_value import UserValue
from titration.utils import lcd_interface


class DegasTime(UserValue):
    """
    This is a class for the DegasTime state of the photometer

    Attributes:
        photometer (Photometer object): the photometer is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        string (string): the string is used to hold the user input
    """

    def save_value(self):
        """
        The function to save the titrator's degas time
        """
        self.titrator.degas_time = self.string

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        lcd_interface.lcd_out("Degas time (s):", line=1)
        super().loop()
