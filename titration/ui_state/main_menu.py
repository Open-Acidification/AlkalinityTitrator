"""
The file for the MainMenu class
"""
import sys

from titration import constants
from titration.ui_state.calibration.setup_calibration import SetupCalibration
from titration.ui_state.demo_mode.demo_mode import DemoMode
from titration.ui_state.prime_pump.prime_pump import PrimePump
from titration.ui_state.titration.setup_titration import SetupTitration
from titration.ui_state.ui_state import UIState
from titration.ui_state.update_settings.update_settings import UpdateSettings


class MainMenu(UIState):
    """
    This is a class for the MainMenu state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                1 -> Setup Titration
                2 -> Setup Calibration
                3 -> Prime Pump
                4 -> Toggle Page
            Substate 2:
                1 -> Update Settings
                2 -> Demo Mode
                3 -> Quit
                4 -> Toggle Page

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if self.substate == 1:
            if key == constants.KEY_1:
                self._set_next_state(SetupTitration(self.titrator), True)

            elif key == constants.KEY_2:
                self._set_next_state(SetupCalibration(self.titrator, self), True)

            elif key == constants.KEY_3:
                self._set_next_state(PrimePump(self.titrator, self), True)

            elif key == constants.KEY_4:
                self.substate = 2
        else:

            if key == constants.KEY_1:
                self._set_next_state(UpdateSettings(self.titrator, self), True)

            elif key == constants.KEY_2:
                self._set_next_state(DemoMode(self.titrator, self), True)

            elif key == constants.KEY_3:
                sys.exit()

            elif key == constants.KEY_4:
                self.substate = 1

    def loop(self):
        """
        The function to loop through until a keypad press
        """

        if self.substate == 1:
            self.titrator.lcd.print("Run titration", line=1)
            self.titrator.lcd.print("Calibrate sensors", line=2)
            self.titrator.lcd.print("Prime pump", line=3)
            self.titrator.lcd.print("Page 2", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Update settings", line=1)
            self.titrator.lcd.print("Test mode", line=2)
            self.titrator.lcd.print("Exit", line=3)
            self.titrator.lcd.print("Page 1", line=4)
