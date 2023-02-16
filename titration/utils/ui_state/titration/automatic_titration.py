"""
The file for the AutomaticTitration class
"""

# pylint: disable=E1101

from titration.utils.ui_state.ui_state import UIState
from titration.utils.ui_state import main_menu


class AutomaticTitration(UIState):
    """
    This is a class for the AutomaticTitration state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the pH_target and current_pH
    """

    def __init__(self, titrator):
        """
        The constructor for the AutomaticTitration class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
        """
        super().__init__(titrator)
        self.values = {"pH_target": 5, "current_pH": 5}

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                Any -> To continue after titrating
            Substate 2:
                Any -> To continue after mixing
            Substate 3:
                Any -> To continue after showing the pH value reached
            Substate 4:
                Any -> To return to main menu

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self.substate += 1

        elif self.substate == 2:
            self.substate += 1

        elif self.substate == 3:
            self.substate += 1

        elif self.substate == 4:
            self._set_next_state(main_menu.MainMenu(self.titrator), True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.clear()
            self.titrator.lcd.print(
                f"Titrating to {self.values['pH_target']} pH",
                line=1,
            )
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("Mixing...", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 3:
            self.titrator.lcd.clear()
            self.titrator.lcd.print(
                f"pH value {self.values['current_pH']} reached", line=1
            )
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 4:
            self.titrator.lcd.clear()
            self.titrator.lcd.print("Return to", line=1)
            self.titrator.lcd.print("main menu", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

    def start(self):
        """
        The function to display AUTO SELECTED upon entering the AutomaticTitration state
        """
        self.titrator.lcd.print("AUTO SELECTED", style="center", line=4)
