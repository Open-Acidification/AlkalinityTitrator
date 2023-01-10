from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.test_mode.test_mode import TestMode
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, interfaces
from titration.utils.ui_state.test_mode.read_values import ReadValues


# Test handleKey
@mock.patch.object(ReadValues, "_setNextState")
def test_handleKey(setNextStateMock):
    readValues = ReadValues(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    readValues.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
@mock.patch.object(interfaces, "delay")
def test_loop(delayMock, lcdOutMock):
    readValues = ReadValues(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    readValues.loop()
    assert delayMock.called_with(readValues.values["timeStep"])
    for i in range(readValues.values["numVals"]):
        lcdOutMock.assert_has_calls(
            [
                mock.call(
                    "Temp: {0:>4.3f} C".format(readValues.values["temp"]), line=1
                ),
                mock.call(
                    "Res:  {0:>4.3f} Ohms".format(readValues.values["res"]), line=2
                ),
                mock.call(
                    "pH:   {0:>4.5f} pH".format(readValues.values["pH_reading"]), line=3
                ),
                mock.call(
                    "pH V: {0:>3.4f} mV".format(readValues.values["pH_volts"] * 1000),
                    line=4,
                ),
                mock.call("Reading: {}".format(i), 1, console=True),
            ]
        )
    lcdOutMock.reset_called()

    lcdOutMock.assert_has_calls(
        [
            mock.call("Press any to cont", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )


# Test ReadValues
@mock.patch.object(ReadValues, "_setNextState")
@mock.patch.object(lcd_interface, "lcd_out")
@mock.patch.object(interfaces, "delay")
def test_ReadValues(delayMock, lcdOutMock, setNextStateMock):
    readValues = ReadValues(Titrator(), TestMode(Titrator(), MainMenu(Titrator())))

    readValues.loop()
    assert delayMock.called_with(readValues.values["timeStep"])
    for i in range(readValues.values["numVals"]):
        lcdOutMock.assert_has_calls(
            [
                mock.call(
                    "Temp: {0:>4.3f} C".format(readValues.values["temp"]), line=1
                ),
                mock.call(
                    "Res:  {0:>4.3f} Ohms".format(readValues.values["res"]), line=2
                ),
                mock.call(
                    "pH:   {0:>4.5f} pH".format(readValues.values["pH_reading"]), line=3
                ),
                mock.call(
                    "pH V: {0:>3.4f} mV".format(readValues.values["pH_volts"] * 1000),
                    line=4,
                ),
                mock.call("Reading: {}".format(i), 1, console=True),
            ]
        )
    lcdOutMock.reset_called()

    lcdOutMock.assert_has_calls(
        [
            mock.call("Press any to cont", line=1),
            mock.call("", line=2),
            mock.call("", line=3),
            mock.call("", line=4),
        ]
    )

    readValues.handleKey("1")
    setNextStateMock.assert_called_with(ANY, True)
    assert setNextStateMock.call_args.args[0].name() == "TestMode"
