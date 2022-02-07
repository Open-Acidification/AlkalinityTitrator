import pytest
from io import StringIO
from titration.utils.UIState import MainMenu
from titration.utils.Titrator import Titrator

def test_handleKey():
    key_input = '*'
    mainMenu = MainMenu.MainMenu(Titrator())
    mainMenu.handleKey(key_input)
    assert(mainMenu.routineSelection == 2)
    mainMenu.handleKey(key_input)
    assert(mainMenu.routineSelection == 1)
