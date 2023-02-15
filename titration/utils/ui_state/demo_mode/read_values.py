"""
The file for the ReadValues class
"""
from AlkalinityTitrator.titration.utils.ui_state.ui_state import UIState


class ReadValues(UIState):
    """
    This is a class for the ReadValues state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the temp, res, pH, volts, numVals, timeStep
    """

    def __init__(self, titrator, previous_state):
        """
        The constructor for the ReadValue class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last visited state
        """
        super().__init__(titrator, previous_state)
        self.values = {
            "temp": 1,
            "res": 1,
            "pH_reading": 1,
            "pH_volts": 1,
            "numVals": 20,
            "timeStep": 0.5,
        }

    def handle_key(self, key):
        """
        The function to handle keypad input. Any input will return you to the previous state

        Parameters:
            key (char): the keypad input is used to move to the next substate
        """
        self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        for i in range(self.values["numVals"]):
            self.titrator.lcd.clear()
            self.titrator.lcd.print(f"Temp: {self.values['temp']} C", line=1)
            self.titrator.lcd.print(f"Res:  {self.values['res']} Ohms", line=2)
            self.titrator.lcd.print(f"pH:   {self.values['pH_reading']} pH", line=3)
            self.titrator.lcd.print(
                f"pH V: {self.values['pH_volts'] * 1000} mV", line=4
            )
            self.titrator.lcd.print(f"Reading: {i}", 1, console=True)
        self.titrator.lcd.clear()
        self.titrator.lcd.print("Press any to cont", line=1)
        self.titrator.lcd.print("", line=2)
        self.titrator.lcd.print("", line=3)
        self.titrator.lcd.print("", line=4)
