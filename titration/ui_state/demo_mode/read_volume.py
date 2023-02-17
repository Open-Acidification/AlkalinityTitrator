"""
The file for the ReadVolume class
"""
from titration.ui_state.ui_state import UIState


class ReadVolume(UIState):
    """
    This is a class for the ReadVolume state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the new_volume
    """

    def handle_key(self, key):
        """
        The function to handle keypad input. Any input will return you to the previous state

        Parameters:
            key (char): the keypad input is used to move to the next state
        """
        self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        self.titrator.lcd.clear()
        self.titrator.lcd.print("Pump Vol: ", line=1)
        self.titrator.lcd.print(
            f"{self.titrator.pump.get_volume_in_pump():1.2f}",
            style="center",
            line=2,
        )
        self.titrator.lcd.print("Press any to cont.", line=3)
        self.titrator.lcd.print("", line=4)
