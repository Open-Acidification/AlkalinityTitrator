"""
The file for the CalibratePh class
"""

from titration import constants
from titration.ui_state.ui_state import UIState
from titration.ui_state.user_value.buffer_ph import BufferPH


class CalibratePh(UIState):
    """
    This is a class for the CalibratePh state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): the values dictionary is used to hold the buffer's measured voltage and actual pH
    """

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                Any -> Go to UserValue to set theBuffer PH
            Substate 2:
                Any -> To continue after putting sensor in reference solution
            Substate 3:
                Any -> Return to previous state

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self._set_next_state(BufferPH(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 2:
            self.titrator.buffer_measured_volts = self.titrator.ph_probe.read_raw_pH()
            self.substate += 1

        elif self.substate == 3:
            constants.PH_REF_VOLTAGE = self.titrator.buffer_measured_volts
            constants.PH_REF_PH = self.titrator.buffer_nominal_ph
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("Enter buffer pH", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Put sensor in buffer", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("to record value", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Recorded pH and volts:", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.buffer_nominal_ph:>2.5f} pH, {self.titrator.buffer_measured_volts:>3.4f} V",
                line=2,
            )
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)
