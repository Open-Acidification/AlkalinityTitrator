from sre_parse import State
from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.titration.InitialTitration import InitialTitration

class CalibratePh(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('CalibratePh', titrator)
        self.titrator = titrator
        self.values = {'buffer1_measured_volts' : 5, 'buffer1_actual_pH' : 0}
        self.subState = 1

    def name(self):
        return 'CalibratePh'

    def handleKey(self, key):
        # Substate 2 key handle
        if self.subState == 2:
            self._setNextState(InitialTitration(self.titrator), True)    # TODO: Does not return

    def loop(self):
        # Substate 1 output and input
        if self.subState == 1:
            self.values['buffer1_actual_pH'] = interfaces.read_user_value("Enter buffer pH:")
            interfaces.lcd_out("Put sensor in buffer", style=constants.LCD_CENT_JUST, line=1)
            interfaces.lcd_out("", line=2)
            interfaces.lcd_out("Press any button", style=constants.LCD_CENT_JUST, line=3)
            interfaces.lcd_out("to record value", style=constants.LCD_CENT_JUST, line=4)
            self.subState += 1

        # Substate 2 output
        elif self.subState == 2:
            interfaces.lcd_clear()
            interfaces.lcd_out("Recorded pH and volts:", line=1)
            interfaces.lcd_out(
                "{0:>2.5f} pH, {1:>3.4f} V".format(self.values['buffer1_actual_pH'], self.values['buffer1_measured_volts']),
                line=2,
            )
            interfaces.lcd_out("Press any button", style=constants.LCD_CENT_JUST, line=3)
            interfaces.lcd_out("to continue", style=constants.LCD_CENT_JUST, line=4)
