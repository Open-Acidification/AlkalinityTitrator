from titration.utils.UIState import UIState
from titration.utils import LCD_interface, constants

class ToggleTestMode(UIState.UIState):
    def __init__(self, titrator, state):
        UIState.__init__('ToggleTestMode', titrator)
        self.titrator = titrator
        self.values = {'new_volume' : 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return 'ToggleTestMode'

    def handleKey(self, key):
        self._setNextState(self.previousState, True)

    def loop(self):
        LCD_interface.lcd_clear()
        LCD_interface.lcd_out("Testing: {}".format(constants.IS_TEST), line=1)
        LCD_interface.lcd_out("", line=2)
        LCD_interface.lcd_out("Press any to cont.", line=3)
        LCD_interface.lcd_out("", line=4)
