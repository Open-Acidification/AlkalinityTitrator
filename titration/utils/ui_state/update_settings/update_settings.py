from titration.utils import lcd_interface
from titration.utils.ui_state.user_value.user_value import UserValue


class UpdateSettings:
    def __init__(self, titrator, state):
        self.titrator = titrator
        self.values = {"vol_in_pump": 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return "UpdateSettings"

    def handleKey(self, key):
        if self.subState == 1:
            if key != "n" and key != "N":
                self.subState += 1
            else:
                self.subState += 2

        elif self.subState == 2:
            self.subState += 1

        elif self.subState == 3:
            if key != "n" and key != "N":
                self.subState += 1
            else:
                self.titrator.updateState(self.previousState)

        elif self.subState == 4:
            self.titrator.updateState(UserValue(self.titrator, self, "Volume in pump:"))
            self.subState += 1

        elif self.subState == 5:
            self.titrator.updateState(self.previousState)

    def loop(self):
        if self.subState == 1:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Reset calibration", line=1)
            lcd_interface.lcd_out("settings to default?", line=2)
            lcd_interface.lcd_out("(y/n)", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 2:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Default constants", line=1)
            lcd_interface.lcd_out("restored", line=2)
            lcd_interface.lcd_out("Press any to cont.", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 3:
            lcd_interface.lcd_out("Set volume in pump?", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("(y/n)", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 4:
            lcd_interface.lcd_out("Enter Volume in pump", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 5:
            lcd_interface.lcd_out("Volume in pump set", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)
