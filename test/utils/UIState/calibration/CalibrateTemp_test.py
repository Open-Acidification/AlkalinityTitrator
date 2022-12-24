from unittest import mock
from unittest.mock import ANY
from titration.utils.UIState.MainMenu import MainMenu
from titration.utils.UIState.calibration.CalibrateTemp import CalibrateTemp
from titration.utils.UIState.calibration.SetupCalibration import SetupCalibration
from titration.utils.Titrator import Titrator
from titration.utils import LCD_interface, constants

# Test handleKey
@mock.patch.object(CalibrateTemp, "_setNextState")
def test_handleKey(setNextStateMock):
    calibrateTemp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrateTemp.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    assert calibrateTemp.subState == 2 

    calibrateTemp.handleKey("1")
    assert calibrateTemp.subState == 3

    calibrateTemp.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "SetupCalibration"


# Test loop
@mock.patch.object(LCD_interface, "lcd_out")
def test_loop(lcdOutMock):
    calibrateTemp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set Ref solution", line=1),
            mock.call("temp", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibrateTemp.subState += 1
    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Put probe in sol", line=1),
            mock.call("", line=2),
            mock.call("Press 1 to", line=3),
            mock.call("record value", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibrateTemp.subState += 1
    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Recorded temp:", line=1),
            mock.call("{0:0.3f}".format(calibrateTemp.values['actual_temperature']), line=2),
            mock.call("{}".format(calibrateTemp.values['new_ref_resistance']), line=3),
            mock.call("", line=4),
        ]
    )


# Test CalibrateTemp
@mock.patch.object(CalibrateTemp, "_setNextState")
@mock.patch.object(LCD_interface, "lcd_out")
def test_CalibrateTemp(lcdOutMock, setNextStateMock):
    calibrateTemp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set Ref solution", line=1),
            mock.call("temp", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibrateTemp.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "UserValue"
    assert calibrateTemp.subState == 2

    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Put probe in sol", line=1),
            mock.call("", line=2),
            mock.call("Press 1 to", line=3),
            mock.call("record value", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibrateTemp.handleKey("1")
    assert calibrateTemp.subState == 3

    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Recorded temp:", line=1),
            mock.call("{0:0.3f}".format(calibrateTemp.values['actual_temperature']), line=2),
            mock.call("{}".format(calibrateTemp.values['new_ref_resistance']), line=3),
            mock.call("", line=4),
        ]
    )

    calibrateTemp.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "SetupCalibration"
