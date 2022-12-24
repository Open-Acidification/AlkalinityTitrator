from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.Titrator import Titrator
from titration.utils import LCD_interface
from titration.utils.UIState.test_mode.TestMode import TestMode

# Test handleKey
@mock.patch.object(TestMode, "_setNextState")
def test_handleKey(setNextStateMock):
    testMode = TestMode(Titrator(), MainMenu(Titrator()))

    testMode.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "ReadValues"
    setNextStateMock.reset_mock()

    testMode.handleKey("2")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "Pump"
    setNextStateMock.reset_mock()

    testMode.handleKey("3")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "SetVolume"
    setNextStateMock.reset_mock()

    testMode.handleKey("*")
    assert testMode.subState == 2

    testMode.handleKey("4")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "ToggleTestMode"
    setNextStateMock.reset_mock()

    testMode.handleKey("5")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "ReadVolume"
    setNextStateMock.reset_mock()

    testMode.handleKey("6")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "MainMenu"
    setNextStateMock.reset_mock()

    testMode.handleKey("*")
    assert testMode.subState == 1


# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
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
@mock.patch.object(TestMode, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_TestMode(lcdOutMock, setNextStateMock):
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
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "ReadValues"
    setNextStateMock.reset_called()

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
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "Pump"
    setNextStateMock.reset_called()

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
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "SetVolume"
    setNextStateMock.reset_called()

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
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "ToggleTestMode"
    setNextStateMock.reset_called()

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
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "ReadVolume"
    setNextStateMock.reset_called()

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
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "MainMenu"
