"""
The file for the PrimePump class
"""

from titration import constants
from titration.ui_state.ui_state import UIState


class PrimePump(UIState):
    """
    This is a class for the PrimePump state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                1 -> Fill Pump
                2 -> Empty Pump
                4 -> Return to Main Menu
            Substate 2, 3:
                Any -> Substate 1
            D -> Return to main menu

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            if key == constants.KEY_1:
                self.titrator.pump.pump_volume_in(1.1)
                self.substate = 2
            elif key == constants.KEY_2:
                self.titrator.pump.pump_volume_out(1.1)
                self.substate = 3
            elif key in (constants.KEY_4):
                self._set_next_state(self.previous_state, True)

        else:
            self.substate = 1

        if key == constants.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1. Fill Pump", line=1)
            self.titrator.lcd.print("2. Empty Pump", line=2)
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("4. Return", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Filling Pump", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Emptying Pump", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)
