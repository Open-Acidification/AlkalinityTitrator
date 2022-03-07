import pytest
from unittest import mock
from titration.utils.UIState.titration.SetupTitration import SetupTitration
from titration.utils.Titrator import Titrator
from titration.utils import interfaces

# Test handleKey
@mock.patch.object(SetupTitration, "_setNextState")
def test_handleKey(mock):
    setupTitration = SetupTitration(Titrator())

    key_input = 1
    setupTitration.handleKey(key_input)
    assert not mock.called
    assert(setupTitration.subState == 2)
    mock.reset_mock()

    setupTitration.handleKey(key_input)
    assert not mock.called
    assert(setupTitration.subState == 3)
    mock.reset_mock()

    setupTitration.handleKey(key_input)
    assert mock.called
    assert(setupTitration.subState == 4)
    mock.reset_mock()

    setupTitration = SetupTitration(Titrator())

    key_input = 2
    setupTitration.handleKey(key_input)
    assert not mock.called
    assert(setupTitration.subState == 2)
    mock.reset_mock()

    setupTitration.handleKey(key_input)
    assert not mock.called
    assert(setupTitration.subState == 3)
    mock.reset_mock()

    setupTitration.handleKey(key_input)
    assert mock.called
    assert(setupTitration.subState == 4)

# Test loop
@mock.patch.object(interfaces, "read_user_value",  return_value=5.5)
@mock.patch.object(interfaces, "lcd_out")
def test_loop(mock1, mock2):
    setupTitration = SetupTitration(Titrator())

    setupTitration.loop()
    assert(setupTitration.values[1] == 5.5)

    setupTitration.subState = 2
    setupTitration.loop()
    assert(setupTitration.values[2] == 5.5)

    setupTitration.subState = 3
    setupTitration.loop()
    mock2.assert_called_with('"{0:>2.3f} pH: {1:>2.4f} V".format(constants.PH_REF_PH, constants.PH_REF_VOLTAGE), line=4')
