"""
The file for the FillPump class
"""

from titration.ui_state.ui_state import UIState


class FillPump(UIState):
    """
    The class for the FillPump UI state. This is used to fill the pump before a titration
    """

    def __init__(self, titrator, previous_state=None):
        """
        The constructor for the FillPump class.
        Starts filling the pump once this state is entered.
        """
        super().__init__(titrator, previous_state)

        # 1.1 is the max pump capacity
        self.titrator.pump.pump_volume_in(1.1)

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Any -> Return to PrimePump menu

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("Filling Pump", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)
