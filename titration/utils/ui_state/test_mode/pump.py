"""
The file for the Pump class
"""
from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, constants
from titration.utils.ui_state.user_value.user_value import UserValue


class Pump(UIState):
    """
    This is a class for the Pump state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last state visited in the state machine
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictonary to hold the probe direction
    """

    def __init__(self, titrator, previous_state):
        """
        The constructor for the Pump class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last state visited in the state machine
        """
        super().__init__(titrator, previous_state)
        self.values = {"p_direction": 0}

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                Any -> Go to UserValue state to set volume
            Substate 2:
                0 or 1 -> Set the probe direction
            Substate 3:
                Any -> Return to previous state

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self._set_next_state(UserValue(self.titrator, self, "Volume: "), True)
            self.substate += 1

        elif self.substate == 2:
            if key == constants.KEY_0 or key == constants.KEY_1:
                self.values["p_direction"] = key
                self.substate += 1

        elif self.substate == 3:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Set Volume", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.substate == 2:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("In/Out (0/1):", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.substate == 3:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Pumping volume", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)
