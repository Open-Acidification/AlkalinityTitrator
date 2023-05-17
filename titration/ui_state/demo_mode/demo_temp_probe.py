"""
The file to demo the temperature probe device
"""

from titration import constants
from titration.ui_state.ui_state import UIState


class DemoTempControl(UIState):
    """
    The class to demo the temperature probe device
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                1 -> Get Probe One
                2 -> Get Probe Two
                4 -> Return to Demo Mode Menu
            Substate 2-3:
                Any -> Substate 1
            D -> Return to Demo Mode Menu

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if self.substate == 1:
            if key == constants.KEY_1:
                self.substate = 2
            elif key == constants.KEY_2:
                self.substate = 3
            elif key == constants.KEY_4:
                self._set_next_state(self.previous_state, True)
        else:
            self.substate = 1

        if key == constants.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Probe One", line=1)
            self.titrator.lcd.print("2: Probe Two", line=2)
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("4: Return", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Probe One", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe_one.get_temperature()} C",
                line=2,
                style="center",
            )
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe_one.get_resistance()} Ohms",
                line=3,
                style="center",
            )
            self.titrator.lcd.print("Any key to continue", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Probe Two", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe_two.get_temperature()} C",
                line=2,
                style="center",
            )
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe_two.get_resistance()} Ohms",
                line=3,
                style="center",
            )
            self.titrator.lcd.print("Any key to continue", line=4)
