"""
The file for the CalibrateTemp class
"""
from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, constants
from titration.utils.ui_state.user_value.reference_temperature import (
    ReferenceTemperature,
)


class CalibrateTemp(UIState):
    """
    This is a class for the CalibrateTemp state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): the values dictionary is used to hold the actual temp, new reference resistance,
         - and expected temperature
    """

    def __init__(self, titrator, previous_state):
        """
        The constructor for the CalibrateTemp class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last visited state
        """
        super().__init__(titrator, previous_state)
        self.values = {
            "actual_temperature": 5,
            "new_ref_resistance": 5,
            "expected_temperature": 0,
        }

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                Any -> Go to UserValue to set the reference solution temp
            Substate 2:
                1 -> To continue after putting probe in reference solution
            Substate 3:
                Any -> Return to previous state

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self._set_next_state(ReferenceTemperature(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 2:
            if key == 1 or key == constants.KEY_1:
                self.substate += 1

        elif self.substate == 3:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Set Ref solution", line=1)
            lcd_interface.lcd_out("temp", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.substate == 2:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Put probe in sol", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press 1 to", line=3)
            lcd_interface.lcd_out("record value", line=4)

        elif self.substate == 3:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Recorded temp:", line=1)
            lcd_interface.lcd_out(
                "{0:0.3f}".format(self.values["actual_temperature"]), line=2
            )
            lcd_interface.lcd_out(
                "{}".format(self.values["new_ref_resistance"]), line=3
            )
            lcd_interface.lcd_out("", line=4)
