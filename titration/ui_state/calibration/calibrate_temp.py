"""
The file for the CalibrateTemp class
"""

from titration.ui_state.ui_state import UIState
from titration.ui_state.user_value.reference_temperature import (
    ReferenceTemperature,
)


class CalibrateTemp(UIState):
    """
    This is a class for the CalibrateTemp state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

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
            self.substate = 2

        elif self.substate == 2:
            self.titrator.temp_probe.calibrate(self.titrator.reference_temperature)
            self.substate = 3

        elif self.substate == 3:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("Set ref solution", line=1)
            self.titrator.lcd.print("temp", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Put probe in sol", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("to record value", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Recorded temp:", line=1)
            self.titrator.lcd.print(
                f"{(self.titrator.temp_probe.get_temperature()):0.3f}", line=2
            )
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe.get_resistance()}", line=3
            )
            self.titrator.lcd.print("", line=4)
