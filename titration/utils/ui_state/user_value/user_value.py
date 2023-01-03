from titration.utils import lcd_interface, constants


class UserValue:
    def __init__(self, titrator, state, message):
        self.titrator = titrator
        self.previousState = state
        self.decimal = False
        self.message = message
        self.string = ""

    def name(self):
        return "UserValue"

    def handleKey(self, key):
        if key == "A":
            self.titrator.updateState(self.previousState)
            # TODO: return entered string to someplace (database or state)

        elif key == "B":
            if len(self.string) > 0:
                popped = self.string[-1]
                self.string = self.string[:len(self.string)-1]
                if popped == ".":
                    self.decimal = False

        elif key == "C":
            self.decimal = False
            self.string = ""

        elif key == "*":
            if self.decimal is False:
                if len(self.string) > 0:
                    self.string = self.string + "."
                    self.decimal = True
                else:
                    self.string = "0."
                    self.decimal = True 

        elif key.isnumeric():
            self.string = self.string + str(key)

    def loop(self):
        lcd_interface.lcd_out(self.message, line=1)
        lcd_interface.lcd_out(self.string, style=constants.LCD_CENT_JUST, line=2)
        lcd_interface.lcd_out("* = .       B = BS", line=3)
        lcd_interface.lcd_out("A = accept  C = Clr", line=4)
