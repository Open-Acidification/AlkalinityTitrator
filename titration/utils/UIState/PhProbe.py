from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.InitialTitration import InitialTitration

class PhProbe(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('PhProbe', titrator)
        self.titrator = titrator
        self.value = 0

    def handleKey(self, key):
        pass

    def name(self):
        return 'PhProbe'

    def loop(self):
        interfaces.lcd_clear()
        interfaces.lcd_out("Calibrate pH probe?", line=1)
        interfaces.lcd_out("Yes: 1", line=2)
        interfaces.lcd_out("No (use old): 0", line=3)
        interfaces.lcd_out("{0:>2.3f} pH: {1:>2.4f} V".format(constants.PH_REF_PH, constants.PH_REF_VOLTAGE), line=4)
        self.value = interfaces.read_user_input()
        self._setNextState(InitialTitration(self.titrator))

    def start(self):
        pass

