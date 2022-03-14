from unittest import mock
from titration.utils.UIState.titration.AutomaticTitration import AutomaticTitration
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces

# Test handleKey
@mock.patch.object(AutomaticTitration, "_setNextState")
def test_handleKey(mock):
    initialTitration = AutomaticTitration(Titrator())

    initialTitration.handleKey(1)
    assert not mock.called
    mock.reset_mock()

    initialTitration.subState += 1
    initialTitration.handleKey(1)
    assert not mock.called

    initialTitration.subState += 1
    initialTitration.handleKey(1)
    assert not mock.called

    initialTitration.subState += 1
    initialTitration.handleKey(0)
    assert mock.called

# Test loop
@mock.patch.object(interfaces, "lcd_out")
def test_loop(mock):
    initialTitration = AutomaticTitration(Titrator())

    initialTitration.loop()
    mock.assert_called_with(               
                "Titrating to {} pH".format(str(initialTitration.values['pH_target'])),   # TODO: Change pH_target
                style=constants.LCD_CENT_JUST,
                line=4
    )
    assert(initialTitration.subState == 2)
    mock.reset_mock()

    initialTitration.loop()
    mock.assert_called_with("Mixing...", style=constants.LCD_CENT_JUST, line=4)
    assert(initialTitration.subState == 3)
    mock.reset_mock()

    initialTitration.loop()
    mock.assert_called_with("pH value {} reached".format(initialTitration.values['current_pH']), line=4)
    assert(initialTitration.subState == 4)
    mock.reset_mock()

    initialTitration.loop()
    mock.assert_called_with("Exit: 1", line=3)

@mock.patch.object(AutomaticTitration, "_setNextState")
@mock.patch.object(interfaces, "lcd_out")
def test_AutomaticTitration(mock1, mock2):
    initialTitration = AutomaticTitration(Titrator())

    initialTitration.loop()
    mock1.assert_called_with(               
                "Titrating to {} pH".format(str(initialTitration.values['pH_target'])),   # TODO: Change pH_target
                style=constants.LCD_CENT_JUST,
                line=4
    )
    assert(initialTitration.subState == 2)
    mock1.reset_mock()

    initialTitration.handleKey(1)

    initialTitration.loop()
    mock1.assert_called_with("Mixing...", style=constants.LCD_CENT_JUST, line=4)
    assert(initialTitration.subState == 3)
    mock1.reset_mock()

    initialTitration.handleKey(1)

    initialTitration.loop()
    mock1.assert_called_with("pH value {} reached".format(initialTitration.values['current_pH']), line=4)
    assert(initialTitration.subState == 4)
    mock1.reset_mock()

    initialTitration.loop()
    mock1.assert_called_with("Exit: 1", line=3)
    mock1.reset_mock()

    initialTitration.handleKey(0)
    mock2.assert_called()
