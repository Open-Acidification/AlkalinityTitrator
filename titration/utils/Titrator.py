from titration.utils.UIState import UIState, MainMenu
from titration.utils import interfaces, constants, Input
import sys

class Titrator:
    def __init__(self):
        self.state = MainMenu.MainMenu(self)
        self.nextState = None
        interfaces.setup_interfaces()

    def loop(self):
        self._handleUI()                            # look at keypad, update LCD

    def setNextState(self, newState, update):
        print("Titrator::setNextState() from ", self.nextState.name() if self.nextState else 'nullptr', " to ", newState.name())
        assert(self.nextState == None)
        self.nextState = newState
        if (update):
            self._updateState()

    def setup():
        pass

    def _updateState(self):
        if (self.nextState):
            print("Titrator::updateState() to ", self.nextState.name())
            assert(self.state != self.nextState)
            self.state = self.nextState
            self.nextState = None
            self.state.start()

    def _handleUI(self):
        print("Titrator::handleUI() - ", self.state.name())
        key = Input.getKey()
        if (key == constants.NO_KEY):
            if (self.nextState):
                pass
        else:
            print("Titrator::handleUI() - ", self.state.name(), "::handleKey(", key, ")")
            self.state.handleKey(key)
        self._updateState()
        print("Titrator::handleUI() - ", self.state.name(), "::substate", self.state.subState, "::loop()")
        self.state.loop()
        