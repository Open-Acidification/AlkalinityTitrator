"""
The file for the  class
"""

from titration.devices.library import Keypad
from titration.ui_state.demo_mode.demo_ph_probe import DemopHProbe
from titration.ui_state.demo_mode.demo_pump import DemoPump
from titration.ui_state.demo_mode.demo_stir_control import DemoStirControl
from titration.ui_state.demo_mode.demo_temp_probe import DemoTempControl
from titration.ui_state.demo_mode.read_values import ReadValues
from titration.ui_state.demo_mode.toggle_demo_mode import ToggleDemoMode
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
                2 -> Demo Temp Control
                3 -> Toggle Demo Mode
                4 -> Toggle menu pages
            D -> Return to Main Menu

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if self.substate == 1:
            if key == Keypad.KEY_1:
                self._set_next_state(ReadValues(self.titrator, self), True)

            elif key == Keypad.KEY_2:
                self._set_next_state(DemopHProbe(self.titrator, self), True)

            elif key == Keypad.KEY_3:
                self._set_next_state(DemoPump(self.titrator, self), True)

            elif key == Keypad.KEY_4:
                self.substate = 2

        elif self.substate == 2:
            if key == Keypad.KEY_1:
                self._set_next_state(DemoStirControl(self.titrator, self), True)

            elif key == Keypad.KEY_2:
                self._set_next_state(DemoTempControl(self.titrator, self), True)

            elif key == Keypad.KEY_3:
                self._set_next_state(ToggleDemoMode(self.titrator, self), True)

            if key == Keypad.KEY_4:
                self.substate = 1

        if key == Keypad.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Read Values", line=1)
            self.titrator.lcd.print("2: Demo pH Probe", line=2)
            self.titrator.lcd.print("3: Demo Pump", line=3)
            self.titrator.lcd.print("4: Page 2", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("1: Demo Stir Control", line=1)
            self.titrator.lcd.print("2: Demo Temp Probe", line=2)
            self.titrator.lcd.print("3: Toggle Demo Mode", line=3)
            self.titrator.lcd.print("4: Page 1", line=4)
