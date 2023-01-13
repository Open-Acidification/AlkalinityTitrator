from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, constants
from titration.utils.ui_state.user_value.user_value import UserValue


class CalibrateTemp(UIState):
    def __init__(self, titrator, state):
        super().__init__(titrator, state)
        self.values = {
            "actual_temperature": 5,
            "new_ref_resistance": 5,
            "expected_temperature": 0,
        }

    def name(self):
        return "CalibrateTemp"

    def handleKey(self, key):
        if self.subState == 1:
            self._setNextState(
                UserValue(self.titrator, self, "Ref solution temp:"), True
            )
            self.subState += 1

        elif self.subState == 2:
            if key == 1 or key == constants.KEY_1:
                self.subState += 1

        elif self.subState == 3:
            self._setNextState(self.previousState, True)

    def loop(self):
        if self.subState == 1:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Set Ref solution", line=1)
            lcd_interface.lcd_out("temp", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 2:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Put probe in sol", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press 1 to", line=3)
            lcd_interface.lcd_out("record value", line=4)

        elif self.subState == 3:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Recorded temp:", line=1)
            lcd_interface.lcd_out(
                "{0:0.3f}".format(self.values["actual_temperature"]), line=2
            )
            lcd_interface.lcd_out(
                "{}".format(self.values["new_ref_resistance"]), line=3
            )
            lcd_interface.lcd_out("", line=4)
            # TODO: reinitialize sensors with calibrated values
