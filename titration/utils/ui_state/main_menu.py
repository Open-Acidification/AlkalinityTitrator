from titration.utils.ui_state.ui_state import UIState
from titration.utils import constants
from titration.utils.ui_state.prime_pump import prime_pump
from titration.utils.ui_state.test_mode import test_mode
from titration.utils.ui_state.titration import setup_titration
from titration.utils.ui_state.calibration import setup_calibration
from titration.utils.ui_state.update_settings import update_settings
from titration.utils import lcd_interface


class MainMenu(UIState):
    def handleKey(self, key):
        # Substate 1 key handle
        if self.subState == 1:
            if key == constants.KEY_STAR:
                self.subState = 2

            elif key == constants.KEY_1:
                # Next state SetupTitration
                self._setNextState(setup_titration.SetupTitration(self.titrator), True)

            elif key == constants.KEY_2:
                # Next state SetupCalibration
                self._setNextState(
                    setup_calibration.SetupCalibration(self.titrator, self), True
                )

            elif key == constants.KEY_3:
                # Next state PrimePump
                self._setNextState(prime_pump.PrimePump(self.titrator, self), True)

        # Substate 2 key handle
        else:
            if key == constants.KEY_STAR:
                self.subState = 1

            elif key == constants.KEY_4:
                # Next state UpdateSettings
                self._setNextState(
                    update_settings.UpdateSettings(self.titrator, self), True
                )

            elif key == constants.KEY_5:
                # Next state TestMode
                self._setNextState(test_mode.TestMode(self.titrator, self), True)

            elif key == constants.KEY_6:
                quit()

    def loop(self):
        # Substate 1 output
        if self.subState == 1:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Run titration", line=1)
            lcd_interface.lcd_out("Calibrate sensors", line=2)
            lcd_interface.lcd_out("Prime pump", line=3)
            lcd_interface.lcd_out("Page 2", line=4)

        # Substate 2 output
        elif self.subState == 2:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Update settings", line=1)
            lcd_interface.lcd_out("Test mode", line=2)
            lcd_interface.lcd_out("Exit", line=3)
            lcd_interface.lcd_out("Page 1", line=4)
