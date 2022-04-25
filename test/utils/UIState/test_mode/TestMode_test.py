from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils import constants, LCD
from titration.utils.UIState.test_mode.TestMode import TestMode

# Test handleKey
@mock.patch.object(TestMode, "_setNextState")
def test_handleKey(mock):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.handleKey("1")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "ReadValues")
    mock.reset_mock()

    testMode.handleKey("2")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "Pump")
    mock.reset_mock()

    testMode.handleKey("3")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "SetVolume")
    mock.reset_mock()

    testMode.handleKey('*')
    assert(testMode.subState == 2)

    testMode.handleKey("4")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "ToggleTestMode")
    mock.reset_mock()

    testMode.handleKey("5")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "ReadVolume")
    mock.reset_mock()

    testMode.handleKey("6")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "MainMenu")
    mock.reset_mock()

    testMode.handleKey('*')
    assert(testMode.subState == 1)

# Test loop
@mock.patch.object(LCD, "display_list")
def test_loop(mock):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_1)

    testMode.subState += 1

    testMode.loop()
    assert mock.called_with(constants.TEST_OPTIONS_2)

# Test TestMode
@mock.patch.object(TestMode, "_setNextState")
@mock.patch.object(LCD, "display_list")
def test_TestMode(mock1, mock2):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.loop()
    assert mock1.called_with(constants.TEST_OPTIONS_1)

    testMode.handleKey("1")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "ReadValues")
    mock2.reset_mock()

    testMode.loop()
    assert mock1.called_with(constants.TEST_OPTIONS_1)

    testMode.handleKey("2")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "Pump")
    mock2.reset_mock()
    
    testMode.loop()
    assert mock1.called_with(constants.TEST_OPTIONS_1)

    testMode.handleKey("3")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "SetVolume")
    mock2.reset_mock()

    testMode.loop()
    assert mock1.called_with(constants.TEST_OPTIONS_1)

    testMode.handleKey('*')
    assert(testMode.subState == 2)

    testMode.loop()
    assert mock1.called_with(constants.TEST_OPTIONS_2)

    testMode.handleKey("4")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "ToggleTestMode")
    mock2.reset_mock()

    testMode.loop()
    assert mock1.called_with(constants.TEST_OPTIONS_2)

    testMode.handleKey("5")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "ReadVolume")
    mock2.reset_mock()
    
    testMode.loop()
    assert mock1.called_with(constants.TEST_OPTIONS_2)

    testMode.handleKey("6")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "MainMenu")
    mock2.reset_mock()
