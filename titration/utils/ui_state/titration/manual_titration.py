"""
The file for the ManualTitration class
"""
from AlkalinityTitrator.titration.utils.ui_state.ui_state import UIState
from AlkalinityTitrator.titration.utils import constants
from AlkalinityTitrator.titration.utils.ui_state import main_menu
from AlkalinityTitrator.titration.utils.ui_state.user_value.volume import Volume
from AlkalinityTitrator.titration.utils.ui_state.user_value.degas_time import DegasTime


class ManualTitration(UIState):
    """
    This is a class for the ManualTitration state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the volume, direction, degas time, and current pH
    """

    def __init__(self, titrator):
        """
        The constructor for the ManualTitration class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
        """
        super().__init__(titrator)
        self.values = {
            "p_direction": 0,
            "current_pH": 5,
        }

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                Any -> Enter UserValue state to set volume
            Substate 2:
                Any -> Set p_direction
            Substate 3:
                1 -> Add more HCL
                0 -> Do not add more HCL
            Substate 4:
                1 -> Set degas
                0 -> Do not set degas
            Substate 5:
                Any -> Enter UserValue to set the degas value
            Substate 6:
                Any -> Return to main menu

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self._set_next_state(Volume(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 2:
            self.values["p_direction"] = key
            self.substate += 1

        elif self.substate == 3:
            if key == constants.KEY_1:
                self.substate -= 1
            elif key == constants.KEY_0:
                self.substate += 1

        elif self.substate == 4:
            if key == constants.KEY_0:
                self.substate += 2
            elif key == constants.KEY_1:
                self.substate += 1

        elif self.substate == 5:
            self._set_next_state(DegasTime(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 6:
            self._set_next_state(main_menu.MainMenu(self.titrator), True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("Enter Volume", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("Direction (0/1):", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 3:
            self.titrator.lcd.clear()
            self.titrator.lcd.print(f"Current pH: {self.values['current_pH']}", line=1)
            self.titrator.lcd.print("Add more HCl?", line=2)
            self.titrator.lcd.print("(0 - No, 1 - Yes)", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 4:
            self.titrator.lcd.clear()
            self.titrator.lcd.print(f"Current pH: {self.values['current_pH']}", line=1)
            self.titrator.lcd.print("Degas?", line=2)
            self.titrator.lcd.print("(0 - No, 1 - Yes)", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 5:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("Enter Degas time", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 6:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("Return to", line=1)
            self.titrator.lcd.print("main menu", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

    def start(self):
        """
        The function to display MANUAL SELECTED upon entering the ManualTitration state
        """
        self.titrator.lcd.print(
            "MANUAL SELECTED", style=constants.LCD_CENT_JUST, line=4
        )
