from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces, LCD
from titration.utils.UIState.prime_pump.PrimePump import PrimePump

# Test handleKey
@mock.patch.object(PrimePump, "_setNextState")
def test_handleKey(mock):
    primePump = PrimePump(Titrator(), Titrator())

    primePump.handleKey(3)
    assert(primePump.values['selection'] == 3)
    assert(primePump.subState == 2)

    primePump.handleKey(1)
    assert(primePump.values['selection'] == 1)

    primePump.handleKey(0)
    assert(primePump.values['selection'] == 0)
    assert mock.called

# Test loop
@mock.patch.object(LCD, "lcd_out")
def test_loop(mock1):
    primePump = PrimePump(Titrator(), Titrator())

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
@mock.patch.object(LCD, "lcd_out")
def test_PrimePump(mock1, mock2):
    primePump = PrimePump(Titrator(), Titrator())

    primePump.loop()
    mock1.assert_has_calls(
        [mock.call("How many pumps?", line=1),
        mock.call("Choose a number", line=2),
        mock.call("Choose 0 to return", line=3)]
    )
    mock1.reset_called()

    primePump.handleKey(3)
    assert(primePump.values['selection'] == 3)
    assert(primePump.subState == 2)

    primePump.loop()
    mock1.assert_has_calls(
        [mock.call("How many more?", line=1),
        mock.call("Choose a number", line=2),
        mock.call("Choose 0 to return", line=3)]
    )
    mock1.reset_called()

    primePump.handleKey(1)
    assert(primePump.values['selection'] == 1)

    mock1.assert_has_calls(
        [mock.call("How many more?", line=1),
        mock.call("Choose a number", line=2),
        mock.call("Choose 0 to return", line=3)]
    )

    primePump.handleKey(0)
    assert(primePump.values['selection'] == 0)
    assert mock2.called
