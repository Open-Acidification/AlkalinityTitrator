from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
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
        # Substate 1 key handle
        if key == 1 or key == constants.KEY_1:
            # calibrate pH
            self._setNextState(CalibratePh(self.titrator, self), True)
        
        elif key == 2 or key == constants.KEY_2:
            # calibrate temp
            self._setNextState(CalibrateTemp(self.titrator, self), True)

        elif key == 3 or key == constants.KEY_3:
            # return to main menu
            self._setNextState(self.previousState, True)

    def loop(self):
        # Substate 1 output
        interfaces.display_list(constants.SENSOR_OPTIONS)
        interfaces.lcd_out("3. Return", line=3)
