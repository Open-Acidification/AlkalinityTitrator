from titration.utils import lcd_interface, constants
from titration.utils.ui_state import main_menu


class AutomaticTitration:
    def __init__(self, titrator):
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
            self.titrator.updateState(main_menu.MainMenu(self.titrator))

    def loop(self):
        if self.subState == 1:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out(
                "Titrating to {} pH".format(
                    str(self.values["pH_target"])
                ),  # TODO: Change pH_target
                line=1,
            )
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 2:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Mixing...", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 3:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out(
                "pH value {} reached".format(self.values["current_pH"]), line=1
            )  # TODO: Change current_pH
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 4:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Return to", line=1)
            lcd_interface.lcd_out("main menu", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)
