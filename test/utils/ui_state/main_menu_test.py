from unittest.mock import ANY
from unittest import mock
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface


# Test handleKey
@mock.patch.object(MainMenu, "_setNextState")
def test_handleKey(setNextStateMock):
    mainMenu = MainMenu(Titrator())

    mainMenu.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "SetupTitration"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("2")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "SetupCalibration"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("3")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "PrimePump"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("*")
    assert mainMenu.subState == 2

    mainMenu.handleKey("4")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UpdateSettings"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("5")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("*")
    assert mainMenu.subState == 1


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    mainMenu = MainMenu(Titrator())

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
@mock.patch.object(MainMenu, "_setNextState")
def test_MainMenu(setNextStateMock, lcdOutMock):
    mainMenu = MainMenu(Titrator())

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

    mainMenu.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "SetupTitration"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("2")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "SetupCalibration"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("3")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "PrimePump"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("*")
    assert mainMenu.subState == 2

    mainMenu.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Update settings", line=1),
            mock.call("Test mode", line=2),
            mock.call("Exit", line=3),
            mock.call("Page 1", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    mainMenu.handleKey("4")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UpdateSettings"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("5")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"
    setNextStateMock.reset_mock()

    mainMenu.handleKey("*")
    assert mainMenu.subState == 1
