from titration.utils.ui_state import main_menu
from titration.utils import interfaces, constants
import types
from titration.utils.devices.keypad_mock import Keypad

# TODO: look at ModuleType
# TODO: log instead of print
if constants.IS_TEST:
    from titration.utils.devices import board_mock

board_class: types.ModuleType = board_mock

if constants.IS_TEST:
    board_class = board_mock
else:
    import board

    board_class = board


class Titrator:
    def __init__(self):
        self.state = main_menu.MainMenu(self)
        interfaces.setup_interfaces()  # TODO: look at removing, update to not call LCD and keypad
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
        self._handleUI()  # look at keypad, update LCD

    def updateState(self, newState):
        print(
            "Titrator::updateState() from ",
            self.state.name(),
            " to ",
            newState.name(),
        )
        self.state.start()

    def _handleUI(self):
        print("Titrator::handleUI() - ", self.state.name())
        key = self.keypad.get_key()
        print("Titrator::handleUI() - ", self.state.name(), "::handleKey(", key, ")")
        self.state.handleKey(key)
        print(
            "Titrator::handleUI() - ",
            self.state.name(),
            "::substate",
            self.state.subState,
            "::loop()",
        )
        self.state.loop()
