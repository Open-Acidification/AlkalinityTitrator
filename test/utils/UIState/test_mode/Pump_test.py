from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.UIState.test_mode.TestMode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import LCD_interface
from titration.utils.UIState.test_mode.Pump import Pump

# Test handleKey
@mock.patch.object(Pump, "_setNextState")
def test_handleKey(mock):
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.handleKey("0")
    assert(pump.values['p_direction'] == "0")
    assert(pump.subState == 2)

    pump.handleKey("0")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "TestMode")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD_interface, 'lcd_out')
@mock.patch.object(LCD_interface, 'read_user_value', return_value=5.5)
def test_loop(mock1, mock2):
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.loop()
    assert(pump.values['p_volume'] == 5.5)
    assert mock1.called_with("Volume: ")
    mock1.reset_called()
    mock2.assert_has_calls(
        [mock.call("In/Out (0/1):", line=1)]
    )
    mock2.reset_called()
    
    pump.subState += 1
    pump.loop()
    mock2.assert_has_calls(
        [mock.call("Pumping volume", line=1),
        mock.call("Press any to cont.", line=3)]
    )

# Test Pump
@mock.patch.object(Pump, "_setNextState")
@mock.patch.object(LCD_interface, 'lcd_out')
@mock.patch.object(LCD_interface, 'read_user_value', return_value=5.5)
def test_Pump(mock1, mock2, mock3):
    pump = Pump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    pump.loop()
    assert(pump.values['p_volume'] == 5.5)
    assert mock1.called_with("Volume: ")
    mock1.reset_called()
    mock2.assert_has_calls(
        [mock.call("In/Out (0/1):", line=1)]
    )
    mock2.reset_called()

    pump.handleKey("0")
    assert(pump.values['p_direction'] == "0")
    assert(pump.subState == 2)

    pump.loop()
    mock2.assert_has_calls(
        [mock.call("Pumping volume", line=1),
        mock.call("Press any to cont.", line=3)]
    )

    pump.handleKey("0")
    mock3.assert_called_with(ANY, True)
    assert(mock3.call_args.args[0].name() == "TestMode")
    mock3.reset_mock()
