from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.calibration.CalibratePh import CalibratePh

class SetupCalibration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('SetupCalibration', titrator)
        self.titrator = titrator
        self.subState = 0

    def name(self):
        return 'SetupCalibration'

    def handleKey(self, key):
        if key == '1' or key == constants.KEY_1:
            # calibrate pH
            self._setNextState(CalibratePh(self.titrator, self), True)
            pass
        
        elif key == '2' or key == constants.KEY_2:
            # calibrate temp
            pass

    def loop(self):
        interfaces.display_list(constants.SENSOR_OPTIONS)
