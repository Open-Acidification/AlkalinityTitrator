"""
The file to demo the stir controller device
"""

from titration import constants
from titration.ui_state.ui_state import UIState


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
                4 -> Return to Demo Mode Menu
            Substate 2:
                Any -> Substate 2
            D -> Return to Demo Mode Menu

        Parameters:
            key (char): the keypad input to determine which state to go to
        """
        if self.substate == 1:
            if key == constants.KEY_1:
                self.titrator.stir_controller.motor_speed_fast()
                self.substate = 2
            elif key == constants.KEY_2:
                self.titrator.stir_controller.motor_speed_slow()
                self.substate = 3
            elif key == constants.KEY_4:
                self.titrator.stir_controller.motor_stop()
                self._set_next_state(self.previous_state, True)
        else:
            self.titrator.stir_controller.motor_stop()
            self.substate = 1

        if key == constants.KEY_D:
            self.titrator.stir_controller.motor_stop()
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: Set Fast Speed", line=1)
            self.titrator.lcd.print("2: Set Slow Speed", line=2)
            self.titrator.lcd.print("", line=3)
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
