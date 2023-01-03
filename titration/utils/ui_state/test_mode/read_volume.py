from titration.utils import lcd_interface, constants


class ReadVolume:
    def __init__(self, titrator, state):
        self.titrator = titrator
        self.values = {"new_volume": 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return "ReadVolume"

    def handleKey(self, key):
        self.titrator.updateState(self.previousState)

    def loop(self):
        lcd_interface.lcd_out("Pump Vol: ", line=1)
        lcd_interface.lcd_out(
            "{0:1.2f}".format(constants.volume_in_pump),
            style=constants.LCD_CENT_JUST,
            line=2,
        )
        lcd_interface.lcd_out("Press any to cont.", line=3)
        lcd_interface.lcd_out("", line=4)
