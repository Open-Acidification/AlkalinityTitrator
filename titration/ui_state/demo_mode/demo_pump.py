"""
The file to demo the pump device
"""

from titration.devices.library import Keypad
from titration.ui_state.ui_state import UIState
from titration.ui_state.user_value.pump_volume import PumpVolume


class DemoPump(UIState):
    """
    The class to demo the pump
    """

    def handle_key(self, key):
        """
        The function to handle keypad input:
            Substate 1:
                1 -> Get Pump Volume
                2 -> Get Added Volume
                3 -> Clear Added Volume
                4 -> Go to 2nd page of options
            Substate 2:
                1 -> Fill Pump
                2 -> Empty Pump
                3 -> Pull Volume
                4 -> Go to 3rd page of options
            Substate 3:
                1 -> Push Volume
                4 -> Go to 1st page
            Substate 4, 5, 6:
                Any -> Substate 1
            Substate 7, 8, 9:
                Any -> Substate 2
            Substate 10:
                Any -> Substate 3
            D -> Return to Demo Mode Menu

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            if key == Keypad.KEY_1:
                self.substate = 4
            elif key == Keypad.KEY_2:
                self.substate = 5
            elif key == Keypad.KEY_3:
                self.substate = 6
            elif key == Keypad.KEY_4:
                self.substate = 2

        elif self.substate == 2:
            if key == Keypad.KEY_1:
                self.titrator.pump.fill()
                self.substate = 7
            elif key == Keypad.KEY_2:
                self.titrator.pump.empty()
                self.substate = 8
            elif key == Keypad.KEY_3:
                self._set_next_state(PumpVolume(self.titrator, self), True)
                self.titrator.pump.pump_out(self.titrator.volume)
                self.substate = 9
            elif key == Keypad.KEY_4:
                self.substate = 3

        elif self.substate == 3:
            if key == Keypad.KEY_1:
                self._set_next_state(PumpVolume(self.titrator, self), True)
                self.titrator.pump.pump_in(self.titrator.volume)
                self.substate = 10
            if key == Keypad.KEY_4:
                self.substate = 1

        elif self.substate in (4, 5, 6):
            self.substate = 1

        elif self.substate in (7, 8, 9):
            self.substate = 2

        elif self.substate == 10:
            self.substate = 3

        if key == Keypad.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Get Volume", line=1)
            self.titrator.lcd.print("2: Set Volume", line=2)
            self.titrator.lcd.print("3: Zero Added Volume", line=3)
            self.titrator.lcd.print("4: Page 2", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("1: Fill Pump", line=1)
            self.titrator.lcd.print("2: Empty Pump", line=2)
            self.titrator.lcd.print("3: Pump In", line=3)
            self.titrator.lcd.print("4: Page 3", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("1: Pump Out", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("4: Page 1", line=4)

        elif self.substate == 4:
            self.titrator.lcd.print("Pump Volume:", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.pump.get_pump_volume()} ml", line=2, style="center"
            )
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 5:
            self.titrator.lcd.print("Added Volume:", line=1)
            self.titrator.lcd.print(
                f"{self.titrator.pump.get_added_volume()} ml", line=2, style="center"
            )
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 6:
            self.titrator.lcd.print("Cleared", line=1, style="center")
            self.titrator.lcd.print("Added Volume", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 7:
            self.titrator.lcd.print("Filling Pump", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 8:
            self.titrator.lcd.print("Emptying Pump", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 9:
            self.titrator.lcd.print("Pumping Volume In", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 10:
            self.titrator.lcd.print("Pumping Volume Out", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)
