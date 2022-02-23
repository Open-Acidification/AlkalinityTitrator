from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.titration.InitialTitration import InitialTitration

class SetupTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('SetupTitration', titrator)
        self.titrator = titrator
        self.prompts = [
            'Sol. weight (g):',
            'Sol. salinity (ppt):'
        ]
        self.values = { 'weight' : 0, 'salinity' : 0}
        self.subState = 0

    def name(self):
        return 'SetupTitration'

    def handleKey(self, key):
        self.value = key
        self._setNextState(InitialTitration(self.titrator), True)

    def loop(self):
        self.values[self.subState] = interfaces.read_user_value(self.prompts[self.subState])
        self.subState += 1

        if self.subState == 2:
            interfaces.lcd_clear()
            interfaces.lcd_out("Calibrate pH probe?", line=1)
            interfaces.lcd_out("Yes: 1", line=2)
            interfaces.lcd_out("No (use old): 0", line=3)
            interfaces.lcd_out("{0:>2.3f} pH: {1:>2.4f} V".format(constants.PH_REF_PH, constants.PH_REF_VOLTAGE), line=4)

    def start(self):
        pass
