"""
The file for the DemoMode class
"""
from titration import constants
from titration.ui_state.demo_mode.pump import Pump
from titration.ui_state.demo_mode.read_values import ReadValues
from titration.ui_state.demo_mode.read_volume import ReadVolume
from titration.ui_state.demo_mode.set_volume import SetVolume
from titration.ui_state.demo_mode.toggle_demo_mode import ToggleDemoMode
from titration.ui_state.ui_state import UIState


class DemoMode(UIState):
    """
    This is a class for the DemoMode state of the titrator

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
                2 -> Pump
                3 -> Set Volume
                4 -> Toggle menu pages
            Substate 2:
                1 -> Toggle Demo Mode
                2 -> Read Volume
                3 -> Return to previous state
                4 -> Toggle menu pages

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if self.substate == 1:
            if key == constants.KEY_1:
                self._set_next_state(ReadValues(self.titrator, self), True)

            elif key == constants.KEY_2:
                self._set_next_state(Pump(self.titrator, self), True)

            elif key == constants.KEY_3:
                self._set_next_state(SetVolume(self.titrator, self), True)

            elif key == constants.KEY_4:
                self.substate += 1

        elif self.substate == 2:
            if key == constants.KEY_1:
                self._set_next_state(ToggleDemoMode(self.titrator, self), True)

            elif key == constants.KEY_2:
                self._set_next_state(ReadVolume(self.titrator, self), True)

            elif key == constants.KEY_3:
                self._set_next_state(self.previous_state, True)

            if key == constants.KEY_4:
                self.substate -= 1

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Read Values", line=1)
            self.titrator.lcd.print("2: Pump", line=2)
            self.titrator.lcd.print("3: Set Volume", line=3)
            self.titrator.lcd.print("4: Page 2", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("1: Toggle Demo Mode", line=1)
            self.titrator.lcd.print("2: Read Volume", line=2)
            self.titrator.lcd.print("3: Exit Demo Mode", line=3)
            self.titrator.lcd.print("4: Page 1", line=4)
