import ph_probe_mock
import board_mock
import pytest

def test_ph_create():
    ph = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    assert ph != None

def test_ph_create_none():
    ph = ph_probe_mock.pH_Probe(None, None)
    assert ph != None

def test_ph_voltage():
    ph_1 = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    ph_2 = ph_probe_mock.pH_Probe(None, None)

    assert ph_1.voltage() == 3.14159
    assert ph_2.voltage() == 3.14159

def test_ph_set_gain():
    ph = ph_probe_mock.pH_Probe(board_mock.SCL, board_mock.SDA)
    gain_options = [2 / 3, 1, 2, 4, 8, 16]

    for gain in gain_options:
        ph.set_gain(gain)
        assert ph.get_gain() == gain
    
    with pytest.raises(ValueError):
        ph.set_gain(0)
    
    with pytest.raises(ValueError):
        ph.set_gain(32)