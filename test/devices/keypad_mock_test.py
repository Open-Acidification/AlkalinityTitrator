"""
The file to test the mock keypad
"""
import digitalio

from titration import constants
from titration.devices.library import Keypad, board


def test_keypad_create():
    """
    The function to test creating a mock keypad
    """
    keypad = Keypad()

    assert keypad.pin_r0 == board.D1
    assert keypad.pin_r1 == board.D6
    assert keypad.pin_r2 == board.D5
    assert keypad.pin_r3 == board.D19
    assert keypad.pin_c0 == board.D16
    assert keypad.pin_c1 == board.D26
    assert keypad.pin_c2 == board.D20
    assert keypad.pin_c3 == board.D21

    assert keypad.pin_r0.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_r1.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_r2.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_r3.direction == digitalio.Direction.OUTPUT
    assert keypad.pin_c0.direction == digitalio.Direction.INPUT
    assert keypad.pin_c1.direction == digitalio.Direction.INPUT
    assert keypad.pin_c2.direction == digitalio.Direction.INPUT
    assert keypad.pin_c3.direction == digitalio.Direction.INPUT

    assert keypad.pin_c0.pull == digitalio.Pull.DOWN
    assert keypad.pin_c1.pull == digitalio.Pull.DOWN
    assert keypad.pin_c2.pull == digitalio.Pull.DOWN
    assert keypad.pin_c3.pull == digitalio.Pull.DOWN


def test_set_key():
    """
    The function to test setting a pressed key
    """
    keypad = Keypad()

    keypad.set_key("A")
    assert keypad.key_pressed == "A"


def test_get_key():
    """
    The function to test getting a pressed key from the GUI
    """
    keypad = Keypad()

    constants.GUI_ENABLED = True
    keypad.key_pressed = "A"
    assert keypad.get_key() == "A"
