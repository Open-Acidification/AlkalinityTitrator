"""
The file to test the mock keypad
"""
import digitalio
from titration.utils.devices import board_mock as board
from titration.utils.devices.keypad_mock import Keypad


def test_keypad_create():
    """
    The function to test creating a mock keypad
    """
    keypad = Keypad()

    assert keypad.pin_r_zero == board.D1
    assert keypad.pin_r_one == board.D6
    assert keypad.pin_r_two == board.D5
    assert keypad.pin_r_three == board.D19
    assert keypad.pin_c_zero == board.D16
    assert keypad.pin_c_one == board.D26
    assert keypad.pin_c_two == board.D20
    assert keypad.pin_c_three == board.D21

    assert keypad.pin_r_zero.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_r_one.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_r_two.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_r_three.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_c_zero.direction == digitalio.Direction.INPUT
    assert keypad.pin_c_one.direction == digitalio.Direction.INPUT
    assert keypad.pin_c_two.direction == digitalio.Direction.INPUT
    assert keypad.pin_c_three.direction == digitalio.Direction.INPUT

    assert keypad.pin_c_zero.pull == digitalio.Pull.DOWN
    assert keypad.pin_c_one.pull == digitalio.Pull.DOWN
    assert keypad.pin_c_two.pull == digitalio.Pull.DOWN
    assert keypad.pin_c_three.pull == digitalio.Pull.DOWN
