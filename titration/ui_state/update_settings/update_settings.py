"""
The file to for the UpdateSetting class
"""
from titration.ui_state.ui_state import UIState
from titration.ui_state.user_value.pump_volume import PumpVolume


class UpdateSettings(UIState):
    """
    This is a class for the UpdateSettings state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the volume in the pump
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                Y -> Reset calibration settings to default
                N -> Do not reset calibration settings to default
            Substate 2:
                Any -> To continue
            Substate 3:
                Y -> Set volume in pump
                N -> Do not set volume in pump
            Substate 4:
                Any -> Enter user value state to set volume in pump
            Substate 5:
                Any -> Return to previous state

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            if key not in ("n", "N"):
                self.substate += 1
            else:
                self.substate += 2

        elif self.substate == 2:
            self.substate += 1

        elif self.substate == 3:
            if key not in ("n", "N"):
                self.substate += 1
            else:
                self._set_next_state(self.previous_state, True)

        elif self.substate == 4:
            self._set_next_state(PumpVolume(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 5:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("Reset calibration", line=1)
            self.titrator.lcd.print("settings to default?", line=2)
            self.titrator.lcd.print("(y/n)", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Default constants", line=1)
            self.titrator.lcd.print("restored", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Set volume in pump?", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("(y/n)", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 4:
            self.titrator.lcd.print("Enter Volume in pump", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 5:
            self.titrator.lcd.print("Volume in pump set", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont", line=3)
            self.titrator.lcd.print("", line=4)
