from titration.utils import constants
from titration.utils.ui_state.titration.initial_titration import InitialTitration
from titration.utils.ui_state.titration.calibrate_ph import CalibratePh
from titration.utils import lcd_interface
from titration.utils.ui_state.user_value.user_value import UserValue


class SetupTitration:
    def __init__(self, titrator):
        self.titrator = titrator
        self.values = {"weight": 0, "salinity": 0}
        self.subState = 1

    def name(self):
        return "SetupTitration"

    def handleKey(self, key):
        if self.subState == 1:
            self.titrator.updateState(
                UserValue(self.titrator, self, "Sol. weight (g):")
            )
            self.subState += 1

        elif self.subState == 2:
            self.titrator.updateState(
                UserValue(self.titrator, self, "Sol. salinity (ppt):")
            )
            self.subState += 1

        elif self.subState == 3:
            if key == constants.KEY_1:
                self.titrator.updateState(CalibratePh(self.titrator))
            else:
                self.titrator.updateState(InitialTitration(self.titrator))

    def loop(self):
        if self.subState == 1:
            lcd_interface.lcd_out("Enter Sol.", line=1)
            lcd_interface.lcd_out("weight (g)", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 2:
            lcd_interface.lcd_out("Enter Sol.", line=1)
            lcd_interface.lcd_out("salinity (ppt)", line=2)
            lcd_interface.lcd_out("Press any to cont", line=3)
            lcd_interface.lcd_out("", line=4)

        elif self.subState == 3:
            lcd_interface.lcd_out("Calibrate pH probe?", line=1)
            lcd_interface.lcd_out("Yes: 1", line=2)
            lcd_interface.lcd_out("No (use old): 0", line=3)
            lcd_interface.lcd_out(
                "{0:>2.3f} pH: {1:>2.4f} V".format(
                    constants.PH_REF_PH, constants.PH_REF_VOLTAGE
                ),
                line=4,
            )

    def start(self):
        pass
