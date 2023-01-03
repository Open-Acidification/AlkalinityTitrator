from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.titration.initial_titration import InitialTitration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, constants


# Test handleKey
def test_handleKey():
    initialTitration = InitialTitration(Titrator())

    initialTitration.handleKey("1")
    assert initialTitration.choice == "1"
    assert initialTitration.subState == 2


# Test loop
@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock, updateStateMock):
    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Bring pH to 3.5:", line=1),
            mock.call("Manual: 1", line=2),
            mock.call("Automatic: 2", line=3),
            mock.call("Stir speed: slow", line=4),
        ]
    )
    lcdOutMock.reset_called()

    initialTitration.subState += 1
    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Heating to 30 C...", line=1),
            mock.call("", line=2),
            mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "AutomaticTitration"
    updateStateMock.reset_mock()

    initialTitration = InitialTitration(Titrator())

    initialTitration.subState += 1
    initialTitration.choice = "1"
    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Heating to 30 C...", line=1),
            mock.call("", line=2),
            mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
            mock.call("", line=4),
        ]
    )
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "ManualTitration"


@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_InitialTitration(lcdOutMock, updateStateMock):
    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Bring pH to 3.5:", line=1),
            mock.call("Manual: 1", line=2),
            mock.call("Automatic: 2", line=3),
            mock.call("Stir speed: slow", line=4),
        ]
    )
    lcdOutMock.reset_called()

    initialTitration.handleKey("1")
    assert initialTitration.choice == "1"
    assert initialTitration.subState == 2

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Heating to 30 C...", line=1),
            mock.call("", line=2),
            mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "ManualTitration"
    updateStateMock.reset_called()

    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Bring pH to 3.5:", line=1),
            mock.call("Manual: 1", line=2),
            mock.call("Automatic: 2", line=3),
            mock.call("Stir speed: slow", line=4),
        ]
    )
    lcdOutMock.reset_called()

    initialTitration.handleKey("2")
    assert initialTitration.choice == "2"
    assert initialTitration.subState == 2

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Heating to 30 C...", line=1),
            mock.call("", line=2),
            mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
            mock.call("", line=4),
        ]
    )
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "AutomaticTitration"
