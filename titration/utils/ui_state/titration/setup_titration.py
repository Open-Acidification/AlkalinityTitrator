"""
The file for the SetupTitration class
"""
from titration.utils.ui_state.ui_state import UIState
from titration.utils import constants
from titration.utils.ui_state.titration.initial_titration import InitialTitration
from titration.utils.ui_state.titration.calibrate_ph import CalibratePh
from titration.utils import lcd_interface
from titration.utils.ui_state.user_value.solution_weight import SolutionWeight
from titration.utils.ui_state.user_value.solution_salinity import SolutionSalinity


class SetupTitration(UIState):
    """
    This is a class for the SetupTitration state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the weight and salinity of the solution
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                Any -> Enter Solution weight
            Substate 2:
                Any -> Enter Solution salinity
            Substate 3:
                1 -> Calibrate pH probe
                Else -> Begin initial titration

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            self._set_next_state(SolutionWeight(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 2:
            self._set_next_state(SolutionSalinity(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 3:
            if key == constants.KEY_1:
                self._set_next_state(CalibratePh(self.titrator), True)
            else:
                self._set_next_state(InitialTitration(self.titrator), True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Enter Sol.", line=1)
            lcd_interface.lcd_out("weight (g)", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.substate == 2:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Enter Sol.", line=1)
            lcd_interface.lcd_out("salinity (ppt)", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.substate == 3:
            lcd_interface.lcd_clear()
            lcd_interface.lcd_out("Calibrate pH probe?", line=1)
            lcd_interface.lcd_out("Yes: 1", line=2)
            lcd_interface.lcd_out("No (use old): 0", line=3)
            lcd_interface.lcd_out(
                "{0:>2.3f} pH: {1:>2.4f} V".format(
                    constants.PH_REF_PH, constants.PH_REF_VOLTAGE
                ),
                line=4,
            )
