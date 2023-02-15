"""
Module to test keypad calls in the terminal
"""

from AlkalinityTitrator.titration.utils.devices import board_mock as board
from AlkalinityTitrator.titration.utils.devices import keypad_mock as keypad


def test_keypad_create():
    """
    Function to create a mock keypad for testing
    """
    key = keypad.Keypad(
        board.D0, board.D1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7
    )
    assert key is not None


def test_keypad_create_null():
    """
    Function to create a null keypad for testing
    """
    key = keypad.Keypad(None, None, None, None, None, None, None, None)
    assert key is not None
