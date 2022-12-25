from titration.utils.ui_state import ui_state
from titration.utils import lcd_interface, interfaces


# TODO: read from actual devices
class ReadValues(ui_state.UIState):
    def __init__(self, titrator, state):
        ui_state.__init__("ReadValues", titrator)
        self.titrator = titrator
        self.values = {
            "temp": 1,
            "res": 1,
            "pH_reading": 1,
            "pH_volts": 1,
            "numVals": 20,
            "timeStep": 0.5,
        }
        self.subState = 1
        self.previousState = state

    def name(self):
        return "ReadValues"

    def handleKey(self, key):
        self._setNextState(self.previousState, True)

    def loop(self):
        for i in range(self.values["numVals"]):
            lcd_interface.lcd_out(
                "Temp: {0:>4.3f} C".format(self.values["temp"]), line=1
            )
            lcd_interface.lcd_out(
                "Res:  {0:>4.3f} Ohms".format(self.values["res"]), line=2
            )
            lcd_interface.lcd_out(
                "pH:   {0:>4.5f} pH".format(self.values["pH_reading"]), line=3
            )
            lcd_interface.lcd_out(
                "pH V: {0:>3.4f} mV".format(self.values["pH_volts"] * 1000), line=4
            )
            lcd_interface.lcd_out("Reading: {}".format(i), 1, console=True)
            interfaces.delay(self.values["timeStep"])
        lcd_interface.lcd_out("Press any to cont", line=1)
        lcd_interface.lcd_out("", line=2)
        lcd_interface.lcd_out("", line=3)
        lcd_interface.lcd_out("", line=4)
