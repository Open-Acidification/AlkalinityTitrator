"""
The file to hold the CalibratePh class
"""
from titration.utils.ui_state.ui_state import UIState
from titration.utils import lcd_interface
from titration.utils.ui_state.titration.initial_titration import InitialTitration
from titration.utils.ui_state.user_value.user_value import UserValue


class CalibratePh(UIState):
    """
    This is a class for the CalibratePh state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the buffer's measured volts and actual pH
    """

    def __init__(self, titrator):
        """
        The constructor for the CalibratePh class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
        """
        super().__init__(titrator)
        self.values = {"buffer1_measured_volts": 5, "buffer1_actual_pH": 0}

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                Any -> Enter UserValue state to set buffer pH
            Substate 2:
                Any -> To continue (Put probe in solution first)
            Substate 3:
                Any -> Begin initial titration

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self._set_next_state(
                UserValue(self.titrator, self, "Enter buffer pH:"), True
            )
            self.substate += 1

        elif self.substate == 2:
            self.substate += 1

        elif self.substate == 3:
            self._set_next_state(InitialTitration(self.titrator), True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Enter buffer pH", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.substate == 2:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Put sensor in buffer", line=1)
            lcd_interface.lcd_out("", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.substate == 3:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Recorded pH, volts:", line=1)
            lcd_interface.lcd_out(
                "{0:>2.5f} pH, {1:>3.4f} V".format(
                    self.values["buffer1_actual_pH"],
                    self.values["buffer1_measured_volts"],
                ),
                line=2,
            )
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)
