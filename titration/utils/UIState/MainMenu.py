from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.titration import SetupTitration
from titration.utils.UIState.calibration import SetupCalibration

# TODO: remove unecessary lcd_outs
class MainMenu (UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('MainMenu', titrator)
        self.routineSelection = 1
        self.titrator = titrator

    def name(self):
        return 'MainMenu'

    def handleKey(self, key):
        # Substate 1 key handle
        if self.routineSelection == 1:
            if key == '*' or key is constants.KEY_STAR:
                self.routineSelection = 2

            elif key == 1 or key is constants.KEY_1:
                # Next state SetupTitration
                self._setNextState(SetupTitration.SetupTitration(self.titrator), True)

            elif key == 2 or key is constants.KEY_2:
                # Next state SetupCalibration
                self._setNextState(SetupCalibration.SetupCalibration(self.titrator, self), True)

            elif key == 3 or key is constants.KEY_3:
                # prime pump
                pass

        # Substate 2 key handle
        else:
            if key == '*' or key is constants.KEY_STAR:
                self.routineSelection = 1

            elif key == 4 or key is constants.KEY_4:
                # update settings
                pass

            elif key == 5 or key is constants.KEY_5:
                # test mode
                pass

            elif key == 6 or key is constants.KEY_6:
                # exit
                pass

    def loop(self):
        # Substate 1 output
        if self.routineSelection == 1:
            interfaces.display_list(constants.ROUTINE_OPTIONS_1)
            
        # Substate 2 output
        else:
            interfaces.display_list(constants.ROUTINE_OPTIONS_2)
