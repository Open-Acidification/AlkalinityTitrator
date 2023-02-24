"""
The file for the Pump class
"""
from titration import constants
from titration.ui_state.ui_state import UIState
from titration.ui_state.user_value.pump_volume import PumpVolume


class Pump(UIState):
    """
    This is a class for the Pump state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the probe direction
    """

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                Any -> Set the Volume, Display Set Volume
            Substate 2:
                Any -> Set the Probe Direction
            Substate 3:
                0 or 1 -> Display Probe Direction
            Substate 3:
                Any -> Return to previous state

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self._set_next_state(PumpVolume(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 2:
            self.substate += 1

        elif self.substate == 3:
            if key in (constants.KEY_0, constants.KEY_1):
                self.titrator.pump.set_pump_direction(key)
                self.substate += 1

        elif self.substate == 4:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("Set Volume", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Pumping Volume Set To:", line=1)
            self.titrator.lcd.print(f"{self.titrator.pump_volume}", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Set Pump Direction", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("In/Out (0/1):", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 4:
            self.titrator.lcd.print("Pump Direction Set To:", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.pump.get_pump_direction()}", line=2
            )
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)
