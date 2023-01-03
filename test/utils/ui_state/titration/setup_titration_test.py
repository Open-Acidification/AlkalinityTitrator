from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.titration.setup_titration import SetupTitration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface, constants


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    setupTitration = SetupTitration(Titrator())

    setupTitration.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    assert setupTitration.subState == 2
    updateStateMock.reset_called()

    setupTitration.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    assert setupTitration.subState == 3
    updateStateMock.reset_called()

    setupTitration.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "CalibratePh"
    updateStateMock.reset_called()

    setupTitration.handleKey("0")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "InitialTitration"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    setupTitration = SetupTitration(Titrator())

    setupTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Sol.", line=1),
            mock.call("weight (g)", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    setupTitration.subState += 1
    setupTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Sol.", line=1),
            mock.call("salinity (ppt)", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    setupTitration.subState += 1
    setupTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Calibrate pH probe?", line=1),
            mock.call("Yes: 1", line=2),
            mock.call("No (use old): 0", line=3),
            mock.call(
                "{0:>2.3f} pH: {1:>2.4f} V".format(
                    constants.PH_REF_PH, constants.PH_REF_VOLTAGE
                ),
                line=4,
            ),
        ]
    )


@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_SetupTitration(lcdOutMock, updateStateMock):
    setupTitration = SetupTitration(Titrator())

    setupTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Sol.", line=1),
            mock.call("weight (g)", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    setupTitration.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    assert setupTitration.subState == 2
    updateStateMock.reset_called()

    setupTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Enter Sol.", line=1),
            mock.call("salinity (ppt)", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    setupTitration.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    assert setupTitration.subState == 3
    updateStateMock.reset_called()

    setupTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Calibrate pH probe?", line=1),
            mock.call("Yes: 1", line=2),
            mock.call("No (use old): 0", line=3),
            mock.call(
                "{0:>2.3f} pH: {1:>2.4f} V".format(
                    constants.PH_REF_PH, constants.PH_REF_VOLTAGE
                ),
                line=4,
            ),
        ]
    )

    setupTitration.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "CalibratePh"