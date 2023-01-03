from titration.utils import constants
from titration.utils.ui_state.prime_pump import prime_pump
from titration.utils.ui_state.test_mode import test_mode
from titration.utils.ui_state.titration import setup_titration
from titration.utils.ui_state.calibration import setup_calibration
from titration.utils.ui_state.update_settings import update_settings
from titration.utils import lcd_interface


class MainMenu:
    def __init__(self, titrator):
        self.titrator = titrator
        self.subState = 1

    def name(self):
        return "MainMenu"

    def handleKey(self, key):
        # Substate 1 key handle
        if self.subState == 1:
            if key == "*":
                self.subState = 2

            elif key == "1":
                # Next state SetupTitration
                self.titrator.updateState(setup_titration.SetupTitration(self.titrator))

            elif key == "2":
                # Next state SetupCalibration
                self.titrator.updateState(
                    setup_calibration.SetupCalibration(self.titrator, self)
                )

            elif key == "3":
                # Next state PrimePump
                self.titrator.updateState(prime_pump.PrimePump(self.titrator, self))

        # Substate 2 key handle
        elif self.subState == 2:
            if key == "*":
                self.subState = 1

            elif key == "4":
                # Next state UpdateSettings
                self.titrator.updateState(
                    update_settings.UpdateSettings(self.titrator, self)
                )

            elif key == "5":
                # Next state TestMode
                self.titrator.updateState(test_mode.TestMode(self.titrator, self))

            elif key == "6":
                quit()

    def loop(self):
        # Substate 1 output
        if self.subState == 1:
            lcd_interface.lcd_clear()
            lcd_interface.display_list(
                constants.ROUTINE_OPTIONS_1
            )  # TODO: change to LCD

        # Substate 2 output
        else:
            lcd_interface.lcd_clear()
            lcd_interface.display_list(constants.ROUTINE_OPTIONS_2)
