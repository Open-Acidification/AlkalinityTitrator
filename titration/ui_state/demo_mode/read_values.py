"""
The file for the ReadValues class
"""

from titration import constants
from titration.ui_state.ui_state import UIState


class ReadValues(UIState):
    """
    This is a class for the ReadValues state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the temp, res, pH, volts, numVals, timeStep
    """

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                Any -> Next Page of Values
            Substate 2:
                Any -> Return to Demo Mode Menu
            D -> Return to Demo Mode Menu

        Parameters:
            key (char): the keypad input is used to move to the next substate
        """
        if self.substate == 1:
            self.substate = 2

        elif self.substate == 2:
            self._set_next_state(self.previous_state, True)

        if key == constants.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print(
                f"pH: {self.titrator.ph_probe.get_voltage():>4.5f} pH", line=1
            )
            self.titrator.lcd.print(
                f"pH V: {(self.titrator.ph_probe.get_voltage() * 1000):>3.4f} mV",
                line=2,
            )
            self.titrator.lcd.print(
                f"Gain: {self.titrator.ph_probe.get_gain()}", line=3
            )
            self.titrator.lcd.print(
                f"Volume: {self.titrator.pump.get_volume_in_pump()} ml", line=4
            )

        elif self.substate == 2:
            self.titrator.lcd.print(
                f"Temp: {self.titrator.temp_probe_one.get_temperature():>4.3f} C",
                line=1,
            )
            self.titrator.lcd.print(
                f"Res:  {self.titrator.temp_probe_one.get_resistance():>4.3f} Ohms",
                line=2,
            )
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)
