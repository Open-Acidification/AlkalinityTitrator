"""
The file for the UserValue class
"""
from AlkalinityTitrator.titration.utils.ui_state.ui_state import UIState
from AlkalinityTitrator.titration.utils import constants


class UserValue(UIState):
    """
    This is a class for the UserValue state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        value (string): the value is used to hold the user input
    """

    def __init__(self, titrator, previous_state):
        """
        The constructor for the UserValue state

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last visited state
        """
        super().__init__(titrator, previous_state)
        self.value = ""

    def save_value(self, value):
        """
        The function to save photometer values
        """
        raise Exception(self.name() + " requires a save_value function")

    def get_label(self):
        """
        The function to return the label printed on the LCD Screen
        """
        raise Exception(self.name() + " requires a get_label function")

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            A -> Save value and return to previous state
            B -> Backspace on the entered user value
            C -> Clear currently entered user value
            D -> Return to previous state without saving a new value
            * -> Enters a decimal point to be appended to new user value
                - Only if there is not already a decimal point
            [0-9] -> Enter a number to be appended to new user value

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if key == "A":
            self._set_next_state(self.previous_state, True)
            self.save_value(self.value)

        elif key == "B":
            self.value = self.value[:-1]

        elif key == "C":
            self.value = ""

        elif key == "D":
            self._set_next_state(self.previous_state, True)

        elif key == "*":
            if "." not in self.value:
                self.value = self.value + "."

        elif str(key).isdigit():
            self.value = self.value + str(key)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        self.titrator.lcd.clear()
        self.titrator.lcd.print(self.get_label(), line=1)
        self.titrator.lcd.print(self.value, style=constants.LCD_CENT_JUST, line=2)
        self.titrator.lcd.print("* = .       B = BS", line=3)
        self.titrator.lcd.print("A = accept  C = Clr", line=4)
