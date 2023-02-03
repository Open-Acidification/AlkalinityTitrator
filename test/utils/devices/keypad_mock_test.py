"""
The file to test the mock keypad
"""
import pytest
import digitalio
from titration.utils.devices import board_mock as board
from titration.utils.devices.keypad_mock import Keypad


def test_keypad_create():
    """
    The function to test creating a mock keypad
    """
    keypad = Keypad(
        board.D0, board.D1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7
    )

    assert keypad.pin_R0 == board.D0
    assert keypad.pin_R1 == board.D1
    assert keypad.pin_R2 == board.D2
    assert keypad.pin_R3 == board.D3
    assert keypad.pin_C0 == board.D4
    assert keypad.pin_C1 == board.D5
    assert keypad.pin_C2 == board.D6
    assert keypad.pin_C3 == board.D7

    assert keypad.pin_R0.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_R1.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_R2.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_R3.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_C0.direction == digitalio.Direction.INPUT
    assert keypad.pin_C1.direction == digitalio.Direction.INPUT
    assert keypad.pin_C2.direction == digitalio.Direction.INPUT
    assert keypad.pin_C3.direction == digitalio.Direction.INPUT

    assert keypad.pin_C0.pull == digitalio.Pull.DOWN
    assert keypad.pin_C1.pull == digitalio.Pull.DOWN
    assert keypad.pin_C2.pull == digitalio.Pull.DOWN
    assert keypad.pin_C3.pull == digitalio.Pull.DOWN


def test_keypad_create_null():
    """
    The function to test creating a null mock keypad
    """
    with pytest.raises(Exception):
        Keypad(None, None, None, None, None, None, None, None)
