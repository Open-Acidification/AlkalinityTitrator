import titration.board_mock as board
import titration.keypad_mock as keypad


def test_keypad_create():
    key = keypad.Keypad(
        board.D0, board.D1, board.D2, board.D3, board.D4, board.D5, board.D6, board.D7
    )
    assert key != None


def test_keypad_create_null():
    key = keypad.Keypad(None, None, None, None, None, None, None, None)
    assert key != None
