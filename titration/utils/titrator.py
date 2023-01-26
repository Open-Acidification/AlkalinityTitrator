"""
The file for the Titrator class
"""
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils import interfaces, constants


if constants.IS_TEST:
    from titration.utils.devices import board_mock as board_class
    from titration.utils.devices.keypad_mock import Keypad
else:
    import board as board_class  # type: ignore
    from titration.utils.devices.keypad import Keypad  # type: ignore


class Titrator:
    """
    The Titrator class is the model for the state machine in order to move through the different titration states

    Attributes:
        state (UIState object): is used to represent the current state in the state machine
        next_state (UIState object): is used to move to the next state in the state machine
        keypad (Keypad object): is used to identify what keypad value was entered
    """

    def __init__(self):
        """
        The constructor for the Titrator class
        """
        self.state = MainMenu(self)
        self.next_state = None
        interfaces.setup_interfaces()  # TODO: look at removing, update to not call LCD and keypad

        # Initialize Keypad
        self.key = "A"
        self.keypad = Keypad(
            r0=board_class.D1,
            r1=board_class.D6,
            r2=board_class.D5,
            r3=board_class.D19,
            c0=board_class.D16,
            c1=board_class.D26,
            c2=board_class.D20,
            c3=board_class.D21,
        )

    def loop(self):
        """
        The function used to loop through in each state
        """
        self._handle_ui()

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
            self._update_state()

    def _update_state(self):
        """
        The function used to move to the next state
        """
        if self.next_state:
            print("Titrator::updateState() to ", self.next_state.name())
            self.state = self.next_state
            self.next_state = None
            self.state.start()

    def _handle_ui(self):
        """
        The function used to receive the keypad input and process the appropriate response
        """
        print("Titrator::handleUI() - ", self.state.name())
        if self.key != self.keypad.keypad_poll():
            self.key = self.keypad.keypad_poll()  # pylint: disable = E1128
            print(
                "Titrator::handleUI() - ",
                self.state.name(),
                "::handle_key(",
                self.key,
                ")",
            )
            self.state.handle_key(self.key)
        self._update_state()
        print(
            "Titrator::handleUI() - ",
            self.state.name(),
            "::substate",
            self.state.substate,
            "::loop()",
        )
        self.state.loop()
