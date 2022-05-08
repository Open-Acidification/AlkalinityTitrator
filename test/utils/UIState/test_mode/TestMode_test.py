from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils import LCD_interface
from titration.utils.UIState.test_mode.TestMode import TestMode

# Test handleKey
@mock.patch.object(TestMode, "_setNextState")
def test_handleKey(setNextStateMock):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "ReadValues")
    setNextStateMock.reset_mock()

    testMode.handleKey("2")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "Pump")
    setNextStateMock.reset_mock()

    testMode.handleKey("3")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "SetVolume")
    setNextStateMock.reset_mock()

    testMode.handleKey('*')
    assert(testMode.subState == 2)

    testMode.handleKey("4")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "ToggleTestMode")
    setNextStateMock.reset_mock()

    testMode.handleKey("5")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "ReadVolume")
    setNextStateMock.reset_mock()

    testMode.handleKey("6")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "MainMenu")
    setNextStateMock.reset_mock()

    testMode.handleKey('*')
    assert(testMode.subState == 1)

# Test loop
@mock.patch.object(LCD_interface, "display_list")
def test_loop(displayListMock):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.loop()
    assert displayListMock.called_with(testMode.TEST_OPTIONS_1)
    displayListMock.reset_called()

    testMode.subState += 1
    testMode.loop()
    assert displayListMock.called_with(testMode.TEST_OPTIONS_2)

# Test TestMode
@mock.patch.object(TestMode, "_setNextState")
@mock.patch.object(LCD_interface, "display_list")
def test_TestMode(displayListMock, setNextStateMock):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.loop()
    assert displayListMock.called_with(testMode.TEST_OPTIONS_1)

    testMode.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "ReadValues")
    setNextStateMock.reset_called()

    testMode.loop()
    assert displayListMock.called_with(testMode.TEST_OPTIONS_1)
    displayListMock.reset_called()

    testMode.handleKey("2")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "Pump")
    setNextStateMock.reset_called()
    
    testMode.loop()
    assert displayListMock.called_with(testMode.TEST_OPTIONS_1)
    displayListMock.reset_called()

    testMode.handleKey("3")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "SetVolume")
    setNextStateMock.reset_called()

    testMode.loop()
    assert displayListMock.called_with(testMode.TEST_OPTIONS_1)
    displayListMock.reset_called()

    testMode.handleKey('*')
    assert(testMode.subState == 2)

    testMode.loop()
    assert displayListMock.called_with(testMode.TEST_OPTIONS_2)
    displayListMock.reset_called()

    testMode.handleKey("4")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "ToggleTestMode")
    setNextStateMock.reset_called()

    testMode.loop()
    assert displayListMock.called_with(testMode.TEST_OPTIONS_2)

    testMode.handleKey("5")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "ReadVolume")
    setNextStateMock.reset_called()
    
    testMode.loop()
    assert displayListMock.called_with(testMode.TEST_OPTIONS_2)

    testMode.handleKey("6")
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "MainMenu")
