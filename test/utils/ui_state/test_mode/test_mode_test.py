from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface
from titration.utils.ui_state.test_mode.test_mode import TestMode


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "ReadValues"
    updateStateMock.reset_mock()

    testMode.handleKey("2")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "Pump"
    updateStateMock.reset_mock()

    testMode.handleKey("3")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "SetVolume"
    updateStateMock.reset_mock()

    testMode.handleKey("*")
    assert testMode.subState == 2

    testMode.handleKey("4")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "ToggleTestMode"
    updateStateMock.reset_mock()

    testMode.handleKey("5")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "ReadVolume"
    updateStateMock.reset_mock()

    testMode.handleKey("6")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"
    updateStateMock.reset_mock()

    testMode.handleKey("*")
    assert testMode.subState == 1


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )
    lcdOutMock.reset_called()

    testMode.subState += 1
    testMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("4: Toggle Test Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Test Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )


# Test TestMode
@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_TestMode(lcdOutMock, updateStateMock):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )
    lcdOutMock.reset_called()

    testMode.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "ReadValues"
    updateStateMock.reset_called()

    testMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )
    lcdOutMock.reset_called()

    testMode.handleKey("2")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "Pump"
    updateStateMock.reset_called()

    testMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )
    lcdOutMock.reset_called()

    testMode.handleKey("3")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "SetVolume"
    updateStateMock.reset_called()

    testMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("1: Read Values", line=1),
            mock.call("2: Pump", line=2),
            mock.call("3: Set Volume", line=3),
            mock.call("*: Page 2", line=4),
        ]
    )
    lcdOutMock.reset_called()

    testMode.handleKey("*")
    assert testMode.subState == 2

    testMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("4: Toggle Test Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Test Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )
    lcdOutMock.reset_called()

    testMode.handleKey("4")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "ToggleTestMode"
    updateStateMock.reset_called()

    testMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("4: Toggle Test Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Test Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )
    lcdOutMock.reset_called()

    testMode.handleKey("5")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "ReadVolume"
    updateStateMock.reset_called()

    testMode.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("4: Toggle Test Mode", line=1),
            mock.call("5: Read Volume", line=2),
            mock.call("6: Exit Test Mode", line=3),
            mock.call("*: Page 1", line=4),
        ]
    )
    lcdOutMock.reset_called()

    testMode.handleKey("6")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"
