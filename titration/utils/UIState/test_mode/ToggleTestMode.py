from pickletools import int4
from sre_parse import State
from titration.utils.UIState import UIState
from titration.utils import interfaces, constants

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
        interfaces.lcd_clear()
        interfaces.lcd_out("Testing: {}".format(constants.IS_TEST), line=1)
        interfaces.lcd_out("Press any to cont.", line=3)
