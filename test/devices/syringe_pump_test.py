"""
The file to test the syringe pump
"""

# pylint: disable = protected-access

from unittest import mock
from unittest.mock import call

from titration.devices.library import Serial, SyringePump


def test_init():
    """
    The function to test creating syringe
    """
    pump = SyringePump()

    assert pump._pump_volume == 0
    assert pump._serial is not None
    assert pump is not None


def test_get_pump_volume():
    """
    The function to test getting the syringe volume
    """
    pump = SyringePump()

    pump._pump_volume = 0.5

    assert pump.get_pump_volume() == 0.5


def test_get_added_volume():
    """
    The function to test getting the amount of added solution
    """
    pump = SyringePump()

    pump._added_volume = 0.5

    assert pump.get_added_volume() == 0.5


def test_clear_added_volume():
    """
    The function to test clearing the added amount of volume
    """
    pump = SyringePump()

    pump._added_volume = 0.5

    pump.clear_added_volume()
    assert pump._added_volume == 0


@mock.patch.object(SyringePump, "_drive_step_stick")
def test_fill_completely_empty(_drive_step_stick):
    """
    The function to test filling the pump
    """
    pump = SyringePump()

    pump.fill()
    assert pump._pump_volume == 1.1
    _drive_step_stick.assert_called_with(10505, 0)

    pump._pump_volume = 0.5

    pump.fill()
    assert pump._pump_volume == 1.1
    _drive_step_stick.assert_called_with(5730, 0)


@mock.patch.object(SyringePump, "_drive_step_stick")
def test_fill_partially_empty(_drive_step_stick):
    """
    The function to test filling the pump
    """
    pump = SyringePump()

    pump._pump_volume = 0.5

    pump.fill()
    assert pump._pump_volume == 1.1
    _drive_step_stick.assert_called_with(5730, 0)


@mock.patch.object(SyringePump, "_drive_step_stick")
def test_fill_already_full(_drive_step_stick):
    """
    The function to test filling the pump
    """
    pump = SyringePump()

    pump._pump_volume = 1.1

    pump.fill()
    assert pump._pump_volume == 1.1
    _drive_step_stick.assert_called_with(0, 0)


@mock.patch.object(SyringePump, "_drive_step_stick", return_value=0)
def test_empty_full(_drive_step_stick):
    """
    The function to test emptying the pump
    """
    pump = SyringePump()

    pump._added_volume = 0.5
    pump._pump_volume = 1.1

    pump.empty()
    assert pump._pump_volume == 0
    assert pump._added_volume == 0.5
    _drive_step_stick.assert_called_with(10505, 1)


@mock.patch.object(SyringePump, "_drive_step_stick", return_value=0)
def test_empty_partially_full(_drive_step_stick):
    """
    The function to test emptying the pump
    """
    pump = SyringePump()

    pump._added_volume = 0.5
    pump._pump_volume = 0.5

    pump.empty()
    assert pump._pump_volume == 0
    assert pump._added_volume == 0.5
    _drive_step_stick.assert_called_with(4775, 1)


@mock.patch.object(SyringePump, "_drive_step_stick", return_value=0)
def test_empty_already_empty(_drive_step_stick):
    """
    The function to test emptying the pump
    """
    pump = SyringePump()

    pump._added_volume = 0.5
    pump._pump_volume = 0

    pump.empty()
    assert pump._pump_volume == 0
    assert pump._added_volume == 0.5
    _drive_step_stick.assert_called_with(0, 1)


@mock.patch.object(SyringePump, "_drive_step_stick")
def test_pump_in(_drive_step_stick):
    """
    The function to test pulling liquid into the syringe
    """
    pump = SyringePump()

    pump.pump_in(0.5)
    assert pump._pump_volume == 0.5
    assert pump._added_volume == 0
    _drive_step_stick.assert_called_with(4775, 0)


@mock.patch.object(SyringePump, "_drive_step_stick")
def test_pump_in_above_max(_drive_step_stick):
    """
    The function to test pulling more liquid than the syringe can hold
    """
    pump = SyringePump()

    pump.pump_in(1.5)
    assert pump._pump_volume == 1.1
    assert pump._added_volume == 0
    _drive_step_stick.assert_called_with(10505, 0)


