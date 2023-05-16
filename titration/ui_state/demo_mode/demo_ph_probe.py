"""
The file to demo the pH Probe device
"""

from titration.devices.library import Keypad
from titration.ui_state.ui_state import UIState


class DemopHProbe(UIState):
    """
    The class to demo the pH Probe
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                1 -> Get Voltage
                2 -> Get Gain
                3 -> Return to Demo Mode Menu
            Substate 2:
                Any -> Return to Substate 1
            Substate 3:
                Any -> Return to Substate 1
            D -> Return to Demo Mode Menu

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if self.substate == 1:
            if key == Keypad.KEY_1:
                self.substate = 2
            elif key == Keypad.KEY_2:
                self.substate = 3
            elif key == Keypad.KEY_3:
                self._set_next_state(self.previous_state, True)

        else:
            self.substate = 1

        if key == Keypad.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Get Voltage", line=1)
            self.titrator.lcd.print("2: Get Gain", line=2)
            self.titrator.lcd.print("3: Return", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("pH Probe Voltage:", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.ph_probe.get_voltage()} volts", line=2, style="center"
            )
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("pH Probe Gain:", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.ph_probe.get_gain()} volts", line=2, style="center"
            )
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)
