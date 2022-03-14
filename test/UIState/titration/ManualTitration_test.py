from unittest import mock
from titration.utils.UIState.titration.ManualTitration import ManualTitration
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces

# Test handleKey
@mock.patch.object(ManualTitration, "_setNextState")
def test_handleKey(mock):
    manualTitration = ManualTitration(Titrator())

    manualTitration.handleKey(5)
    assert(manualTitration.values['p_direction'] == 5)
    assert(manualTitration.subState == 2)

    manualTitration.handleKey(1)
    assert(manualTitration.subState == 1)

    manualTitration.handleKey(6)
    assert(manualTitration.values['p_direction'] == 6)

    manualTitration.handleKey(2)
    assert(manualTitration.subState == 3)

    manualTitration.handleKey(1)
    assert(manualTitration.subState == 4)

    manualTitration.handleKey(1)
    assert(manualTitration.subState == 5)

    manualTitration.handleKey(0)
    mock.assert_called()

# Test loop
@mock.patch.object(interfaces, "read_user_value", return_value=5.5)
@mock.patch.object(interfaces, "lcd_out")
def test_loop(mock1, mock2):
    manualTitration = ManualTitration(Titrator())

    manualTitration.loop()
    assert(manualTitration.values['p_volume'] == 5.5)
    mock1.reset_mock()

    manualTitration.subState += 1
    manualTitration.loop()
    # mock1.assert_called_with("", line=4)
    mock1.assert_has_calls([mock1.call("(0 - No, 1 - Yes)", line=3), mock1.call("", line=4)])
    mock1.reset_mock()

    manualTitration.subState += 1
    manualTitration.loop()
    mock1.assert_called_with("(0 - No, 1 - Yes)", line=2)

    manualTitration.subState += 1
    manualTitration.values['user_choice'] = 1
    manualTitration.loop()
    assert(manualTitration.values['degas_time'] == 5.5)

@mock.patch.object(ManualTitration, "_setNextState")
@mock.patch.object(interfaces, "read_user_value", return_value=5.5)
@mock.patch.object(interfaces, "lcd_out")
def test_ManualTitration(mock1, mock2, mock3):
    manualTitration = ManualTitration(Titrator())

    manualTitration.loop()
    assert(manualTitration.values['p_volume'] == 5.5)
    mock1.reset_mock()

    manualTitration.handleKey(1)
    assert(manualTitration.values['p_direction'] == 1)
    assert(manualTitration.subState == 2)

    manualTitration.loop()
    mock1.assert_called_with("", line=4)
    mock1.reset_mock()

    manualTitration.handleKey(2)
    assert(manualTitration.subState == 3)

    manualTitration.loop()
    mock1.assert_called_with("(0 - No, 1 - Yes)", line=2)

    manualTitration.handleKey(1)
    assert(manualTitration.subState == 4)
    
    manualTitration.loop()
    assert(manualTitration.values['degas_time'] == 5.5)

    manualTitration.handleKey(1)
    assert(manualTitration.subState == 5)

    manualTitration.handleKey(0)
    mock3.assert_called()
