import time

import src.devices.board_mock as board
import src.devices.temp_probe_mock as temp_probe
import src.devices.tempcontrol_mock as tempcontrol


def test_tempcontrol_create():
    sensor = temp_probe.Temp_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    tempcontroller = tempcontrol.TempControl(board.D1, sensor)

    assert tempcontroller is not None


def test_tempcontrol_update():
    sensor = temp_probe.Temp_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    tempcontroller = tempcontrol.TempControl(board.D1, sensor)

    tempcontroller.update()
    time.sleep(1)
    tempcontroller.update()


def test_tempcontrol_enable_print():
    sensor = temp_probe.Temp_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    tempcontroller = tempcontrol.TempControl(board.D1, sensor)

    tempcontroller.enable_print()


def test_tempcontrol_disable_print():
    sensor = temp_probe.Temp_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    tempcontroller = tempcontrol.TempControl(board.D1, sensor)

    tempcontroller.disable_print()


def test_tempcontrol_at_temp():
    sensor = temp_probe.Temp_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    tempcontroller = tempcontrol.TempControl(board.D1, sensor)

    tempcontroller.at_temp()


def test_tempcontrol_last_temp():
    sensor = temp_probe.Temp_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    tempcontroller = tempcontrol.TempControl(board.D1, sensor)

    tempcontroller.get_last_temp()


def test_tempcontrol_activate():
    sensor = temp_probe.Temp_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    tempcontroller = tempcontrol.TempControl(board.D1, sensor)

    tempcontroller.activate()


def test_tempcontrol_deactivate():
    sensor = temp_probe.Temp_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    tempcontroller = tempcontrol.TempControl(board.D1, sensor)

    tempcontroller.deactivate()
