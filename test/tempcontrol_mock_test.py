import time

import src.devices.board_mock as board
import src.devices.temp_probe_mock as temp_probe
import src.devices.tempcontrol_mock as tempcontrol


def test_tempcontrol_create():
    temp_sensor = temp_probe.Temp_Probe(
        board.SCK, board.MOSI, board.MISO, board.D4, wires=3
    )
    tempcontroller = tempcontrol.TempControl(temp_sensor, board.D1)

    assert tempcontroller is not None


def test_tempcontrol_update():
    temp_sensor = temp_probe.Temp_Probe(
        board.SCK, board.MOSI, board.MISO, board.D4, wires=3
    )
    tempcontroller = tempcontrol.TempControl(temp_sensor, board.D1)

    tempcontroller.update()
    time.sleep(1)
    tempcontroller.update()


def test_tempcontrol_enable_print():
    temp_sensor = temp_probe.Temp_Probe(
        board.SCK, board.MOSI, board.MISO, board.D4, wires=3
    )
    tempcontroller = tempcontrol.TempControl(temp_sensor, board.D1)

    tempcontroller.enable_print()


def test_tempcontrol_disable_print():
    temp_sensor = temp_probe.Temp_Probe(
        board.SCK, board.MOSI, board.MISO, board.D4, wires=3
    )
    tempcontroller = tempcontrol.TempControl(temp_sensor, board.D1)

    tempcontroller.disable_print()


def test_tempcontrol_at_temp():
    temp_sensor = temp_probe.Temp_Probe(
        board.SCK, board.MOSI, board.MISO, board.D4, wires=3
    )
    tempcontroller = tempcontrol.TempControl(temp_sensor, board.D1)

    tempcontroller.at_temp()


def test_tempcontrol_last_temp():
    temp_sensor = temp_probe.Temp_Probe(
        board.SCK, board.MOSI, board.MISO, board.D4, wires=3
    )
    tempcontroller = tempcontrol.TempControl(temp_sensor, board.D1)

    tempcontroller.get_last_temp()


def test_tempcontrol_activate():
    temp_sensor = temp_probe.Temp_Probe(
        board.SCK, board.MOSI, board.MISO, board.D4, wires=3
    )
    tempcontroller = tempcontrol.TempControl(temp_sensor, board.D1)

    tempcontroller.activate()


def test_tempcontrol_deactivate():
    temp_sensor = temp_probe.Temp_Probe(
        board.SCK, board.MOSI, board.MISO, board.D4, wires=3
    )
    tempcontroller = tempcontrol.TempControl(temp_sensor, board.D1)

    tempcontroller.deactivate()
