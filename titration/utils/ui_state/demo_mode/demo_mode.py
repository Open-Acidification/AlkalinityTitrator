"""
The file for the DemoMode class
"""
from AlkalinityTitrator.titration.utils.ui_state.ui_state import UIState
from AlkalinityTitrator.titration.utils import constants
from AlkalinityTitrator.titration.utils.ui_state.demo_mode.pump import Pump
from AlkalinityTitrator.titration.utils.ui_state.demo_mode.read_values import ReadValues
from AlkalinityTitrator.titration.utils.ui_state.demo_mode.read_volume import ReadVolume
from AlkalinityTitrator.titration.utils.ui_state.demo_mode.set_volume import SetVolume
from AlkalinityTitrator.titration.utils.ui_state.demo_mode.toggle_demo_mode import ToggleDemoMode


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
            * -> Toggle menu pages
            1 -> Read Values
            2 -> Pump
            3 -> Set Volume
            4 -> Toggle Demo Mode
            5 -> Read Volume
            6 -> Return to previous state

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if self.substate == 1:
            if key == constants.KEY_STAR:
                self.substate += 1

            elif key == constants.KEY_1:
                self._set_next_state(ReadValues(self.titrator, self), True)

            elif key == constants.KEY_2:
                self._set_next_state(Pump(self.titrator, self), True)

            elif key == constants.KEY_3:
                self._set_next_state(SetVolume(self.titrator, self), True)

        elif self.substate == 2:
            if key == constants.KEY_STAR:
                self.substate -= 1

            elif key == constants.KEY_4:
                self._set_next_state(ToggleDemoMode(self.titrator, self), True)

            elif key == constants.KEY_5:
                self._set_next_state(ReadVolume(self.titrator, self), True)

            elif key == constants.KEY_6:
                self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("1: Read Values", line=1)
            self.titrator.lcd.print("2: Pump", line=2)
            self.titrator.lcd.print("3: Set Volume", line=3)
            self.titrator.lcd.print("*: Page 2", line=4)

        elif self.substate == 2:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("4: Toggle Demo Mode", line=1)
            self.titrator.lcd.print("5: Read Volume", line=2)
            self.titrator.lcd.print("6: Exit Demo Mode", line=3)
            self.titrator.lcd.print("*: Page 1", line=4)