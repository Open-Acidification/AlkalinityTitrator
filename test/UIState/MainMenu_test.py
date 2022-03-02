import pytest
from unittest import mock
from io import StringIO
from titration.utils.UIState import MainMenu
from titration.utils.Titrator import Titrator
from titration.utils import interfaces, constants
from titration.utils.UIState.titration import SetupTitration
from titration.utils.UIState.calibration import SetupCalibration

# Test handleKey
def test_handleKey(mocker):
    mainMenu = MainMenu.MainMenu(Titrator())

    key_input = '*'
    mainMenu.handleKey(key_input)
    assert(mainMenu.routineSelection == 2)
    mainMenu.handleKey(key_input)
    assert(mainMenu.routineSelection == 1)

# Test _setNextState
@mock.patch.object(MainMenu.MainMenu, "_setNextState")
def test_stateChanges(mock):
    mainMenu = MainMenu.MainMenu(Titrator())

    mainMenu.handleKey('1')
    mock.assert_called()

    mainMenu.handleKey('2')
    mock.assert_called()

# Test loop
@mock.patch.object(interfaces, "display_list")
def test_loop(mock):
    mainMenu = MainMenu.MainMenu(Titrator())

    mainMenu.loop()
    mock.assert_called_with(constants.ROUTINE_OPTIONS_1)

    mainMenu.handleKey('*')
    mainMenu.loop()
    mock.assert_called_with(constants.ROUTINE_OPTIONS_2)

    mainMenu.handleKey('*')
    mainMenu.loop()
    mock.assert_called_with(constants.ROUTINE_OPTIONS_1)
