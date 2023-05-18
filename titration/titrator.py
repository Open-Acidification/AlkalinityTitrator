"""
The file for the Titrator class
"""

# pylint: disable = too-many-instance-attributes

from titration import constants
from titration.devices.library import (
    Keypad,
    LiquidCrystal,
    PHProbe,
    StirControl,
    SyringePump,
    TemperatureControl,
    TemperatureProbe,
)
from titration.ui_state.main_menu import MainMenu


class Titrator:
    """
    The Titrator class is the model for the state machine in order
    to move through the different titration states

    Attributes:
        state (UIState object): is used to represent the current state in the state machine
        next_state (UIState object): is used to move to the next state in the state machine
        keypad (Keypad object): is used to identify what keypad value was entered
    """

    def __init__(self):
        """
        The constructor for the Titrator class
        """
        # Initialize LCD
        self.lcd = LiquidCrystal(cols=constants.LCD_WIDTH, rows=constants.LCD_HEIGHT)

        # Initialize Keypad
        self.keypad = Keypad()

        # Initialize pH Probe
        self.ph_probe = PHProbe()

        # Initialize Syringe Pump
        self.pump = SyringePump()

        # Initialize Stir Controller
        self.stir_controller = StirControl()

        # Initialize Temperature Probes
        self.temp_probe_one = TemperatureProbe(1)
        self.temp_probe_two = TemperatureProbe(2)

        # Initialize Temperature Controller
        self.temp_controller = TemperatureControl(self.temp_probe_two)

        # Initialize State
        self.state = MainMenu(self)
        self.next_state = None

        # Initialize Titrator Values
        self.pump_volume = "0"
        self.solution_weight = "0"
        self.solution_salinity = "0"
        self.volume = "0"
        self.degas_time = 0

        # pH Calibration Values
        self.buffer_measured_volts = 0
        self.buffer_nominal_ph = 0

        # Temperature Calibration Values
        self.reference_temperature = 0

    def loop(self):
        """
        The function used to loop through in each state
        """
        self.temp_controller.update()
        self.update_state()
        print(
            "Titrator::handleUI() - ",
            self.state.name(),
            "::substate",
            self.state.substate,
            "::loop()",
        )
        self.handle_ui()

    def set_next_state(self, new_state, update):
        """
        The function used to set the next state the state machine will enter
        """
        print(
            "Titrator::setNextState() from ",
            self.next_state.name() if self.next_state else "nullptr",
            " to ",
            new_state.name(),
        )
        self.next_state = new_state
        if update:
            self.update_state()

    def update_state(self):
        """
        The function used to move to the next state
        """
        if self.next_state:
            print("Titrator::updateState() to ", self.next_state.name())
            self.state = self.next_state
            self.next_state = None
            self.state.start()

    def handle_ui(self):
        """
        The function used to receive the keypad input and process the appropriate response
        """
        print("Titrator::handleUI() - ", self.state.name())
        key = self.keypad.get_key()
        print("Titrator::handleUI() - ", self.state.name(), "::handleKey(", key, ")")
        if key is not None:
            self.state.handle_key(key)
        self.state.loop()
