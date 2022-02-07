from titration.utils.UIState import UIState

class MainMenu (UIState.UIState):
    def __init__(self, tc):
        UIState.__init__('MainMenu', tc)

    def handleKey(self, key):
        pass

    def name(self):
        return "MainMenu"

    def loop(self):
        pass

    def start(self):
        pass

    def _setNextState(self, state):
        self.tc.setNextState(state)
