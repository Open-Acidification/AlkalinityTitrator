from unittest.mock import ANY
from unittest import mock
from titration.utils.ui_state import main_menu
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, constants


# Test handleKey
@mock.patch.object(main_menu.MainMenu, "_setNextState")
def test_handleKey(mock):
    mainMenu = main_menu.MainMenu(Titrator())

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
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    mainMenu = main_menu.MainMenu(Titrator())

    mainMenu.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Run titration", line=1),
            mock.call("Calibrate sensors", line=2),
            mock.call("Prime pump", line=3),
            mock.call("Page 2", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    mainMenu.subState = 2
    mainMenu.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Update settings", line=1),
            mock.call("Test mode", line=2),
            mock.call("Exit", line=3),
            mock.call("Page 1", line=4),
        ]
    )


# Test MainMenu
@mock.patch.object(lcd_interface, "lcd_out")
@mock.patch.object(main_menu.MainMenu, "_setNextState")
def test_MainMenu(mock1, mock2):
    mainMenu = main_menu.MainMenu(Titrator())

    mainMenu.loop()
    mock2.assert_has_calls(
        [
            mock.call("Run titration", line=1),
            mock.call("Calibrate sensors", line=2),
            mock.call("Prime pump", line=3),
            mock.call("Page 2", line=4),
        ]
    )
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
    mock2.assert_has_calls(
        [
            mock.call("Update settings", line=1),
            mock.call("Test mode", line=2),
            mock.call("Exit", line=3),
            mock.call("Page 1", line=4),
        ]
    )
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
