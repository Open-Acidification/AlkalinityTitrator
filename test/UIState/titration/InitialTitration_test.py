from unittest import mock
from titration.utils.UIState.titration.AutomaticTitration import AutomaticTitration
from titration.utils.UIState.titration.InitialTitration import InitialTitration
from titration.utils.Titrator import Titrator
from titration.utils import interfaces
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
@mock.patch.object(interfaces, "lcd_out")
def test_loop(mock1, mock2):
    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    assert mock1.called_with("Stir speed: slow", line=4)

    initialTitration.subState += 1
    initialTitration.loop()
    assert mock2.called_with(AutomaticTitration(initialTitration.titrator), False)
    mock2.reset_called()

    initialTitration = InitialTitration(Titrator())

    initialTitration.subState += 1
    initialTitration.value = 1
    initialTitration.loop()
    assert mock2.called_with(ManualTitration(initialTitration.titrator), False)
    mock2.reset_called()

@mock.patch.object(InitialTitration, "_setNextState")
@mock.patch.object(interfaces, "lcd_out")
def test_InitialTitration(mock1, mock2):
    initialTitration = InitialTitration(Titrator())

    initialTitration.loop()
    assert mock1.called_with("Stir speed: slow", line=4)

    initialTitration.handleKey(1)
    assert(initialTitration.value == 1)
    assert(initialTitration.subState == 2)

    initialTitration.loop()
    assert mock2.called_with(ManualTitration(initialTitration.titrator), False)
    mock2.reset_called()

    initialTitration = InitialTitration(Titrator())

    initialTitration.handleKey(2)
    assert(initialTitration.value == 2)
    assert(initialTitration.subState == 2)

    initialTitration.loop()
    assert mock2.called_with(AutomaticTitration(initialTitration.titrator), False)
    mock2.reset_called()
