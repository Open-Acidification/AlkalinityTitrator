from unittest import mock
from titration.utils.Titrator import Titrator
from titration.utils import constants, interfaces
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
@mock.patch.object(interfaces, "lcd_out")
def test_loop(mock):
    primePump = PrimePump(Titrator(), Titrator())

    primePump.loop()
    assert mock.called_with("Choose 0 to return", line=3)
    mock.reset_called()

    primePump.subState += 1
    primePump.loop()
    assert mock.called_with("Choose 0 to return", line=3)

# Test PrimePump
@mock.patch.object(PrimePump, "_setNextState")
@mock.patch.object(interfaces, "lcd_out")
def test_PrimePump(mock1, mock2):
    primePump = PrimePump(Titrator(), Titrator())

    primePump.loop()
    assert mock1.called_with("Choose 0 to return", line=3)
    mock1.reset_called()

    primePump.handleKey(3)
    assert(primePump.values['selection'] == 3)
    assert(primePump.subState == 2)

    primePump.loop()
    assert mock1.called_with("Choose 0 to return", line=3)
    mock1.reset_called()

    primePump.handleKey(1)
    assert(primePump.values['selection'] == 1)

    primePump.loop()
    assert mock1.called_with("Choose 0 to return", line=3)
    mock1.reset_called()

    primePump.handleKey(0)
    assert(primePump.values['selection'] == 0)
    assert mock2.called
