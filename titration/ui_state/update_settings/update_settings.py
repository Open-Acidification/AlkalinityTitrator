"""
The file to for the UpdateSetting class
"""

from titration import constants
from titration.ui_state.ui_state import UIState
from titration.ui_state.update_settings.set_gain import SetGain


class UpdateSettings(UIState):
    """
    This is a class for the UpdateSettings state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            if key == constants.KEY_1:
                self._set_next_state(SetGain(self.titrator, self), True)
            elif key == constants.KEY_4:
                self._set_next_state(self.previous_state, True)

        if key == constants.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Set pH Probe Gain", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("4: Return", line=4)
