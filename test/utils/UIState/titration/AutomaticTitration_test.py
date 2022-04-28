from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.titration.AutomaticTitration import AutomaticTitration
from titration.utils.titrator import Titrator
from titration.utils import constants, LCD

# Test handleKey
@mock.patch.object(AutomaticTitration, "_setNextState")
def test_handleKey(mock):
    initialTitration = AutomaticTitration(Titrator())

    initialTitration.subState += 3
    
    initialTitration.handleKey("0")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "MainMenu")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD, "lcd_out")
def test_loop(mock1):
    initialTitration = AutomaticTitration(Titrator())

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call(
            "Titrating to {} pH".format(str(initialTitration.values['pH_target'])),
            style=constants.LCD_CENT_JUST,
            line=4
        )]
    )
    mock1.reset_called()
    assert(initialTitration.subState == 2)

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Mixing...", style=constants.LCD_CENT_JUST, line=4)]
    )
    mock1.reset_called()
    assert(initialTitration.subState == 3)

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("pH value {} reached".format(initialTitration.values['current_pH']), line=4)]
    )
    mock1.reset_called()
    assert(initialTitration.subState == 4)

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Return to", line=1),
        mock.call("main menu: 0", line=2),
        mock.call("Exit: 1", line=3)])

@mock.patch.object(AutomaticTitration, "_setNextState")
@mock.patch.object(LCD, "lcd_out")
def test_AutomaticTitration(mock1, mock2):
    initialTitration = AutomaticTitration(Titrator())

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call(
            "Titrating to {} pH".format(str(initialTitration.values['pH_target'])),
            style=constants.LCD_CENT_JUST,
            line=4
        )]
    )
    mock1.reset_called()
    assert(initialTitration.subState == 2)

    initialTitration.handleKey("1")

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Mixing...", style=constants.LCD_CENT_JUST, line=4)]
    )
    mock1.reset_called()    
    assert(initialTitration.subState == 3)

    initialTitration.handleKey("1")

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("pH value {} reached".format(initialTitration.values['current_pH']), line=4)]
    )
    mock1.reset_called()
    assert(initialTitration.subState == 4)

    initialTitration.loop()
    mock1.assert_has_calls(
        [mock.call("Return to", line=1),
        mock.call("main menu: 0", line=2),
        mock.call("Exit: 1", line=3)])
    mock1.reset_called()

    initialTitration.handleKey("0")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "MainMenu")
