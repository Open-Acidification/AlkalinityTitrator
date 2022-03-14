from titration.utils.UIState import UIState
from titration.utils import interfaces, constants

class CalibrateTemp(UIState.UIState):
    def __init__(self, titrator, state):
        UIState.__init__('CalibrateTemp', titrator)
        self.titrator = titrator
        self.subState = 1
        self.values = {'actual_temperature' : 5, 'new_ref_resistance' : 5,
        'expected_temperature' : 0}
        self.previousState = state

    def name(self):
        return 'CalibrateTemp'

    def handleKey(self, key):
        # Substate 2 key handle
        if self.subState == 2:
            if key == 1 or key == constants.KEY_1:
                self.subState += 1

        # Substate 3 key handle
        elif self.subState == 3:
            self._setNextState(self.previousState, True)

    def loop(self):
        # Substate 1 output and input
        if self.subState == 1:
            self.values['expected_temperature'] = interfaces.read_user_value("Ref solution temp?")
            self.subState += 1
        
        # Substate 2 output
        elif self.subState == 2:
            interfaces.lcd_out("Put probe in sol", style=constants.LCD_CENT_JUST, line=1)
            interfaces.lcd_out("", line=2)
            interfaces.lcd_out("Press 1 to", style=constants.LCD_CENT_JUST, line=3)
            interfaces.lcd_out("record value", style=constants.LCD_CENT_JUST, line=4)

        # Substate 3 output
        elif self.subState == 3:
            interfaces.lcd_clear()
            interfaces.lcd_out("Recorded temp:", line=1)
            interfaces.lcd_out("{0:0.3f}".format(self.values['actual_temperature']), line=2)
            # reinitialize sensors with calibrated values
            interfaces.lcd_out("{}".format(self.values['new_ref_resistance']), line=3)
