from unittest import mock
from titration.utils.UIState.titration.AutomaticTitration import AutomaticTitration
from titration.utils.UIState.titration.InitialTitration import InitialTitration
from titration.utils.titrator import Titrator
from titration.utils import constants, interfaces, LCD
from titration.utils.UIState.titration.ManualTitration import ManualTitration

# Test handleKey
@mock.patch.object(InitialTitration, "_setNextState")
def test_handleKey(mock):
    initialTitration = InitialTitration(Titrator())

    key_input = 'a'
    initialTitration.handleKey(key_input)
    assert(initialTitration.value == 'a')
    assert(initialTitration.subState == 2)

# Test loop
@mock.patch.object(InitialTitration, "_setNextState")
@mock.patch.object(LCD, "lcd_out")
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
    assert mock2.called_with(AutomaticTitration(initialTitration.titrator), False)
    mock2.reset_called()

    initialTitration = InitialTitration(Titrator())

    initialTitration.subState += 1
    initialTitration.value = 1
    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3)]
    )
    mock1.reset_called()
    assert mock2.called_with(ManualTitration(initialTitration.titrator), False)
    mock2.reset_called()

@mock.patch.object(InitialTitration, "_setNextState")
@mock.patch.object(LCD, "lcd_out")
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

    initialTitration.handleKey(1)
    assert(initialTitration.value == 1)
    assert(initialTitration.subState == 2)

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3)]
    )
    mock1.reset_called()
    assert mock2.called_with(ManualTitration(initialTitration.titrator), False)
    mock2.reset_called()

    initialTitration = InitialTitration(Titrator())

    initialTitration.handleKey(2)
    assert(initialTitration.value == 2)
    assert(initialTitration.subState == 2)

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Heating to 30 C...", line=1),
        mock.call("Please wait...", style=constants.LCD_CENT_JUST, line=3)]
    )
    mock1.reset_called()
    assert mock2.called_with(AutomaticTitration(initialTitration.titrator), False)
    mock2.reset_called()
