from titration.utils.UIState import UIState
from titration.utils import LCD_interface, constants
from titration.utils.UIState import MainMenu
from titration.utils.UIState.user_value.UserValue import UserValue


class ManualTitration(UIState.UIState):
    def __init__(self, titrator):
        UIState.__init__("ManualTitration", titrator)
        self.titrator = titrator
        self.values = {
            "p_volume": 0,
            "p_direction": 0,
            "degas_time": 0,
            "current_pH": 5,
        }
        self.subState = 1

    def name(self):
        return "ManualTitration"

    def handleKey(self, key):
        if self.subState == 1:
            self._setNextState(UserValue(self.titrator, self, "Volume:"), True)
            self.subState += 1

        elif self.subState == 2:
            self.values["p_direction"] = key
            self.subState += 1

        elif self.subState == 3:
            if key == constants.KEY_1:
                self.subState -= 1
            else:
                self.subState += 1

        elif self.subState == 4:
            if key == constants.KEY_0:
                self.subState += 2
            elif key == constants.KEY_1:
                self.subState += 1

        elif self.subState == 5:
            self._setNextState(UserValue(self.titrator, self, "Degas time (s):"), True)
            self.subState += 1

        elif self.subState == 6:
            self._setNextState(
                MainMenu.MainMenu(self.titrator), True
            )  # TODO; pop back up

    def loop(self):
        if self.subState == 1:
            LCD_interface.lcd_out("Enter Volume", line=1)
            LCD_interface.lcd_out("", line=2)
            LCD_interface.lcd_out("Press any to cont", line=3)
            LCD_interface.lcd_out("", line=4)

        elif self.subState == 2:
            LCD_interface.lcd_out("Direction (0/1):", line=1)
            LCD_interface.lcd_out("", line=2)
            LCD_interface.lcd_out("", line=3)
            LCD_interface.lcd_out("", line=4)

        elif self.subState == 3:
            LCD_interface.lcd_out(
                "Current pH: {0:>4.5f}".format(self.values["current_pH"]), line=1
            )  # TODO: change current pH value from 5
            LCD_interface.lcd_out("Add more HCl?", line=2)
            LCD_interface.lcd_out("(0 - No, 1 - Yes)", line=3)
            LCD_interface.lcd_out("", line=4)

        elif self.subState == 4:
            LCD_interface.lcd_out(
                "Current pH: {0:>4.5f}".format(self.values["current_pH"]), line=1
            )  # TODO: change current pH value from 5
            LCD_interface.lcd_out("Degas?", line=2)
            LCD_interface.lcd_out("(0 - No, 1 - Yes)", line=3)
            LCD_interface.lcd_out("", line=4)

        elif self.subState == 5:
            LCD_interface.lcd_out("Enter Degas time", line=1)
            LCD_interface.lcd_out("", line=2)
            LCD_interface.lcd_out("Press any to cont", line=3)
            LCD_interface.lcd_out("", line=4)

        elif self.subState == 6:
            LCD_interface.lcd_out("Return to", line=1)
            LCD_interface.lcd_out("main menu", line=2)
            LCD_interface.lcd_out(
                "Press any to cont", line=3
            )  # TODO: change exit and go to main menu
            LCD_interface.lcd_out("", line=4)

    def start(self):
        LCD_interface.lcd_out("MANUAL SELECTED", style=constants.LCD_CENT_JUST, line=4)
