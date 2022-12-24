from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.UIState.test_mode.TestMode import TestMode
from titration.utils.Titrator import Titrator
from titration.utils import LCD_interface
from titration.utils.UIState.prime_pump.PrimePump import PrimePump

# Test handleKey
@mock.patch.object(PrimePump, "_setNextState")
def test_handleKey(setNextStateMock):
    primePump = PrimePump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    primePump.handleKey("3")
    assert primePump.values["selection"] == "3"
    assert primePump.subState == 2

    primePump.handleKey("1")
    assert primePump.values["selection"] == "1"

    primePump.handleKey("0")
    assert primePump.values["selection"] == "0"
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"


# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(lcdOutMock):
    primePump = PrimePump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    primePump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("How many pumps?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    primePump.subState += 1
    primePump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("How many more?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )


# Test PrimePump
@mock.patch.object(PrimePump, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_PrimePump(lcdOutMock, setNextStateMock):
    primePump = PrimePump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    primePump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("How many pumps?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    primePump.handleKey("3")
    assert primePump.values["selection"] == "3"
    assert primePump.subState == 2

    primePump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("How many more?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    primePump.handleKey("1")
    assert primePump.values["selection"] == "1"

    lcdOutMock.assert_has_calls(
        [
            mock.call("How many more?", line=1),
            mock.call("Choose a number", line=2),
            mock.call("Choose 0 to return", line=3),
            mock.call("", line=4),
        ]
    )

    primePump.handleKey("0")
    assert primePump.values["selection"] == "0"
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"
