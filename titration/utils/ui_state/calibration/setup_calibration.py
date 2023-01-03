from titration.utils import lcd_interface, constants
from titration.utils.ui_state.calibration.calibrate_ph import CalibratePh
from titration.utils.ui_state.calibration.calibrate_temp import CalibrateTemp


class SetupCalibration:
    def __init__(self, titrator, state):
        self.titrator = titrator
        self.previousState = state
        self.subState = 1

    def name(self):
        return "SetupCalibration"

    def handleKey(self, key):
        if key == constants.KEY_1:
            self.titrator.updateState(CalibratePh(self.titrator, self))

        elif key == constants.KEY_2:
            self.titrator.updateState(CalibrateTemp(self.titrator, self))

        elif key == constants.KEY_3:
            self.titrator.updateState(self.previousState)

    def loop(self):
        lcd_interface.lcd_out("1. pH", line=1)
        lcd_interface.lcd_out("2. Temperature", line=2)
        lcd_interface.lcd_out("3. Return", line=3)
        lcd_interface.lcd_out("", line=4)
