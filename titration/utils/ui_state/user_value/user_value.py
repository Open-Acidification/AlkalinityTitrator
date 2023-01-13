from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, constants


class UserValue(UIState):
    def __init__(self, titrator, state, message):
        super().__init__(titrator, state)
        self.inputs = []
        self.decimal = False
        self.message = message
        self.string = ""

    def handleKey(self, key):
        if key == "A":
            self._setNextState(
                self.previousState, True
            )  # TODO: return entered string to someplace (database or state)

        elif key == "B":
            if len(key) > 0:
                popped = self.inputs.pop()
                if popped == "*":
                    self.decimal = False
                self.string = self.string[:-1]

        elif key == "C":
            self.inputs.clear()
            self.decimal = False
            self.string = "_"

        elif key == "D":
            self._setNextState(self.previousState, True)

        elif key.isnumeric() or key == "*":

            # Check for decimal. If there is already one, do nothing
            if key == "*":
                if not self.decimal:
                    self.inputs.append(key)
                    self.string = self.string + "."
                    self.decimal = True
            # Otherwise, add number to input list
            else:
                self.string = self.string + str(key)
                self.inputs.append(int(key))

    def loop(self):
        lcd_interface.lcd_clear()
        lcd_interface.lcd_out(self.message, line=1)
        lcd_interface.lcd_out(self.string, style=constants.LCD_CENT_JUST, line=2)
        lcd_interface.lcd_out("* = .       B = BS", line=3)
        lcd_interface.lcd_out("A = accept  C = Clr", line=4)
