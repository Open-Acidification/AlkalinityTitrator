"""
The file to demo the stir controller device
"""

from titration.devices.library import Keypad
from titration.ui_state.ui_state import UIState
from titration.ui_state.user_value.degas_time import DegasTime


class DemoStirControl(UIState):
    """
    The class to demo the stir controller device
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                1 -> Set Motor Speed to Fast
                2 -> Set Motor Speed to Slow
                3 -> Degas
                4 -> Return to Demo Mode Menu
            Substate 2:
                Any -> Substate 2
            D -> Return to Demo Mode Menu

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if self.substate == 1:
            if key == Keypad.KEY_1:
                self.titrator.stir_controller.set_fast()
                self.substate = 2
            elif key == Keypad.KEY_2:
                self.titrator.stir_controller.set_slow()
                self.substate = 3
            elif key == Keypad.KEY_3:
                self._set_next_state(DegasTime(self.titrator, self), True)
                self.titrator.stir_controller.degas(self.titrator.degas_time)
                self.substate = 4
            elif key == Keypad.KEY_4:
                self.titrator.stir_controller.set_stop()
                self._set_next_state(self.previous_state, True)

        else:
            self.titrator.stir_controller.set_stop()
            self.substate = 1

        if key == Keypad.KEY_D:
            self.titrator.stir_controller.set_stop()
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Set Fast Speed", line=1)
            self.titrator.lcd.print("2: Set Slow Speed", line=2)
            self.titrator.lcd.print("3: Degas", line=3)
            self.titrator.lcd.print("4: Return", line=4)

        elif self.substate == 2:
            self.titrator.lcd.print("Motor Speed", line=1)
            self.titrator.lcd.print("Set To Fast", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 3:
            self.titrator.lcd.print("Motor Speed", line=1)
            self.titrator.lcd.print("Set To Slow", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)

        elif self.substate == 4:
            self.titrator.lcd.print("Degassing", line=1)
            self.titrator.lcd.print("Solution", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("after degassing", line=4)
