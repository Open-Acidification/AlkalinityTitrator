"""
The file for the CalibrateTemp class
"""
from titration import constants
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
            # self.titrator.temp_probe.calibrate_temperature()
            self.substate = 3

        elif self.substate == 3:
            # self.titrator.temp_probe.__init__()
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("Set Ref solution", line=1)
            self.titrator.lcd.print("temp", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Put probe in sol", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to", line=3)
            self.titrator.lcd.print("record value", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Recorded temp:", line=1)
            self.titrator.lcd.print(f"{self.titrator.measured_temperature:0.3f}", line=2)
            self.titrator.lcd.print(f"{constants.TEMP_REF_RESISTANCE}", line=3)
            self.titrator.lcd.print("", line=4)

    def calibrate_temperature(self):
        """
        Calculates the expected resistance. Used for calibrating temperature probe.
        https://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf
        """

        A = 0.0039083
        B = -0.000000578
        C = -0.000000000004183

        temp = self.titrator.reference_temperature

        if temp >= 0:
            self.titrator.reference_resistance = constants.TEMP_NOMINAL_RESISTANCE * (1 + A * temp + B * temp ** 2)
        else:
            self.titrator.reference_resistance = constants.TEMP_NOMINAL_RESISTANCE * (1 + A * temp + B * temp ** 2 + C * (temp - 100) * temp ** 3)

        self.titrator.measured_temperature = self.titrator.temperature_probe.get_temperature()
        self.titrator.measured_resistance = self.titrator.temperature_probe.get_resistance()

        diff = self.titrator.reference_resistance - self.titrator.temperature_probe.get_resistance()
        constants.TEMP_REF_RESISTANCE = float(constants.TEMP_REF_RESISTANCE + diff * constants.TEMP_REF_RESISTANCE / self.titrator.reference_temperature)
