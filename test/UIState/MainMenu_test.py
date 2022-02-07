import pytest
from io import StringIO
from titration.utils.UIState import MainMenu

def test_handleKey(monkeypatch):
    key_input = StringIO('*\n')
    monkeypatch.setattr('sys.stdin', key_input)
    mainMenu = MainMenu()
    mainMenu.handleKey(key_input)
    assert(mainMenu.routineSelection == 2)
    mainMenu.handleKey(key_input)
    assert(mainMenu.routineSelection == 1)
