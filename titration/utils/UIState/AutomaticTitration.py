from titration.utils.UIState import UIState
from titration.utils import interfaces, constants

class AutomaticTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('AutomaticTitration', titrator)
        self.titrator = titrator
        self.value = 0

    def handleKey(self, key):
        pass

    def name(self):
        return 'AutomaticTitration'

    def loop(self):
        pass

    def start(self):
        pass

