from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, constants


class UserValue(UIState):
    def __init__(self, titrator, state, message):
        super().__init__(titrator, state)
        self.message = message
        self.string = ""

    def handleKey(self, key):
        if key == "A":
            self._setNextState(
                self.previousState, True
            )  # TODO: return entered string to someplace (database or state)

        elif key == "B":
            self.string = self.string[:-1]

        elif key == "C":
            self.string = ""

        elif key == "*":
            if "." not in self.string:
                self.string = self.string + "."

        elif key.isnumeric():
            self.string = self.string + str(key)

    def loop(self):
        lcd_interface.lcd_clear()
        lcd_interface.lcd_out(self.message, line=1)
        lcd_interface.lcd_out(self.string, style=constants.LCD_CENT_JUST, line=2)
        lcd_interface.lcd_out("* = .       B = BS", line=3)
        lcd_interface.lcd_out("A = accept  C = Clr", line=4)
