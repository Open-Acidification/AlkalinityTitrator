from titration.utils.UIState import UIState
from titration.utils import interfaces
from titration.utils.UIState.CalibratePhProbe import CalibratePhProbe

class SolWeightSalinity(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('SolWeightSalinity', titrator)
        self.titrator = titrator
        self.prompts = [
            'Sol. weight (g):',
            'Sol. salinity (ppt):'
        ]
        self.values = [ 0, 0 ]
        self.subState = 0

    def name(self):
        return 'SolWeightSalinity'

    def handleKey(self, key):
        pass

    def loop(self):
        self.values[self.subState] = interfaces.read_user_value(self.prompts[self.subState])
        self.subState += 1
        if self.subState == 2:
            self._setNextState(CalibratePhProbe(self.titrator), True)

    def start(self):
        pass
