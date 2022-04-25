from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.titration.SetupTitration import SetupTitration
from titration.utils.titrator import Titrator
from titration.utils import constants, LCD

# Test handleKey
@mock.patch.object(SetupTitration, "_setNextState")
def test_handleKey(mock):
    setupTitration = SetupTitration(Titrator())

    setupTitration.handleKey("1")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "CalibratePh")
    mock.reset_mock()

    setupTitration = SetupTitration(Titrator())

    setupTitration.handleKey("0")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "InitialTitration")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD, "read_user_value",  return_value=5.5)
@mock.patch.object(LCD, "lcd_out")
def test_loop(mock1, mock2):
    setupTitration = SetupTitration(Titrator())

    setupTitration.loop()
    assert(setupTitration.values[0] == 5.5)
    assert(setupTitration.values[1] == 5.5)
    mock1.assert_has_calls(
        [mock.call("Calibrate pH probe?", line=1), 
        mock.call("Yes: 1", line=2),
        mock.call("No (use old): 0", line=3),
        mock.call("{0:>2.3f} pH: {1:>2.4f} V".format(constants.PH_REF_PH, constants.PH_REF_VOLTAGE), line=4)
    ])    

@mock.patch.object(SetupTitration, "_setNextState")
@mock.patch.object(LCD, "read_user_value",  return_value=5.5)
@mock.patch.object(LCD, "lcd_out")
def test_SetupTitration(mock1, mock2, mock3):
    setupTitration = SetupTitration(Titrator())

    setupTitration.loop()
    assert(setupTitration.values[0] == 5.5)
    assert(setupTitration.values[1] == 5.5)
    mock1.assert_has_calls(
        [mock.call("Calibrate pH probe?", line=1), 
        mock.call("Yes: 1", line=2),
        mock.call("No (use old): 0", line=3),
        mock.call("{0:>2.3f} pH: {1:>2.4f} V".format(constants.PH_REF_PH, constants.PH_REF_VOLTAGE), line=4)
    ])    

    setupTitration.handleKey("1")
    mock3.assert_called_with(ANY, True)
    assert(mock3.call_args.args[0].name() == "CalibratePh")
    mock3.reset_mock()
