"""
The file to test the mock keypad
"""
import digitalio
from AlkalinityTitrator.titration.utils.devices import board_mock as board
from AlkalinityTitrator.titration.utils.devices.keypad_mock import Keypad


def test_keypad_create():
    """
    The function to test creating a mock keypad
    """
    keypad = Keypad()

    assert keypad.pin_R0 == board.D1
    assert keypad.pin_R1 == board.D6
    assert keypad.pin_R2 == board.D5
    assert keypad.pin_R3 == board.D19
    assert keypad.pin_C0 == board.D16
    assert keypad.pin_C1 == board.D26
    assert keypad.pin_C2 == board.D20
    assert keypad.pin_C3 == board.D21

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
