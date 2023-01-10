from titration.utils.ui_state import ui_state
from titration.utils import lcd_interface
from titration.utils.ui_state.user_value.user_value import UserValue


class CalibratePh(ui_state.UIState):
    def __init__(self, titrator, state):
        ui_state.__init__("CalibratePh", titrator)
        self.titrator = titrator
        self.values = {"buffer1_measured_volts": 5, "buffer1_actual_pH": 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return "CalibratePh"

    def handleKey(self, key):
        if self.subState == 1:
            self._setNextState(UserValue(self.titrator, self, "Sol. weight (g):"), True)
            self.subState += 1

        elif self.subState == 2:
            self.subState += 1

        elif self.subState == 3:
            self._setNextState(self.previousState, True)

    def loop(self):
        if self.subState == 1:
            lcd_interface.lcd_out("Enter Sol weight", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 2:
            lcd_interface.lcd_out("Put sensor in buffer", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("to record value", line=4)

        elif self.subState == 3:
            lcd_interface.lcd_out("Recorded pH and volts:", line=1)
            lcd_interface.lcd_out(
                "{0:>2.5f} pH, {1:>3.4f} V".format(
                    self.values["buffer1_actual_pH"],
                    self.values["buffer1_measured_volts"],
                ),
                line=2,
            )
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)
