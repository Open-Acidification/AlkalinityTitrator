from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.AutomaticTitration import AutomaticTitration
from titration.utils.UIState.ManualTitration import ManualTitration

class InitialTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('InitialTitration', titrator)
        self.titrator = titrator
        self.value = 0

    def handleKey(self, key):
        pass

    def name(self):
        return 'InitialTitration'

    def loop(self):
        # Manual or automatic titration
        interfaces.lcd_out("Bring pH to 3.5:", line=1)
        interfaces.lcd_out("Manual: 1", line=2)
        interfaces.lcd_out("Automatic: 2", line=3)
        interfaces.lcd_out("Stir speed: slow", line=4)
        self.value = interfaces.read_user_input()

        # wait until solution is up to temperature
        interfaces.lcd_clear()
        interfaces.lcd_out("Heating to 30 C...", line=1)
        interfaces.lcd_out("Please wait...", style=constants.LCD_CENT_JUST, line=3)

        if self.value == 1:
            self._setNextState(ManualTitration(self.titrator))
        else:
            self._setNextState(AutomaticTitration(self.titrator))

    def start(self):
        pass

