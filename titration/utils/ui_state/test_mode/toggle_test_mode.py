from titration.utils import lcd_interface, constants


class ToggleTestMode:
    def __init__(self, titrator, state):
        self.titrator = titrator
        self.values = {"new_volume": 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return "ToggleTestMode"

    def handleKey(self, key):
        self.titrator.updateState(self.previousState)

    def loop(self):
        lcd_interface.lcd_clear()
        lcd_interface.lcd_out("Testing: {}".format(constants.IS_TEST), line=1)
        lcd_interface.lcd_out("", line=2)
        lcd_interface.lcd_out("Press any to cont.", line=3)
        lcd_interface.lcd_out("", line=4)
