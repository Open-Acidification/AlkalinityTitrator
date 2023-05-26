"""
The file for the  class
"""

from titration.devices.library import Keypad
from titration.ui_state.demo_mode.demo_pump import DemoPump
from titration.ui_state.demo_mode.demo_stir_control import DemoStirControl
from titration.ui_state.demo_mode.demo_temperature_controller import (
    DemoTemperatureControl,
)
from titration.ui_state.demo_mode.demo_temperature_probe import (
    DemoTemperatureProbe,
)
from titration.ui_state.demo_mode.read_values import ReadValues
from titration.ui_state.ui_state import UIState


class DemoModeMenu(UIState):
    """
    This is a class for the  state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                1 -> Read Values
                2 -> Demo pH Probe
                3 -> Demo Pump
                4 -> Toggle menu pages
            Substate 2:
                1 -> Demo Stir Control
                2 -> Demo Temperature Probes
                3 -> Demo Temperature Controls
                4 -> Toggle menu pages
            Substate 3:
                Any -> Return to Demo Mode Menu
            D -> Return to Main Menu

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if self.substate == 1:
            if key == Keypad.KEY_1:
                self._set_next_state(ReadValues(self.titrator, self), True)

            elif key == Keypad.KEY_2:
                self.substate = 3

            elif key == Keypad.KEY_3:
                self._set_next_state(DemoPump(self.titrator, self), True)

            elif key == Keypad.KEY_4:
                self.substate = 2

        elif self.substate == 2:
            if key == Keypad.KEY_1:
                self._set_next_state(DemoStirControl(self.titrator, self), True)

            elif key == Keypad.KEY_2:
                self._set_next_state(DemoTemperatureProbe(self.titrator, self), True)

            elif key == Keypad.KEY_3:
                self._set_next_state(DemoTemperatureControl(self.titrator, self), True)

            if key == Keypad.KEY_4:
                self.substate = 1

        elif self.substate == 3:
            self.substate = 1

        if key == Keypad.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Read values", line=1)
            self.titrator.lcd.print("2: Demo pH probe", line=2)
            self.titrator.lcd.print("3: Demo pump", line=3)
            self.titrator.lcd.print("4: Page 2", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("1: Demo stir control", line=1)
            self.titrator.lcd.print("2: Demo temp probe", line=2)
            self.titrator.lcd.print("3: Demo temp control", line=3)
            self.titrator.lcd.print("4: Page 1", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("pH probe", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.ph_probe.get_voltage()} volts", line=2, style="center"
            )
            self.titrator.lcd.print(
                f"{self.titrator.ph_probe.get_gain()} volts", line=3, style="center"
            )
            self.titrator.lcd.print("Any key to continue", line=4)
