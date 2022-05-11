from titration.utils.UIState import UIState
from titration.utils import LCD_interface, constants
from titration.utils.UIState.calibration.CalibratePh import CalibratePh
from titration.utils.UIState.calibration.CalibrateTemp import CalibrateTemp

class SetupCalibration(UIState.UIState):
    def __init__(self, titrator, state):
        UIState.__init__('SetupCalibration', titrator,)
        self.titrator = titrator
        self.previousState = state
        self.subState = 1

    def name(self):
        return 'SetupCalibration'

    def handleKey(self, key):
        if key == constants.KEY_1:
            self._setNextState(CalibratePh(self.titrator, self), True)
        
        elif key == constants.KEY_2:
            self._setNextState(CalibrateTemp(self.titrator, self), True)

        elif key == constants.KEY_3:
            self._setNextState(self.previousState, True)

    def loop(self):
        LCD_interface.lcd_out("1. pH", line=1)
        LCD_interface.lcd_out("2. Temperature", line=2)
        LCD_interface.lcd_out("3. Return", line=3)
        LCD_interface.lcd_out("", line=4)
