from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.titration.ManualTitration import ManualTitration
from titration.utils.titrator import Titrator
from titration.utils import LCD_interface

# Test handleKey
@mock.patch.object(ManualTitration, "_setNextState")
def test_handleKey(mock):
    manualTitration = ManualTitration(Titrator())

    manualTitration.handleKey("5")
    assert(manualTitration.values['p_direction'] == "5")
    assert(manualTitration.subState == 2)

    manualTitration.handleKey("1")
    assert(manualTitration.subState == 1)

    manualTitration.handleKey("6")
    assert(manualTitration.values['p_direction'] == "6")

    manualTitration.handleKey("2")
    assert(manualTitration.subState == 3)

    manualTitration.handleKey("1")
    assert(manualTitration.subState == 4)

    manualTitration.handleKey("1")
    assert(manualTitration.subState == 5)

    manualTitration.handleKey("0")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "MainMenu")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD_interface, "read_user_value", return_value=5.5)
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(mock1, mock2):
    manualTitration = ManualTitration(Titrator())

    manualTitration.loop()
    assert(manualTitration.values['p_volume'] == 5.5)
    mock2.assert_called_with("Volume: ")
    mock2.reset_called()
    mock1.assert_has_calls(
        [mock.call("Direction (0/1): ", line=1)
    ])
    mock1.reset_mock()

    manualTitration.subState += 1
    manualTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Current pH: {0:>4.5f}".format(manualTitration.values['current_pH']), line=1), 
        mock.call("Add more HCl?", line=2),
        mock.call("(0 - No, 1 - Yes)", line=3),
        mock.call("", line=4)
    ])
    mock1.reset_mock()

    manualTitration.subState += 1
    manualTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Current pH: {0:>4.5f}".format(manualTitration.values['current_pH']), line=1),
        mock.call("Degas?", 1),
        mock.call("(0 - No, 1 - Yes)", line=2)]
    )

    manualTitration.subState += 1
    manualTitration.values['user_choice'] = 1
    manualTitration.loop()
    mock2.assert_called_with("Degas time (s):")
    mock2.reset_called()
    assert(manualTitration.values['degas_time'] == 5.5)

    manualTitration.subState += 1
    manualTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Return to", line=1),
        mock.call("main menu: 0", line=2),
        mock.call("Exit: 1", line=3)]
    )

@mock.patch.object(ManualTitration, "_setNextState")
@mock.patch.object(LCD_interface, "read_user_value", return_value=5.5)
@mock.patch.object(LCD_interface, "lcd_out")
def test_ManualTitration(mock1, mock2, mock3):
    manualTitration = ManualTitration(Titrator())

    manualTitration.loop()
    assert(manualTitration.values['p_volume'] == 5.5)
    mock2.assert_called_with("Volume: ")
    mock2.reset_called()
    mock1.assert_has_calls(
        [mock.call("Direction (0/1): ", line=1)
    ])
    mock1.reset_mock()

    manualTitration.handleKey("1")
    assert(manualTitration.values['p_direction'] == "1")
    assert(manualTitration.subState == 2)

    manualTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Current pH: {0:>4.5f}".format(manualTitration.values['current_pH']), line=1), 
        mock.call("Add more HCl?", line=2),
        mock.call("(0 - No, 1 - Yes)", line=3),
        mock.call("", line=4)
    ])
    mock1.reset_mock()

    manualTitration.handleKey("2")
    assert(manualTitration.subState == 3)

    manualTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Current pH: {0:>4.5f}".format(manualTitration.values['current_pH']), line=1),
        mock.call("Degas?", 1),
        mock.call("(0 - No, 1 - Yes)", line=2)]
    )
    mock1.reset_mock()

    manualTitration.handleKey("1")
    assert(manualTitration.subState == 4)
    
    manualTitration.loop()
    mock2.assert_called_with("Degas time (s):")
    mock2.reset_called()
    assert(manualTitration.values['degas_time'] == 5.5)

    manualTitration.handleKey("1")
    assert(manualTitration.subState == 5)

    manualTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Return to", line=1),
        mock.call("main menu: 0", line=2),
        mock.call("Exit: 1", line=3)]
    )

    manualTitration.handleKey("0")
    mock3.assert_called_with(ANY, True)
    assert(mock3.call_args.args[0].name() == "MainMenu")
