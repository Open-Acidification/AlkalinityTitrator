from unittest import mock
from titration.utils.UIState.titration.SetupTitration import SetupTitration
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces

# Test handleKey
@mock.patch.object(SetupTitration, "_setNextState")
def test_handleKey(mock):
    setupTitration = SetupTitration(Titrator())

    setupTitration.handleKey(1)
    assert mock.called

    setupTitration = SetupTitration(Titrator())

    setupTitration.handleKey(0)
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "read_user_value",  return_value=5.5)
@mock.patch.object(interfaces, "lcd_out")
def test_loop(mock1, mock2):
    setupTitration = SetupTitration(Titrator())

    setupTitration.loop()
    assert(setupTitration.values[0] == 5.5)
    assert(setupTitration.values[1] == 5.5)
    assert mock1.called_with("{0:>2.3f} pH: {1:>2.4f} V".format(constants.PH_REF_PH, constants.PH_REF_VOLTAGE), line=4)

@mock.patch.object(SetupTitration, "_setNextState")
@mock.patch.object(interfaces, "read_user_value",  return_value=5.5)
@mock.patch.object(interfaces, "lcd_out")
def test_SetupTitration(mock1, mock2, mock3):
    setupTitration = SetupTitration(Titrator())

    setupTitration.loop()
    assert(setupTitration.values[0] == 5.5)
    assert(setupTitration.values[1] == 5.5)
    assert mock1.called_with("{0:>2.3f} pH: {1:>2.4f} V".format(constants.PH_REF_PH, constants.PH_REF_VOLTAGE), line=4)

    setupTitration.handleKey(1)

    assert mock3.called
