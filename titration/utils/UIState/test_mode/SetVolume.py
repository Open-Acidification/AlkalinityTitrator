from titration.utils.UIState import UIState
from titration.utils import LCD_interface
from titration.utils.UIState.user_value.UserValue import UserValue

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
        if self.subState == 1:
            self._setNextState(UserValue(self.titrator, self, 'Volume in pump: '), True)
            self.subState += 1

        elif self.subState == 2:
            self._setNextState(self.previousState, True)

    def loop(self):
        if self.subState == 1:
            LCD_interface.lcd_out("Set volume in pump", line=1)
            LCD_interface.lcd_out("", line=2)
            LCD_interface.lcd_out("Press any to cont", line=3)
            LCD_interface.lcd_out("", line=4)

        elif self.subState == 2:
            LCD_interface.lcd_out("Volume in pump", line=1)
            LCD_interface.lcd_out("recorded", line=2)
            LCD_interface.lcd_out("Press any to cont", line=3)
            LCD_interface.lcd_out("", line=4)
