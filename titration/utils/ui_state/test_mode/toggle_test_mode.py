"""
The file for the ToggleTestMode class
"""
from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, constants


class ToggleTestMode(UIState):
    """
    This is a class for the ToggleTestMode state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the new_volume
    """

    def __init__(self, titrator, previous_state):
        """
        The constructor for the ToggleTestMode class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last visited state
        """
        super().__init__(titrator, previous_state)
        self.values = {"new_volume": 0}

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
        lcd_interface.lcd_clear()
        lcd_interface.lcd_out("Testing: {}".format(constants.IS_TEST), line=1)
        lcd_interface.lcd_out("", line=2)
        lcd_interface.lcd_out("Press any to cont.", line=3)
        lcd_interface.lcd_out("", line=4)
