from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.calibration.calibrate_ph import CalibratePh
from titration.utils.ui_state.calibration.setup_calibration import SetupCalibration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    calibratePh = CalibratePh(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibratePh.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    updateStateMock.reset_called()
    assert calibratePh.subState == 2

    calibratePh.handleKey("1")
    assert calibratePh.subState == 3

    calibratePh.handleKey("a")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "SetupCalibration"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    calibratePh = CalibratePh(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Sol weight", line=1),
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
            mock.call("to record value", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibratePh.subState += 1
    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Recorded pH and volts:", line=1),
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


@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_CalibratePh(lcdOutMock, updateStateMock):
    calibratePh = CalibratePh(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Sol weight", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibratePh.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    updateStateMock.reset_called()
    assert calibratePh.subState == 2

    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Put sensor in buffer", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("to record value", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibratePh.handleKey("1")
    assert calibratePh.subState == 3

    calibratePh.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Recorded pH and volts:", line=1),
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

    calibratePh.handleKey("a")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "SetupCalibration"
