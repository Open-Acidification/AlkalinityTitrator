"""
The file for the PrimePump class
"""
from titration.utils.ui_state.ui_state import UIState


class PrimePump(UIState):
    """
    This is a class for the PrimePump state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to the users amount of pumps
    """

    def __init__(self, titrator, previous_state):
        """
        The constructor for the PrimePump class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last visited state
        """
        super().__init__(titrator, previous_state)
        self.values = {"selection": 0}

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                Any -> Enter a number of pumps to occur
            Substate 2:
                Any -> Enter how many more pumps you would like to occur
                0 -> Return to previous state

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self.values["selection"] = key
            self.substate += 1

        elif self.substate == 2:
            self.values["selection"] = key

        if self.values["selection"] == "0":
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("How many pumps?", line=1)
            self.titrator.lcd.print("Choose a number", line=2)
            self.titrator.lcd.print("Choose 0 to return", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("How many more?", line=1)
            self.titrator.lcd.print("Choose a number", line=2)
            self.titrator.lcd.print("Choose 0 to return", line=3)
            self.titrator.lcd.print("", line=4)
