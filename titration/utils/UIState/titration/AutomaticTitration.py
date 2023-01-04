from titration.utils.UIState import UIState
from titration.utils import LCD_interface, constants
from titration.utils.UIState import MainMenu


class AutomaticTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__("AutomaticTitration", titrator)
        self.titrator = titrator
        self.values = {"pH_target": 5, "current_pH": 5}
        self.subState = 1

    def name(self):
        return "AutomaticTitration"

    def handleKey(self, key):
        if self.subState == 1:
            self.subState += 1

        elif self.subState == 2:
            self.subState += 1

        elif self.subState == 3:
            self.subState += 1

        elif self.subState == 4:
            self._setNextState(MainMenu.MainMenu(self.titrator), True)

    def loop(self):
        if self.subState == 1:
            LCD_interface.lcd_out(
                "Titrating to {} pH".format(
                    str(self.values["pH_target"])
                ),  # TODO: Change pH_target
                line=1,
            )
            LCD_interface.lcd_out("", line=2)
            LCD_interface.lcd_out("Press any to cont", line=3)
            LCD_interface.lcd_out("", line=4)

        elif self.subState == 2:
            LCD_interface.lcd_out("Mixing...", line=1)
            LCD_interface.lcd_out("", line=2)
            LCD_interface.lcd_out("Press any to cont", line=3)
            LCD_interface.lcd_out("", line=4)

        elif self.subState == 3:
            LCD_interface.lcd_out(
                "pH value {} reached".format(self.values["current_pH"]), line=1
            )  # TODO: Change current_pH
            LCD_interface.lcd_out("", line=2)
            LCD_interface.lcd_out("Press any to cont", line=3)
            LCD_interface.lcd_out("", line=4)

        elif self.subState == 4:
            LCD_interface.lcd_out("Return to", line=1)
            LCD_interface.lcd_out("main menu", line=2)
            LCD_interface.lcd_out("Press any to cont", line=3)
            LCD_interface.lcd_out("", line=4)

    def start(self):
        LCD_interface.lcd_out("AUTO SELECTED", style=constants.LCD_CENT_JUST, line=4)
