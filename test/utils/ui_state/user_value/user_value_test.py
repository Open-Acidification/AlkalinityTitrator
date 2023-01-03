from unittest import mock
from unittest.mock import ANY
from titration.utils.titrator import Titrator
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.update_settings.update_settings import UpdateSettings
from titration.utils.ui_state.user_value.user_value import UserValue
from titration.utils import lcd_interface


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    userValue = UserValue(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())), "Volume in pump:"
    )

    userValue.handleKey("A")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UpdateSettings"
    updateStateMock.reset_mock()

    # userValue.handleKey("B") is tested in the test_UserValue function
    # No General Case for this call due to pop an empty list

    userValue.handleKey("C")
    assert len(userValue.inputs) == 0
    assert userValue.decimal is False
    assert userValue.string == "_"

    userValue.handleKey("D")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UpdateSettings"
    updateStateMock.reset_mock()

    userValue.handleKey("1")
    assert userValue.string[-1] == "1"
    assert userValue.inputs[-1] == 1

    userValue.handleKey("*")
    assert userValue.inputs[-1] == "*"
    assert userValue.string[-1] == "."
    assert userValue.decimal is True


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    userValue = UserValue(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())), "Volume in pump:"
    )

    userValue.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )
    lcdOutMock.reset_called()


@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_UserValue(lcdOutMock, updateStateMock):
    userValue = UserValue(
        Titrator(), UpdateSettings(Titrator(), MainMenu(Titrator())), "Volume in pump:"
    )

    userValue.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )
    lcdOutMock.reset_called()

    userValue.handleKey("3")
    assert userValue.string == "3"
    assert userValue.inputs == [3]
    assert userValue.decimal is False

    userValue.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )
    lcdOutMock.reset_called()

    userValue.handleKey("*")
    assert userValue.string == "3."
    assert userValue.inputs == [3, "*"]
    assert userValue.decimal is True

    userValue.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )
    lcdOutMock.reset_called()

    # This is duplicate code of the last 15 lines, this is on purpose
    userValue.handleKey("*")
    assert userValue.string == "3."
    assert userValue.inputs == [3, "*"]
    assert userValue.decimal is True

    userValue.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )
    lcdOutMock.reset_called()

    userValue.handleKey("1")
    assert userValue.string == "3.1"
    assert userValue.inputs == [3, "*", 1]
    assert userValue.decimal is True

    userValue.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.1", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )
    lcdOutMock.reset_called()

    userValue.handleKey("B")
    assert userValue.string == "3."
    assert userValue.inputs == [3, "*"]
    assert userValue.decimal is True

    userValue.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3.", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )
    lcdOutMock.reset_called()

    userValue.handleKey("B")
    assert userValue.string == "3"
    assert userValue.inputs == [3]
    assert userValue.decimal is False

    userValue.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("3", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )
    lcdOutMock.reset_called()

    userValue.handleKey("C")
    assert userValue.string == "_"
    assert userValue.inputs == []
    assert userValue.decimal is False

    userValue.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Volume in pump:", line=1),
            mock.call("_", style=2, line=2),
            mock.call("* = .       B = BS", line=3),
            mock.call("A = accept  C = Clr", line=4),
        ]
    )
    lcdOutMock.reset_called()

    userValue.handleKey("A")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UpdateSettings"
    updateStateMock.reset_mock()
