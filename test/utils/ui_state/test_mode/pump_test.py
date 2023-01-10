from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.test_mode.test_mode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface
from titration.utils.ui_state.test_mode.pump import Pump


# Test handleKey
@mock.patch.object(Pump, "_setNextState")
def test_handleKey(setNextStateMock):
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    assert pump.subState == 2
    setNextStateMock.reset_called()

    pump.handleKey("0")
    assert pump.values["p_direction"] == "0"
    assert pump.subState == 3

    pump.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    pump.subState += 1
    pump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("In/Out (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    pump.subState += 1
    pump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Pumping volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


# Test Pump
@mock.patch.object(Pump, "_setNextState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_Pump(lcdOutMock, setNextStateMock):
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    pump.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    assert pump.subState == 2
    setNextStateMock.reset_called()

    pump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("In/Out (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    pump.handleKey("0")
    assert pump.values["p_direction"] == "0"
    assert pump.subState == 3

    pump.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Pumping volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    pump.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"
