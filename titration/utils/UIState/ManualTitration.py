from titration.utils.UIState import UIState
from titration.utils import interfaces, constants

class ManualTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('ManualTitration', titrator)
        self.titrator = titrator
        self.value = 0

    def handleKey(self, key):
        pass

    def name(self):
        return 'ManualTitration'

    def loop(self):
        interfaces.lcd_out("MANUAL SELECTED", style=constants.LCD_CENT_JUST, line=4)

    def start(self):
        pass