@mock.patch.object(SyringePump, "_drive_step_stick", return_value=0)
def test_pump_out(_drive_step_stick):
    """
    The function to test pumping a volume out of the syringe
    """
    pump = SyringePump()

    pump._pump_volume = 0.5

    pump.pump_out(0.5)
    assert pump._pump_volume == 0
    assert pump._added_volume == 0.5
    _drive_step_stick.assert_called_with(4775, 1)


@mock.patch.object(SyringePump, "_drive_step_stick", return_value=0)
def test_pump_out_above_max_capacity(_drive_step_stick):
    """
    The function to test pumping more than the max amount of volume the pump can hold
    """
    pump = SyringePump()

    pump._pump_volume = 1.1

    pump.pump_out(1.3)
    assert pump._pump_volume == 0
    assert pump._added_volume == 1.3
    calls = [
        call(10505, 1),
        call(1909, 0),
        call(1909, 1),
    ]
    _drive_step_stick.assert_has_calls(calls)


@mock.patch.object(SyringePump, "_drive_step_stick", return_value=0)
def test_pump_out_above_syringe_volume(_drive_step_stick):
    """
    The function to test when pumping out more volume than what is currently in the syringe
    """
    pump = SyringePump()

    pump._pump_volume = 0.5

    pump.pump_out(0.75)
    assert pump._pump_volume == 0
    assert pump._added_volume == 0.75
    calls = [call(4775, 1), call(2387, 0), call(2387, 1)]
    _drive_step_stick.assert_has_calls(calls)


@mock.patch.object(SyringePump, "_drive_step_stick")
def test_drive_pump_in(_drive_step_stick):
    """
    The function to test the _drive_pump_in function
    """
    pump = SyringePump()

    pump._drive_pump_in(0.5)
    assert pump._pump_volume == 0.5
    assert pump._added_volume == 0
    _drive_step_stick.assert_called_with(4775, 0)


@mock.patch.object(SyringePump, "_drive_step_stick", return_value=0)
def test_drive_pump_out(_drive_step_stick):
    """
    The function to test _drive_pump_out function
    """
    pump = SyringePump()

    pump._pump_volume = 0.5
    pump._added_volume = 0.3

    pump._drive_pump_out(0.2)
    assert pump._pump_volume == 0.3
    assert pump._added_volume == 0.5
    _drive_step_stick.assert_called_with(1910, 1)


@mock.patch.object(Serial, "write")
@mock.patch.object(Serial, "flush")
@mock.patch.object(Serial, "readline", return_value=b"DONE\r\n")
def test_drive_step_stick_in(write, flush, readline):
    """
    The function to test the _drive_step_stick pumping in function
    """
    pump = SyringePump()

    assert pump._drive_step_stick(500, 0) == 0
    write.assert_called()
    flush.assert_called()
    readline.assert_called()


@mock.patch.object(Serial, "write")
@mock.patch.object(Serial, "flush")
@mock.patch.object(Serial, "readline", return_value=b"DONE\r\n")
def test_drive_step_stick_out(write, flush, readline):
    """
    The function to test the _drive_step_stick pumping in function
    """
    pump = SyringePump()

    assert pump._drive_step_stick(500, 1) == 0
    write.assert_called()
    flush.assert_called()
    readline.assert_called()


@mock.patch.object(Serial, "writable")
@mock.patch.object(Serial, "write")
@mock.patch.object(Serial, "flush")
@mock.patch.object(Serial, "readline")
def test_drive_step_stick_in_zero(writable, write, flush, readline):
    """
    The function to test the _drive_step_stick pumping in function with zero cycles
    """
    pump = SyringePump()

    assert pump._drive_step_stick(0, 1) == 0
    writable.assert_not_called()
    write.assert_not_called()
    flush.assert_not_called()
    readline.assert_not_called()


@mock.patch.object(Serial, "writable")
@mock.patch.object(Serial, "write")
@mock.patch.object(Serial, "flush")
@mock.patch.object(Serial, "readline")
def test_drive_step_stick_out_zero(writable, write, flush, readline):
    """
    The function to test the _drive_step_stick pumping out function with zero cycles
    """
    pump = SyringePump()

    assert pump._drive_step_stick(0, 0) == 0
    writable.assert_not_called()
    write.assert_not_called()
    flush.assert_not_called()
    readline.assert_not_called()
