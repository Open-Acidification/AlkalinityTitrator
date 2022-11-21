from unittest import mock
from unittest.mock import ANY 
from titration.utils.UIState.titration.InitialTitration import InitialTitration
from titration.utils.Titrator import Titrator
from titration.utils import LCD_interface, constants

# Test handleKey
def test_handleKey():
    initialTitration = InitialTitration(Titrator())

    initialTitration.handleKey("1")
    assert(initialTitration.choice == "1")
    assert(initialTitration.subState == 2)

# Test loop
@mock.patch.object(InitialTitration, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(lcdOutMock, setNextStateMock):
    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Bring pH to 3.5:", line=1),
        mock.call("Manual: 1", line=2),
        mock.call("Automatic: 2", line=3),
        mock.call("Stir speed: slow", line=4)]
    )
    lcdOutMock.reset_called()

    initialTitration.subState += 1
    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("", line=2),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
        mock.call("", line=4)]
    )
    lcdOutMock.reset_called()
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "AutomaticTitration")
    setNextStateMock.reset_mock()

    initialTitration = InitialTitration(Titrator())

    initialTitration.subState += 1
    initialTitration.choice = "1"
    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("", line=2),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
        mock.call("", line=4)]    
    )
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "ManualTitration")

@mock.patch.object(InitialTitration, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_InitialTitration(lcdOutMock, setNextStateMock):
    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Bring pH to 3.5:", line=1),
        mock.call("Manual: 1", line=2),
        mock.call("Automatic: 2", line=3),
        mock.call("Stir speed: slow", line=4)]
    )
    lcdOutMock.reset_called()

    initialTitration.handleKey("1")
    assert(initialTitration.choice == "1")
    assert(initialTitration.subState == 2)

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("", line=2),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
        mock.call("", line=4)]
    )
    lcdOutMock.reset_called()
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "ManualTitration")
    setNextStateMock.reset_called()

    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Bring pH to 3.5:", line=1),
        mock.call("Manual: 1", line=2),
        mock.call("Automatic: 2", line=3),
        mock.call("Stir speed: slow", line=4)]
    )
    lcdOutMock.reset_called()

    initialTitration.handleKey("2")
    assert(initialTitration.choice == "2")
    assert(initialTitration.subState == 2)

    initialTitration.loop()
    lcdOutMock.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("", line=2),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3),
        mock.call("", line=4)]    
    )
    setNextStateMock.assert_called_with(ANY, True)
    assert(setNextStateMock.call_args.args[0].name() == "AutomaticTitration")
