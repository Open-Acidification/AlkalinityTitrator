"""
The file for the PrimePump class
"""

from titration import constants
from titration.ui_state.prime_pump.empty_pump import EmptyPump
from titration.ui_state.prime_pump.fill_pump import FillPump
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
            1 -> Fill Pump
            2 -> Empty Pump
            4 -> Return to Main Menu

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if key == constants.KEY_1:
            self._set_next_state(FillPump(self.titrator, self), True)
        elif key == constants.KEY_2:
            self._set_next_state(EmptyPump(self.titrator, self), True)
        elif key in (constants.KEY_4, constants.KEY_D):
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
