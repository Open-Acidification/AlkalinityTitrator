from pickletools import int4
from sre_parse import State
from titration.utils.UIState import UIState
from titration.utils import interfaces, constants, LCD

class ReadVolume(UIState.UIState):
    def __init__(self, titrator, state):
        UIState.__init__('ReadVolume', titrator)
        self.titrator = titrator
        self.values = {'new_volume' : 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return 'ReadVolume'

    def handleKey(self, key):
        self._setNextState(self.previousState, True)

    def loop(self):
        LCD.lcd_clear()
        LCD.lcd_out("Pump Vol: ", line=1)
        LCD.lcd_out(
            "{0:1.2f}".format(constants.volume_in_pump),
            style=constants.LCD_CENT_JUST,
            line=2,
        )
        LCD.lcd_out("Press any to cont.", line=3)
