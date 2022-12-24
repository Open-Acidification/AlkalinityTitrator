from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.titration.ManualTitration import ManualTitration
from titration.utils.Titrator import Titrator
from titration.utils import LCD_interface

# Test handleKey
@mock.patch.object(ManualTitration, "_setNextState")
def test_handleKey(setNextStateMock):
    manualTitration = ManualTitration(Titrator())

    manualTitration.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    setNextStateMock.reset_mock()
    assert manualTitration.subState == 2

    manualTitration.handleKey("1")
    assert manualTitration.values["p_direction"] == "1"
    assert manualTitration.subState == 3

    manualTitration.handleKey("0")
    assert manualTitration.subState == 4

    manualTitration.handleKey("1")
    assert manualTitration.subState == 5

    manualTitration.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    setNextStateMock.reset_mock()
    assert manualTitration.subState == 6

    manualTitration.handleKey("0")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "MainMenu"


# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(lcdOutMock):
    manualTitration = ManualTitration(Titrator())

    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.subState += 1
    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Direction (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.subState += 1
    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call(
                "Current pH: {0:>4.5f}".format(manualTitration.values["current_pH"]),
                line=1,
            ),
            mock.call("Add more HCl?", line=2),
            mock.call("(0 - No, 1 - Yes)", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.subState += 1
    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call(
                "Current pH: {0:>4.5f}".format(manualTitration.values["current_pH"]),
                line=1,
            ),
            mock.call("Degas?", line=2),
            mock.call("(0 - No, 1 - Yes)", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.subState += 1
    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Degas time", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.subState += 1
    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Return to", line=1),
            mock.call("main menu", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(ManualTitration, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_ManualTitration(lcdOutMock, setNextStateMock):
    manualTitration = ManualTitration(Titrator())

    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Volume", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    setNextStateMock.reset_mock()
    assert manualTitration.subState == 2

    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Direction (0/1):", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.handleKey("1")
    assert manualTitration.values["p_direction"] == "1"
    assert manualTitration.subState == 3

    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call(
                "Current pH: {0:>4.5f}".format(manualTitration.values["current_pH"]),
                line=1,
            ),
            mock.call("Add more HCl?", line=2),
            mock.call("(0 - No, 1 - Yes)", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.handleKey("0")
    assert manualTitration.subState == 4

    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call(
                "Current pH: {0:>4.5f}".format(manualTitration.values["current_pH"]),
                line=1,
            ),
            mock.call("Degas?", line=2),
            mock.call("(0 - No, 1 - Yes)", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.handleKey("1")
    assert manualTitration.subState == 5

    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Degas time", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_mock()

    manualTitration.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    setNextStateMock.reset_mock()
    assert manualTitration.subState == 6

    manualTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Return to", line=1),
            mock.call("main menu", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    manualTitration.handleKey("0")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "MainMenu"
