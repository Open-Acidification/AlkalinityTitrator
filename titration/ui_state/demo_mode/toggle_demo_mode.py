"""
The file for the ToggleDemoMode class
"""
from titration import constants
from titration.devices.library import Keypad
from titration.ui_state.ui_state import UIState


class ToggleDemoMode(UIState):
    """
    This is a class for the ToggleDemoMode state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the new_volume
    """

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                0 or 1 -> Set Mock Mode, Display Mode
            Substate 2:
                Any -> Return to Previous State

        Parameters:
            key (char): the keypad input is used to move to the next state
        """
        if self.substate == 1:
            if key in (Keypad.KEY_0, Keypad.KEY_1):
                constants.IS_TEST = bool(int(key))
                self.substate += 1

        elif self.substate == 2:
            self._set_next_state(self.previous_state, True)

        if key == Keypad.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("Set Mode:", line=1)
            self.titrator.lcd.print("Mock Devices: 1", line=2)
            self.titrator.lcd.print("Real Devices: 0", line=3)
            self.titrator.lcd.print("", line=4)

        if self.substate == 2:
            self.titrator.lcd.print("Mode Set To:", line=1)
            if constants.IS_TEST:
                self.titrator.lcd.print("Mock Devices", line=2)
            else:
                self.titrator.lcd.print("Real Devices", line=2)
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("", line=4)
