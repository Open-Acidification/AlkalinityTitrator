from titration.utils.UIState import UIState
from titration.utils import interfaces
from titration.utils.UIState.PhProbe import PhProbe

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

    def handleKey(self, key):
        pass

    def name(self):
        return 'SolWeightSalinity'

    def loop(self):
        self.values[self.subState] = interfaces.read_user_value(self.prompts[self.subState])
        self.subState += 1
        if self.subState == 2:
            self._setNextState(PhProbe(self.titrator))

    def start(self):
        pass

