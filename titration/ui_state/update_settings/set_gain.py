"""
The file for the SetGain class
"""

from titration import constants
from titration.ui_state.ui_state import UIState


class SetGain(UIState):
    """
    The class for the SetGain UI State
    """

    def __init__(self, titrator, previous_state=None):
        """
        The constructor function the SetGain class.
        user_choice holds the value of the user choice to be displayed.
        """
        super().__init__(titrator, previous_state)
        self.user_choice = "1"

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                1 -> Set Gain to 2/3
                2 -> Set Gain to 1
                3 -> Set Gain to 2
                4 -> Go to substate 2
            Substate 2:
                1 -> Set Gain to 4
                2 -> Set Gain to 8
                3 -> Set Gain to 16
                4 -> Go to substate 1
            Substate 3:
                Any -> Return to update settings menu
            D -> Return to update settings menu

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            if key == constants.KEY_1:
                self.user_choice = "2/3"
                self.titrator.ph_probe.set_gain(2 / 3)
                self.substate = 3
            elif key == constants.KEY_2:
                self.user_choice = "1"
                self.titrator.ph_probe.set_gain(1)
                self.substate = 3
            elif key == constants.KEY_3:
                self.user_choice = "2"
                self.titrator.ph_probe.set_gain(2)
                self.substate = 3
            elif key == constants.KEY_4:
                self.substate = 2

        elif self.substate == 2:
            if key == constants.KEY_1:
                self.user_choice = "4"
                self.titrator.ph_probe.set_gain(4)
                self.substate = 3
            elif key == constants.KEY_2:
                self.user_choice = "8"
                self.titrator.ph_probe.set_gain(8)
                self.substate = 3
            elif key == constants.KEY_3:
                self.user_choice = "16"
                self.titrator.ph_probe.set_gain(16)
                self.substate = 3
            elif key == constants.KEY_4:
                self.substate = 1

        elif self.substate == 3:
            self._set_next_state(self.previous_state, True)

        if key == constants.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: 2/3", line=1)
            self.titrator.lcd.print("2: 1", line=2)
            self.titrator.lcd.print("3: 2", line=3)
            self.titrator.lcd.print("4: Page 2", line=4)

        if self.substate == 2:
            self.titrator.lcd.print("1: 4", line=1)
            self.titrator.lcd.print("2: 8", line=2)
            self.titrator.lcd.print("3: 16", line=3)
            self.titrator.lcd.print("4: Page 1", line=4)

        if self.substate == 3:
            self.titrator.lcd.print("pH Probe", line=1)
            self.titrator.lcd.print("Gain Set To " + self.user_choice, line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)
