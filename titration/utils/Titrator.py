from titration.utils.UIState import UIState, MainMenu
from titration.utils import interfaces, constants

class Titrator:
    def __init__(self):
        self.state = MainMenu.MainMenu(self)
        self.nextState = None
        interfaces.setup_interfaces()

    def loop(self):
        # wdt_reset()
        # blink                                     # blink the on-board LED to show that we are running
        self._handleUI()                            # look at keypad, update LCD
        # updateControls                            # turn CO2 and temperature controls on or off
        # writeDataToSD                             # record current state to data log
        # writeDataToSerial                         # record current pH and temperature to serial
        # PushingBox::instance()->loop()            # write data to Google Sheets
        # Ethernet_TC::instance()->loop();          # renew DHCP lease
        # EthernetServer_TC::instance()->loop();    # handle any HTTP requests

    def setNextState(self, newState, update):
        print("Titrator::setNextState() from ", self.nextState.name() if self.nextState else 'nullptr', " to ", newState.name())
        assert(self.nextState == None)
        self.nextState = newState
        if (update):
            self._updateState()

    def setup():
        pass

    def _updateState(self):
        if (self.nextState):
            print("Titrator::updateState() to ", self.nextState.name())
            assert(self.state != self.nextState)
            self.state = self.nextState
            self.nextState = None
            self.state.start()

    def _handleUI(self):
        print("Titrator::handleUI() - ", self.state.name())
        key = interfaces.read_user_input()
        if (key == constants.NO_KEY):
            # if (!lastKeypadTime) {
                # // we have already reached an idle state, so don't do other checks
            # else if (isInCalibration()) {
                # // we are in calibration, so don't return to main menu
            # } else if (nextState) {
            if (self.nextState):
                pass
                # we already have a next state teed-up, do don't try to return to main menu
            # else if (millis() - lastKeypadTime > IDLE_TIMEOUT) {
                # // time since last keypress exceeds the idle timeout, so return to main menu
                # self.setNextState(MainMenu(self))
                # lastKeypadTime = 0;  // so we don't do this until another keypress!
        else:
            print("Titrator::handleUI() - ", self.state.name(), "::handleKey(", key, ")")
            self.state.handleKey(key)
            # lastKeypadTime = millis()
        self._updateState()
        print("Titrator::handleUI() - ", self.state.name(), "::loop()")
        self.state.loop()