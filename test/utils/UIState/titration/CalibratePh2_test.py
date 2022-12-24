from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.titration.CalibratePh import CalibratePh
from titration.utils.Titrator import Titrator
from titration.utils import LCD_interface


# Test handleKey
@mock.patch.object(CalibratePh, "_setNextState")
def test_handleKey(setNextStateMock):
    calibratePh = CalibratePh(Titrator())

    calibratePh.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    setNextStateMock.reset_mock()
    assert calibratePh.subState == 2

    calibratePh.handleKey("1")
    assert calibratePh.subState == 3

    calibratePh.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "InitialTitration"
    setNextStateMock.reset_mock()


# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(lcdOutMock):
    calibratePh = CalibratePh(Titrator())

    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter buffer pH", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibratePh.subState += 1
    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Put sensor in buffer", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibratePh.subState += 1
    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Recorded pH, volts:", line=1),
            mock.call(
                "{0:>2.5f} pH, {1:>3.4f} V".format(
                    calibratePh.values["buffer1_actual_pH"],
                    calibratePh.values["buffer1_measured_volts"],
                ),
                line=2,
            ),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(CalibratePh, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_CalibratePh(lcdOutMock, setNextStateMock):
    calibratePh = CalibratePh(Titrator())

    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter buffer pH", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibratePh.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    setNextStateMock.reset_mock()
    assert calibratePh.subState == 2

    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Put sensor in buffer", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibratePh.handleKey("1")
    assert calibratePh.subState == 3

    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Recorded pH, volts:", line=1),
            mock.call(
                "{0:>2.5f} pH, {1:>3.4f} V".format(
                    calibratePh.values["buffer1_actual_pH"],
                    calibratePh.values["buffer1_measured_volts"],
                ),
                line=2,
            ),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    calibratePh.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "InitialTitration"
