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
                Any -> Go to UserValue to set the reference solution temperature for Probe 1
            Substate 2:
                Any -> Continue after putting Probe 1 in reference solution
            Substate 3:
                Any -> Continue after Probe 1's temperature has been displayed
            Substate 4:
                Any -> Go to UserValue to set the reference solution temperature for Probe 2
            Substate 5:
                Any -> Continue after putting Probe 2 in reference solution
            Substate 6:
                Any -> Continue after Probe 2's temperature has been displayed

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self._set_next_state(ReferenceTemperature(self.titrator, self), True)
            self.substate = 2

        elif self.substate == 2:
            self.titrator.temp_probe_one.calibrate(self.titrator.reference_temperature)
            self.substate = 3

        elif self.substate == 3:
            self.substate = 4

        elif self.substate == 4:
            self._set_next_state(ReferenceTemperature(self.titrator, self), True)
            self.substate = 5

        elif self.substate == 5:
            self.titrator.temp_probe_two.calibrate(self.titrator.reference_temperature)
            self.substate = 6

        elif self.substate == 6:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("Set Probe 1", line=1)
            self.titrator.lcd.print("Reference Temp", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Put Probe 1 in Sol", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("to record value", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Recorded temp:", line=1)
            self.titrator.lcd.print(
                f"{(self.titrator.temp_probe_one.get_temperature()):0.3f}", line=2
            )
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe_one.get_resistance()}", line=3
            )
            self.titrator.lcd.print("", line=4)

        elif self.substate == 4:
            self.titrator.lcd.print("Set Probe 2", line=1)
            self.titrator.lcd.print("Reference Temp", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 5:
            self.titrator.lcd.print("Put Probe 2 in Sol", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("to record value", line=4)

        elif self.substate == 6:
            self.titrator.lcd.print("Recorded temp:", line=1)
            self.titrator.lcd.print(
                f"{(self.titrator.temp_probe_two.get_temperature()):0.3f}", line=2
            )
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe_two.get_resistance()}", line=3
            )
            self.titrator.lcd.print("", line=4)
