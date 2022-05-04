from unittest import mock
from unittest.mock import ANY 
from titration.utils.UIState.titration.InitialTitration import InitialTitration
from titration.utils.titrator import Titrator
from titration.utils import LCD_interface, constants

# Test handleKey
@mock.patch.object(InitialTitration, "_setNextState")
def test_handleKey(mock):
    initialTitration = InitialTitration(Titrator())

    initialTitration.handleKey("1")
    assert(initialTitration.value == "1")
    assert(initialTitration.subState == 2)

# Test loop
@mock.patch.object(InitialTitration, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(mock1, mock2):
    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Bring pH to 3.5:", line=1),
        mock.call("Manual: 1", line=2),
        mock.call("Automatic: 2", line=3),
        mock.call("Stir speed: slow", line=4)]
    )
    mock1.reset_called()

    initialTitration.subState += 1
    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3)]
    )
    mock1.reset_called()
    mock2.assert_called_with(ANY, False)
    assert(mock2.call_args.args[0].name() == "AutomaticTitration")
    mock2.reset_mock()

    initialTitration = InitialTitration(Titrator())

    initialTitration.subState += 1
    initialTitration.value = "1"
    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3)]
    )
    mock1.reset_called()
    mock2.assert_called_with(ANY, False)
    assert(mock2.call_args.args[0].name() == "ManualTitration")

@mock.patch.object(InitialTitration, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_InitialTitration(mock1, mock2):
    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Bring pH to 3.5:", line=1),
        mock.call("Manual: 1", line=2),
        mock.call("Automatic: 2", line=3),
        mock.call("Stir speed: slow", line=4)]
    )
    mock1.reset_called()

    initialTitration.handleKey("1")
    assert(initialTitration.value == "1")
    assert(initialTitration.subState == 2)

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3)]
    )
    mock1.reset_called()
    mock2.assert_called_with(ANY, False)
    assert(mock2.call_args.args[0].name() == "ManualTitration")
    mock2.reset_mock()

    initialTitration = InitialTitration(Titrator())

    initialTitration.handleKey("2")
    assert(initialTitration.value == "2")
    assert(initialTitration.subState == 2)

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3)]
    )
    mock1.reset_called()
    mock2.assert_called_with(ANY, False)
    assert(mock2.call_args.args[0].name() == "AutomaticTitration")
