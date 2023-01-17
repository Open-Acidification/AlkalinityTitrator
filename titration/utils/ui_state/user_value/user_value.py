"""
The file for the UserValue class
"""
from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, constants


class UserValue(UIState):
    """
    This is a class for the UserValue state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last state visited in the state machine
        substate (int): the substate is used to keep track of substate of the UIState
        message (string): the message is used to display what setting you are entering
        string (string): the string is used to hold the user input
    """

    def __init__(self, titrator, previous_state, message):
        """
        The constructor for the UserValue state

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last state visited in the state machine
            message (string): the message is used to display what setting you are entering
        """
        super().__init__(titrator, previous_state)
        self.message = message
        self.string = ""

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

        elif key == "B":
            self.string = self.string[:-1]

        elif key == "C":
            self.string = ""

        elif key == "*":
            if "." not in self.string:
                self.string = self.string + "."

        elif key.isnumeric():
            self.string = self.string + str(key)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        lcd_interface.lcd_clear()
        lcd_interface.lcd_out(self.message, line=1)
        lcd_interface.lcd_out(self.string, style=constants.LCD_CENT_JUST, line=2)
        lcd_interface.lcd_out("* = .       B = BS", line=3)
        lcd_interface.lcd_out("A = accept  C = Clr", line=4)
