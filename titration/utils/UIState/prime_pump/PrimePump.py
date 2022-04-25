from titration.utils.UIState import UIState
from titration.utils import LCD

class PrimePump(UIState.UIState):
    def __init__(self, titrator, state):
        UIState.__init__('PrimePump', titrator)
        self.titrator = titrator
        self.values = {'selection' : 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return 'PrimePump'

    def handleKey(self, key):
        # Substate 1 key handle
        if self.subState == 1:
            try:
                self.values['selection'] = int(key)
                self.subState += 1
            except:
                pass
        
        # Substate 2 key handle
        elif self.subState == 2:
            try:
                self.values['selection'] = int(key)
            except:
                pass
        
        # Substate 1 and 2; check if selection is 0
        if self.values['selection'] == 0:
            self._setNextState(self.previousState, True)

    def loop(self):
        # Substate 1 output
        if self.subState == 1:
            LCD.lcd_clear()
            LCD.lcd_out("How many pumps?", line=1)
            LCD.lcd_out("Choose a number", line=2)
            LCD.lcd_out("Choose 0 to return", line=3)

        # Substate 2 output
        elif self.subState == 2:
            LCD.lcd_out("How many more?", line=1)
            LCD.lcd_out("Choose a number", line=2)
            LCD.lcd_out("Choose 0 to return", line=3)
