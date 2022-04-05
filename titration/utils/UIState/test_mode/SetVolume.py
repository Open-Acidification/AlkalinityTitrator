from pickletools import int4
from sre_parse import State
from titration.utils.UIState import UIState
from titration.utils import interfaces, constants, LCD

class SetVolume(UIState.UIState):
    def __init__(self, titrator, state):
        UIState.__init__('SetVolume', titrator)
        self.titrator = titrator
        self.values = {'new_volume' : 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return 'SetVolume'

    def handleKey(self, key):
        self._setNextState(self.previousState, True)

    def loop(self):
        self.values['new_volume'] = LCD.read_user_value("Volume in pump: ")
        LCD.lcd_clear()
        LCD.lcd_out("Press any to cont.", line=1)
