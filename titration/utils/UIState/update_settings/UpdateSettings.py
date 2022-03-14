from sre_parse import State
from titration.utils.UIState import UIState
from titration.utils import interfaces, constants

class UpdateSettings(UIState.UIState):
    def __init__(self, titrator, state):
        UIState.__init__('UpdateSettings', titrator)
        self.titrator = titrator
        self.values = {'vol_in_pump' : 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return 'UpdateSettings'

    def handleKey(self, key):
        if self.subState == 1:
            if key != 'n' and key != 'N':
                self.subState += 1
            else:
                self.subState += 2
        
        elif self.subState == 2:
            self.subState += 1
        
        elif self.subState == 3:
            if key != 'n' and key != 'N':
                self.subState += 1
            else:
                self._setNextState(self.previousState, True)
        
        elif self.subState == 4:
            self._setNextState(self.previousState, True) 

    def loop(self):
        if self.subState == 1:
            interfaces.lcd_clear()
            interfaces.lcd_out("Reset calibration", line=1)
            interfaces.lcd_out("settings to default?", line=2)
            interfaces.lcd_out("(y/n)", line=3)
        
        elif self.subState == 2:
            interfaces.lcd_clear()
            interfaces.lcd_out("Default constants", line=1)
            interfaces.lcd_out("restored", line=2)
            interfaces.lcd_out("Press any to cont.", line=3)

        elif self.subState == 3:
            interfaces.lcd_clear()
            interfaces.lcd_out("Set volume in pump?", line=1)
            interfaces.lcd_out("(y/n)", line=3)

        elif self.subState == 4:
            self.values['vol_in_pump'] = interfaces.read_user_value("Volume in pump: ")
            interfaces.lcd_clear()
            interfaces.lcd_out("Volume in pump set", line=1)
            interfaces.lcd_out("Press any to cont.", line=3)
