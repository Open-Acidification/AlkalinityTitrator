from titration.utils import lcd_interface


# TODO: feedback on number of pumps; one state? Use "D" to exit always
# TODO: implement constant feedback on pumping
class PrimePump:
    def __init__(self, titrator, state):
        self.titrator = titrator
        self.values = {"selection": 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return "PrimePump"

    def handleKey(self, key):
        if self.subState == 1:
            self.values["selection"] = key
            self.subState += 1

        elif self.subState == 2:
            self.values["selection"] = key

        if self.values["selection"] == "0":
            self.titrator.updateState(self.previousState)

    def loop(self):
        if self.subState == 1:
            lcd_interface.lcd_out("How many pumps?", line=1)
            lcd_interface.lcd_out("Choose a number", line=2)
            lcd_interface.lcd_out("Choose 0 to return", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 2:
            lcd_interface.lcd_out("How many more?", line=1)
            lcd_interface.lcd_out("Choose a number", line=2)
            lcd_interface.lcd_out("Choose 0 to return", line=3)
            lcd_interface.lcd_out("", line=4)
