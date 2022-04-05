from pickletools import int4
from sre_parse import State
from titration.utils.UIState import UIState
from titration.utils import interfaces, constants, LCD

class Pump(UIState.UIState):
    def __init__(self, titrator, state):
        UIState.__init__('Pump', titrator)
        self.titrator = titrator
        self.values = {'p_direction' : 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return 'Pump'

    def handleKey(self, key):
        if self.subState == 1:
            if key == 0 or key == constants.KEY_0 or key == 1 or key == constants.KEY_1:
                self.values['p_direction'] = key
                self.subState += 1
        
        elif self.subState == 2:
            self._setNextState(self.previousState, True)

    def loop(self):
        if self.subState == 1:
            self.values['p_volume'] = LCD.read_user_value("Volume: ")

            LCD.lcd_clear()
            LCD.lcd_out("In/Out (0/1):", line=1)

        elif self.subState == 2:
            LCD.lcd_clear()
            LCD.lcd_out("Pumping volume", line=1)
            LCD.lcd_out("Press any to cont.", line=3)