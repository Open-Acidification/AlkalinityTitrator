from titration.utils.UIState import UIState, RunTitration
from titration.utils import interfaces, constants

class MainMenu (UIState.UIState):
    def __init__(self, tc):
        UIState.__init__('MainMenu', tc)
        self.routineSelection = 1
        self.tc = tc


    def handleKey(self, key):
        if self.routineSelection == 1:
            if key is constants.KEY_STAR:
                self.routineSelection = 2

            elif key is constants.KEY_1:
                # Run titration.
                interfaces.lcd_out('Run titration', 1)
                self._setNextState(RunTitration.RunTitration(self.tc))

            elif key is constants.KEY_2:
                interfaces.lcd_out('Calibrate sensors', 1)

            elif key is constants.KEY_3:
                interfaces.lcd_out('Prime Pump', 1)

        else:
            if key is constants.KEY_STAR:
                self.routineSelection = 1

            elif key is constants.KEY_4:
                interfaces.lcd_out('Update settings', 1)

            elif key is constants.KEY_5:
                interfaces.lcd_out('Test Mode', 1)

            elif key is constants.KEY_6:
                interfaces.lcd_out('Exit', 1)


    def name(self):
        return 'MainMenu'


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
        self.tc.setNextState(state, True)
