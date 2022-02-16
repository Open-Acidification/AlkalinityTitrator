from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.InitialTitration import InitialTitration

class CalibratePhProbe(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('CalibratePhProbe', titrator)
        self.titrator = titrator
        self.value = 0

    def name(self):
        return 'CalibratePhProbe'

    def handleKey(self, key):
        self.value = key
        self._setNextState(InitialTitration(self.titrator), True)

    def loop(self):
        interfaces.lcd_clear()
        interfaces.lcd_out("Calibrate pH probe?", line=1)
        interfaces.lcd_out("Yes: 1", line=2)
        interfaces.lcd_out("No (use old): 0", line=3)
        interfaces.lcd_out("{0:>2.3f} pH: {1:>2.4f} V".format(constants.PH_REF_PH, constants.PH_REF_VOLTAGE), line=4)
