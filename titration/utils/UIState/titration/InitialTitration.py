from titration.utils.UIState import UIState
from titration.utils import interfaces, constants
from titration.utils.UIState.titration.AutomaticTitration import AutomaticTitration
from titration.utils.UIState.titration.ManualTitration import ManualTitration

class InitialTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__('InitialTitration', titrator)
        self.titrator = titrator
        self.value = 0
        self.subState = 1

    def name(self):
        return 'InitialTitration'

    def handleKey(self, key):
        # Substate 1 key handle
        if self.subState == 1:
            self.value = key
            self.subState += 1

    def loop(self):
        # Substate 1 output
        if self.subState == 1:
            # Manual or automatic titration
            interfaces.lcd_out("Bring pH to 3.5:", line=1)
            interfaces.lcd_out("Manual: 1", line=2)
            interfaces.lcd_out("Automatic: 2", line=3)
            interfaces.lcd_out("Stir speed: slow", line=4)

        # Substate 2 output
        elif self.subState == 2:
            # wait until solution is up to temperature
            interfaces.lcd_clear()
            interfaces.lcd_out("Heating to 30 C...", line=1)
            interfaces.lcd_out("Please wait...", style=constants.LCD_CENT_JUST, line=3)

            if self.value == 1 or self.value == constants.KEY_1:
                # Next state ManutalTitration
                self._setNextState(ManualTitration(self.titrator), False)
            else:
                # Next state AutomaticTitration
                self._setNextState(AutomaticTitration(self.titrator), False)

            while not interfaces.temperature_controller.at_temperature():
                interfaces.temperature_controller.update()
                temperature = interfaces.temperature_controller.get_last_temperature()
                interfaces.lcd_out(
                    "Temp: {0:>4.3f} C".format(temperature),
                    style=constants.LCD_CENT_JUST,
                    line=2,
                )
                break                               # TODO: fix mock temperature controller

