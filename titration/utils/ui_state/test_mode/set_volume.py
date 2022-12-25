from titration.utils.ui_state import ui_state
from titration.utils import lcd_interface
from titration.utils.ui_state.user_value.user_value import UserValue


class SetVolume(ui_state.UIState):
    def __init__(self, titrator, state):
        ui_state.__init__("SetVolume", titrator)
        self.titrator = titrator
        self.values = {"new_volume": 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return "SetVolume"

    def handleKey(self, key):
        if self.subState == 1:
            self._setNextState(UserValue(self.titrator, self, "Volume in pump: "), True)
            self.subState += 1

        elif self.subState == 2:
            self._setNextState(self.previousState, True)

    def loop(self):
        if self.subState == 1:
            lcd_interface.lcd_out("Set volume in pump", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 2:
            lcd_interface.lcd_out("Volume in pump", line=1)
            lcd_interface.lcd_out("recorded", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)
