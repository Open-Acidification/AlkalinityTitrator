from titration.utils.ui_state import ui_state
from titration.utils import lcd_interface, interfaces, constants
from titration.utils.ui_state.titration.automatic_titration import AutomaticTitration
from titration.utils.ui_state.titration.manual_titration import ManualTitration


<<<<<<< HEAD:titration/utils/ui_state/titration/initial_titration.py
class InitialTitration(ui_state.UIState):
    def __init__(self, titrator):
        ui_state.__init__("InitialTitration", titrator)
=======
class InitialTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__("InitialTitration", titrator)
>>>>>>> upstream/main:titration/utils/UIState/titration/InitialTitration.py
        self.titrator = titrator
        self.choice = 0
        self.subState = 1

    def name(self):
        return "InitialTitration"

    def handleKey(self, key):
        if self.subState == 1:
            self.choice = key
            self.subState += 1

    def loop(self):
        if self.subState == 1:
            # Manual or automatic titration
            lcd_interface.lcd_out("Bring pH to 3.5:", line=1)
            lcd_interface.lcd_out("Manual: 1", line=2)
            lcd_interface.lcd_out("Automatic: 2", line=3)
            lcd_interface.lcd_out("Stir speed: slow", line=4)

        elif self.subState == 2:
            # Wait until solution is up to temperature
<<<<<<< HEAD:titration/utils/ui_state/titration/initial_titration.py
            lcd_interface.lcd_out("Heating to 30 C...", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out(
                "Please wait...", style=constants.LCD_CENT_JUST, line=3
            )
            lcd_interface.lcd_out("", line=4)
=======
            LCD_interface.lcd_out("Heating to 30 C...", line=1)
            LCD_interface.lcd_out("", line=2)
            LCD_interface.lcd_out(
                "Please wait...", style=constants.LCD_CENT_JUST, line=3
            )
            LCD_interface.lcd_out("", line=4)
>>>>>>> upstream/main:titration/utils/UIState/titration/InitialTitration.py

            while not interfaces.temperature_controller.at_temperature():
                interfaces.temperature_controller.update()
                temperature = interfaces.temperature_controller.get_last_temperature()
                lcd_interface.lcd_out(
                    "Temp: {0:>4.3f} C".format(temperature),
                    style=constants.LCD_CENT_JUST,
                    line=2,
                )
                break  # TODO: fix mock temperature controller and remove break

            if self.choice == constants.KEY_1:
                self._setNextState(ManualTitration(self.titrator), True)
            else:
                self._setNextState(AutomaticTitration(self.titrator), True)
