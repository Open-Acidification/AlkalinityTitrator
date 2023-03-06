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
                1 -> Get Temperature
                2 -> Get Resistance
                3 -> Activate Temp Control
                4 -> Return to Demo Mode Menu
            Substate 2:
                Any -> Substate 1
            Substate 3:
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
            elif key == constants.KEY_3:
                self.titrator.temp_controller.activate()
                self.substate = 4
            elif key == constants.KEY_4:
                self._set_next_state(self.previous_state, True)

        elif self.substate == 4:
            self.titrator.temp_controller.deactivate()
            self.substate = 1

        else:
            self.substate = 1

        if key == constants.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Get Temperature", line=1)
            self.titrator.lcd.print("2: Get Resistance", line=2)
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("4: Return", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Probe Temperature", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe.get_temperature()} C",
                line=2,
                style="center",
            )
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Probe Resistance", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe.get_resistance()} Ohms",
                line=2,
                style="center",
            )
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 4:
            self.titrator.lcd.print("Temperature Control", line=1)
            self.titrator.lcd.print("Activated", line=2, style="center")
            self.titrator.lcd.print(
                f"{self.titrator.temp_probe.get_temperature()} C", line=3
            )
            self.titrator.lcd.print("Press any to stop", line=4)

            self.titrator.temp_controller.update()
