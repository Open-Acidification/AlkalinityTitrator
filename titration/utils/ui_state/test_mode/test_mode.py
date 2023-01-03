from titration.utils import lcd_interface, constants
from titration.utils.ui_state.test_mode.pump import Pump
from titration.utils.ui_state.test_mode.read_values import ReadValues
from titration.utils.ui_state.test_mode.read_volume import ReadVolume
from titration.utils.ui_state.test_mode.set_volume import SetVolume
from titration.utils.ui_state.test_mode.toggle_test_mode import ToggleTestMode


class TestMode:
    def __init__(self, titrator, state):
        self.titrator = titrator
        self.subState = 1
        self.previousState = state

    def name(self):
        return "TestMode"

    def handleKey(self, key):
        if self.subState == 1:
            if key == constants.KEY_STAR:
                self.subState += 1

            elif key == constants.KEY_1:
                self.titrator.updateState(ReadValues(self.titrator, self))

            elif key == constants.KEY_2:
                self.titrator.updateState(Pump(self.titrator, self))

            elif key == constants.KEY_3:
                self.titrator.updateState(SetVolume(self.titrator, self))

        elif self.subState == 2:
            if key == constants.KEY_STAR:
                self.subState -= 1

            elif key == constants.KEY_4:
                self.titrator.updateState(ToggleTestMode(self.titrator, self))

            elif key == constants.KEY_5:
                self.titrator.updateState(ReadVolume(self.titrator, self))

            elif key == constants.KEY_6:
                self.titrator.updateState(self.previousState)

    def loop(self):
        if self.subState == 1:
            lcd_interface.lcd_out("1: Read Values", line=1)
            lcd_interface.lcd_out("2: Pump", line=2)
            lcd_interface.lcd_out("3: Set Volume", line=3)
            lcd_interface.lcd_out("*: Page 2", line=4)

        elif self.subState == 2:
            lcd_interface.lcd_out("4: Toggle Test Mode", line=1)
            lcd_interface.lcd_out("5: Read Volume", line=2)
            lcd_interface.lcd_out("6: Exit Test Mode", line=3)
            lcd_interface.lcd_out("*: Page 1", line=4)
