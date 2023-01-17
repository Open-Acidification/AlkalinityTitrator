"""
The file for the ReadValues class
"""
from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface, interfaces


class ReadValues(UIState):
    """
    This is a class for the ReadValues state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last state visited in the state machine
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictonary to hold the temp, res, pH, volts, numVals, timeStep
    """

    def __init__(self, titrator, previous_state):
        """
        The constructor for the ReadValue class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
            previous_state (UIState object): the previous_state is used to return the last state visited in the state machine
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
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out(
                "Temp: {0:>4.3f} C".format(self.values["temp"]), line=1
            )
            lcd_interface.lcd_out(
                "Res:  {0:>4.3f} Ohms".format(self.values["res"]), line=2
            )
            lcd_interface.lcd_out(
                "pH:   {0:>4.5f} pH".format(self.values["pH_reading"]), line=3
            )
            lcd_interface.lcd_out(
                "pH V: {0:>3.4f} mV".format(self.values["pH_volts"] * 1000), line=4
            )
            lcd_interface.lcd_out("Reading: {}".format(i), 1, console=True)
            interfaces.delay(self.values["timeStep"])
        lcd_interface.lcd_clear()
        lcd_interface.lcd_out("Press any to cont", line=1)
        lcd_interface.lcd_out("", line=2)
        lcd_interface.lcd_out("", line=3)
        lcd_interface.lcd_out("", line=4)
