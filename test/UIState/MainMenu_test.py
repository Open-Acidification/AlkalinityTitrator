from json.tool import main
import pytest
from unittest import mock
from io import StringIO
from titration.utils.UIState import MainMenu
from titration.utils.Titrator import Titrator
from titration.utils import interfaces, constants
from titration.utils.UIState.titration import SetupTitration
from titration.utils.UIState.calibration import SetupCalibration

# Test handleKey
@mock.patch.object(MainMenu.MainMenu, "_setNextState")
def test_handleKey(mock):
    mainMenu = MainMenu.MainMenu(Titrator())

    mainMenu.handleKey(1)
    mock.assert_called()
    mock.reset_mock()

    mainMenu.handleKey(2)
    mock.assert_called()
    mock.reset_mock()

    mainMenu.handleKey(3)
    mock.assert_called()
    mock.reset_mock()

    mainMenu.handleKey('*')
    assert(mainMenu.routineSelection == 2)

    mainMenu.handleKey(4)
    mock.assert_called()
    mock.reset_mock()

    mainMenu.handleKey(5)
    mock.assert_called()
    mock.reset_mock()

    mainMenu.handleKey(6)
    mock.assert_called()
    mock.reset_mock()

    mainMenu.handleKey('*')
    assert(mainMenu.routineSelection == 1)

# Test loop
@mock.patch.object(interfaces, "display_list")
def test_loop(mock):
    mainMenu = MainMenu.MainMenu(Titrator())

    mainMenu.loop()
    mock.assert_called_with(constants.ROUTINE_OPTIONS_1)
    mock.reset_mock()

    mainMenu.routineSelection = 2
    mainMenu.loop()
    mock.assert_called_with(constants.ROUTINE_OPTIONS_2)

# Test MainMenu fully
@mock.patch.object(MainMenu.MainMenu, "_setNextState")
@mock.patch.object(interfaces, "display_list")
def test_MainMenu(mock1, mock2):
    mainMenu = MainMenu.MainMenu(Titrator())

    mainMenu.loop()
    mock2.assert_called_with(constants.ROUTINE_OPTIONS_1)
    mock2.reset_mock()
    
    mainMenu.handleKey(1)
    mock1.assert_called()
    mock1.reset_mock()

    mainMenu.handleKey(2)
    mock1.assert_called()
    mock1.reset_mock()

    mainMenu.handleKey(3)
    mock1.assert_called()
    mock1.reset_mock()

    mainMenu.handleKey('*')
    assert(mainMenu.routineSelection == 2)

    mainMenu.loop()
    mock2.assert_called_with(constants.ROUTINE_OPTIONS_2)
    mock2.reset_mock()

    mainMenu.handleKey(4)
    mock1.assert_called()
    mock1.reset_mock()

    mainMenu.handleKey(5)
    mock1.assert_called()
    mock1.reset_mock()

    mainMenu.handleKey(6)
    mock1.assert_called()
    mock1.reset_mock()

    mainMenu.handleKey('*')
    assert(mainMenu.routineSelection == 1)
