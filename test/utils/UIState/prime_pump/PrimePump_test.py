from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.UIState.test_mode.TestMode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import LCD_interface
from titration.utils.UIState.prime_pump.PrimePump import PrimePump

# Test handleKey
@mock.patch.object(PrimePump, "_setNextState")
def test_handleKey(mock):
    primePump = PrimePump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    primePump.handleKey("3")
    assert(primePump.values['selection'] == "3")
    assert(primePump.subState == 2)

    primePump.handleKey("1")
    assert(primePump.values['selection'] == "1")

    primePump.handleKey("0")
    assert(primePump.values['selection'] == "0")
    mock.assert_called_with(ANY, True)
    assert(mock.call_args.args[0].name() == "TestMode")
    mock.reset_mock()

# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(mock1):
    primePump = PrimePump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    primePump.loop()
    mock1.assert_has_calls(
        [mock.call("How many pumps?", line=1),
        mock.call("Choose a number", line=2),
        mock.call("Choose 0 to return", line=3)]
    )
    mock1.reset_called()

    primePump.subState += 1
    primePump.loop()
    mock1.assert_has_calls(
        [mock.call("How many more?", line=1),
        mock.call("Choose a number", line=2),
        mock.call("Choose 0 to return", line=3)]
    )

# Test PrimePump
@mock.patch.object(PrimePump, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_PrimePump(mock1, mock2):
    primePump = PrimePump(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    primePump.loop()
    mock1.assert_has_calls(
        [mock.call("How many pumps?", line=1),
        mock.call("Choose a number", line=2),
        mock.call("Choose 0 to return", line=3)]
    )
    mock1.reset_called()

    primePump.handleKey("3")
    assert(primePump.values['selection'] == "3")
    assert(primePump.subState == 2)

    primePump.loop()
    mock1.assert_has_calls(
        [mock.call("How many more?", line=1),
        mock.call("Choose a number", line=2),
        mock.call("Choose 0 to return", line=3)]
    )
    mock1.reset_called()

    primePump.handleKey("1")
    assert(primePump.values['selection'] == "1")

    mock1.assert_has_calls(
        [mock.call("How many more?", line=1),
        mock.call("Choose a number", line=2),
        mock.call("Choose 0 to return", line=3)]
    )

    primePump.handleKey("0")
    assert(primePump.values['selection'] == "0")
    mock2.assert_called_with(ANY, True)
    assert(mock2.call_args.args[0].name() == "TestMode")
    mock2.reset_mock()
