from titration.utils.UIState import UIState
from titration.utils import interfaces, constants

class MainMenu (UIState.UIState):
    def __init__(self, tc):
        UIState.__init__('MainMenu', tc)
        self.routineSelection = 1


    def handleKey(self, key):
        if key is constants.KEY_STAR and self.routineSelection == 1:
            self.routineSelection = 2
        else:
            self.routineSelection = 1
        pass


    def name(self):
        return "MainMenu"


    def loop(self):
        # Display menu options.
        if self.routineSelection == 1:
            interfaces.display_list(constants.ROUTINE_OPTIONS_1)
        else:
            interfaces.display_list(constants.ROUTINE_OPTIONS_2)
        pass


    def start(self):
        pass


    def _setNextState(self, state):
        self.tc.setNextState(state)
