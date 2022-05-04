from titration.utils.UIState import UIState
from titration.utils import LCD_interface, constants
from titration.utils.UIState.test_mode.Pump import Pump
from titration.utils.UIState.test_mode.ReadValues import ReadValues
from titration.utils.UIState.test_mode.ReadVolume import ReadVolume
from titration.utils.UIState.test_mode.SetVolume import SetVolume
from titration.utils.UIState.test_mode.ToggleTestMode import ToggleTestMode

class TestMode(UIState.UIState):
    def __init__(self, titrator, state):
        UIState.__init__('TestMode', titrator)
        self.titrator = titrator
        self.values = {'selection' : 0}
        self.subState = 1
        self.previousState = state

    def name(self):
        return 'TestMode'

    def handleKey(self, key):
        if self.subState == 1:
            if key == constants.KEY_STAR:
                self.subState += 1

            elif key == constants.KEY_1:
                self._setNextState(ReadValues(self.titrator, self), True)

            elif key == constants.KEY_2:
                self._setNextState(Pump(self.titrator, self), True)
            
            elif key == constants.KEY_3:
                self._setNextState(SetVolume(self.titrator, self), True)

        elif self.subState == 2:
            if key == constants.KEY_STAR:
                self.subState -= 1

            elif key == constants.KEY_4:
                self._setNextState(ToggleTestMode(self.titrator, self), True)

            elif key == constants.KEY_5:
                self._setNextState(ReadVolume(self.titrator, self), True)
            
            elif key == constants.KEY_6:
                self._setNextState(self.previousState, True)

    def loop(self):
        if self.subState == 1:
            LCD_interface.display_list(constants.TEST_OPTIONS_1)

        elif self.subState == 2:
            LCD_interface.display_list(constants.TEST_OPTIONS_2)
