"""
The file to demo the pump device
"""

from titration.devices.library import Keypad
from titration.ui_state.ui_state import UIState
from titration.ui_state.user_value.pump_volume import PumpVolume
from titration.ui_state.user_value.volume_to_move import VolumeToMove


class DemoPump(UIState):
    """
    The class to demo the pump
    """

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                1 -> Get Volume
                2 -> Set Volume
                3 -> Pull Volume in to Pump
                4 -> Go to 2nd page of options
            Substate 2:
                1 -> Pump Volume out into Solution
                4 -> Go to 1st page of options
            Substate 3:
                Any -> Substate 1
            Substate 4:
                Any -> Substate 1
            D -> Return to Demo Mode Menu

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            if key == Keypad.KEY_1:
                self.substate = 3

            elif key == Keypad.KEY_2:
                self._set_next_state(PumpVolume(self.titrator, self), True)
                self.substate = 3

            elif key == Keypad.KEY_3:
                self._set_next_state(VolumeToMove(self.titrator, self), True)
                self.titrator.pump.pull_volume_in(self.titrator.volume_to_move)
                self.titrator.volume_to_move = 0
                self.substate = 3

            elif key == Keypad.KEY_4:
                self.substate = 2

        elif self.substate == 2:
            if key == Keypad.KEY_1:
                self._set_next_state(VolumeToMove(self.titrator, self), True)
                self.titrator.pump.push_volume_out(self.titrator.volume_to_move)
                self.titrator.volume_to_move = 0
                self.substate = 3

            elif key == Keypad.KEY_4:
                self.substate = 1

        elif self.substate == 3:
            self.substate = 1

        if key == Keypad.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Get Volume", line=1)
            self.titrator.lcd.print("2: Set Volume", line=2)
            self.titrator.lcd.print("3: Pull Volume In", line=3)
            self.titrator.lcd.print("4: Page 2", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("1: Push Volume Out", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("4: Page 1", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Pump Volume:", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.pump.get_volume_in_pump()} ml", line=2, style="center"
            )
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("Any key to continue", line=4)
