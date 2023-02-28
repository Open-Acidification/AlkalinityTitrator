"""
The file to for the UpdateSetting class
"""

from titration import constants
from titration.ui_state.ui_state import UIState
from titration.ui_state.update_settings.set_gain import SetGain
from titration.ui_state.user_value.ph_ref_ph import PHRefpH
from titration.ui_state.user_value.ph_ref_voltage import PHRefVoltage
from titration.ui_state.user_value.temp_nom_resistance import TempNomResistance
from titration.ui_state.user_value.temp_ref_resistance import TempRefResistance


DEFAULT_TEMPERATURE_REF_RESISTANCE = 4300.0
DEFAULT_TEMPERATURE_NOMINAL_RESISTANCE = 1000.0
DEFAULT_PH_REF_VOLTAGE = -0.012
DEFAULT_PH_REF_PH = 7.0


class UpdateSettings(UIState):
    """
    This is a class for the UpdateSettings state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
    """

    def handle_key(self, key):
        """
        The function to respond to a keypad input:
            Substate 1:
                1 -> View Current Settings
                2 -> Reset to Default Settings
                3 -> Set Temperature Probe Reference Resistance
                4 -> Page 2
            Substate 2:
                1 -> Set Temperature Probe Nominal Resistance
                2 -> Set pH Probe Reference Voltage
                3 -> Set pH Probe Reference pH
                4 -> Page 3
            Substate 3:
                1 -> Set Gain
                4 -> Page 1
            D -> Return to Main Menu

        Parameters:
            key (char): the keypad input is used to move through the substates
        """
        if self.substate == 1:
            if key == constants.KEY_1:
                self.substate = 4
            elif key == constants.KEY_2:
                constants.TEMPERATURE_REF_RESISTANCE = (
                    DEFAULT_TEMPERATURE_REF_RESISTANCE
                )
                constants.TEMPERATURE_NOMINAL_RESISTANCE = (
                    DEFAULT_TEMPERATURE_NOMINAL_RESISTANCE
                )
                constants.PH_REF_VOLTAGE = DEFAULT_PH_REF_VOLTAGE
                constants.PH_REF_PH = DEFAULT_PH_REF_PH
                self.substate = 5
            elif key == constants.KEY_3:
                self._set_next_state(TempRefResistance(self.titrator, self), True)
            elif key == constants.KEY_4:
                self.substate = 2

        elif self.substate == 2:
            if key == constants.KEY_1:
                self._set_next_state(TempNomResistance(self.titrator, self), True)
            if key == constants.KEY_2:
                self._set_next_state(PHRefVoltage(self.titrator, self), True)
            elif key == constants.KEY_3:
                self._set_next_state(PHRefpH(self.titrator, self), True)
            elif key == constants.KEY_4:
                self.substate = 3

        elif self.substate == 3:
            if key == constants.KEY_1:
                self._set_next_state(SetGain(self.titrator, self), True)
            elif key == constants.KEY_4:
                self.substate = 1

        else:
            self.substate = 1

        if key == constants.KEY_D:
            self._set_next_state(self.previous_state, True)

    def loop(self):
        """
        The function to loop through and display to the LCD screen until a new keypad input
        """
        if self.substate == 1:
            self.titrator.lcd.print("1: View Settings", line=1)
            self.titrator.lcd.print("2: Default Settings", line=2)
            self.titrator.lcd.print("3: T Ref Resistance", line=3)
            self.titrator.lcd.print("4: Page 2", line=4)

        if self.substate == 2:
            self.titrator.lcd.print("1: T Nom Resistance", line=1)
            self.titrator.lcd.print("2: pH Ref Voltage", line=2)
            self.titrator.lcd.print("3: pH Ref pH", line=3)
            self.titrator.lcd.print("4: Page 3", line=4)

        if self.substate == 3:
            self.titrator.lcd.print("1: Set Gain", line=1)
            self.titrator.lcd.print("", line=2)
            self.titrator.lcd.print("", line=3)
            self.titrator.lcd.print("4: Page 1", line=4)

        if self.substate == 4:
            self.titrator.lcd.print(
                f"T Ref Res: {constants.TEMPERATURE_REF_RESISTANCE}", line=1
            )
            self.titrator.lcd.print(
                f"T Nom Res: {constants.TEMPERATURE_NOMINAL_RESISTANCE}", line=2
            )
            self.titrator.lcd.print(f"pH Ref Vol: {constants.PH_REF_VOLTAGE}", line=3)
            self.titrator.lcd.print(f"pH Ref pH: {constants.PH_REF_PH}", line=4)

        if self.substate == 5:
            self.titrator.lcd.print("Default Constants", line=1)
            self.titrator.lcd.print("Restored", line=2)
            self.titrator.lcd.print("Press any to cont.", line=3)
            self.titrator.lcd.print("", line=4)
