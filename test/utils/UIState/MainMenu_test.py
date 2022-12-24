from unittest.mock import ANY
from unittest import mock
from titration.utils.UIState import MainMenu
from titration.utils.Titrator import Titrator
from titration.utils import LCD_interface, constants

# Test handleKey
@mock.patch.object(MainMenu.MainMenu, "_setNextState")
def test_handleKey(mock):
    mainMenu = MainMenu.MainMenu(Titrator())

    mainMenu.handleKey("1")
    mock.assert_called_with(ANY, True)
    assert mock.call_args.args[0].name() == "SetupTitration"
    mock.reset_mock()

    mainMenu.handleKey("2")
    mock.assert_called_with(ANY, True)
    assert mock.call_args.args[0].name() == "SetupCalibration"
    mock.reset_mock()

    mainMenu.handleKey("3")
    mock.assert_called_with(ANY, True)
    assert mock.call_args.args[0].name() == "PrimePump"
    mock.reset_mock()

    mainMenu.handleKey("*")
    assert mainMenu.subState == 2

    mainMenu.handleKey("4")
    mock.assert_called_with(ANY, True)
    assert mock.call_args.args[0].name() == "UpdateSettings"
    mock.reset_mock()

    mainMenu.handleKey("5")
    mock.assert_called_with(ANY, True)
    assert mock.call_args.args[0].name() == "TestMode"
    mock.reset_mock()

    mainMenu.handleKey("*")
    assert mainMenu.subState == 1


# Test loop
@mock.patch.object(LCD_interface, "display_list")
def test_loop(mock):
    mainMenu = MainMenu.MainMenu(Titrator())

    mainMenu.loop()
    mock.assert_called_with(constants.ROUTINE_OPTIONS_1)
    mock.reset_mock()

    mainMenu.subState = 2
    mainMenu.loop()
    mock.assert_called_with(constants.ROUTINE_OPTIONS_2)


# Test MainMenu
@mock.patch.object(LCD_interface, "display_list")
@mock.patch.object(MainMenu.MainMenu, "_setNextState")
def test_MainMenu(mock1, mock2):
    mainMenu = MainMenu.MainMenu(Titrator())

    mainMenu.loop()
    mock2.assert_called_with(constants.ROUTINE_OPTIONS_1)
    mock2.reset_mock()
    
    mainMenu.handleKey("1")
    mock1.assert_called_with(ANY, True)
    assert mock1.call_args.args[0].name() == "SetupTitration"
    mock1.reset_mock()

    mainMenu.handleKey("2")
    mock1.assert_called_with(ANY, True)
    assert mock1.call_args.args[0].name() == "SetupCalibration"
    mock1.reset_mock()

    mainMenu.handleKey("3")
    mock1.assert_called_with(ANY, True)
    assert mock1.call_args.args[0].name() == "PrimePump"
    mock1.reset_mock()

    mainMenu.handleKey("*")
    assert mainMenu.subState == 2

    mainMenu.loop()
    mock2.assert_called_with(constants.ROUTINE_OPTIONS_2)
    mock2.reset_mock()

    mainMenu.handleKey("4")
    mock1.assert_called_with(ANY, True)
    assert mock1.call_args.args[0].name() == "UpdateSettings"
    mock1.reset_mock()

    mainMenu.handleKey("5")
    mock1.assert_called_with(ANY, True)
    assert mock1.call_args.args[0].name() == "TestMode"
    mock1.reset_mock()

    mainMenu.handleKey("*")
    assert mainMenu.subState == 1
