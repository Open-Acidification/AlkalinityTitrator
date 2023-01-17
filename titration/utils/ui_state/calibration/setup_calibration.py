"""
The file for the SetupCalibration class
"""
from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, constants
from titration.utils.ui_state.calibration.calibrate_ph import CalibratePh
from titration.utils.ui_state.calibration.calibrate_temp import CalibrateTemp


class SetupCalibration(UIState):
    """
    This is a class for the SetupCalibration state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def handle_key(self, key):
        """
        The function to handle keypad input:
            1 -> Calibrate pH
            2 -> Calibrate Temp
            3 -> Previous State

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if key == constants.KEY_1:
            self._set_next_state(CalibratePh(self.titrator, self), True)

        elif key == constants.KEY_2:
            self._set_next_state(CalibrateTemp(self.titrator, self), True)

        elif key == constants.KEY_3:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        lcd_interface.lcd_clear()
        lcd_interface.lcd_out("1. pH", line=1)
        lcd_interface.lcd_out("2. Temperature", line=2)
        lcd_interface.lcd_out("3. Return", line=3)
        lcd_interface.lcd_out("", line=4)
