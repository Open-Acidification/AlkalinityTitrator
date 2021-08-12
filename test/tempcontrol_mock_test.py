import time

import src.devices.board_mock as board
import src.devices.temp_probe_mock as temp_probe
import src.devices.tempcontrol_mock as tempcontrol


def test_tempcontrol_create():
    tempcontroller = tempcontrol.TempControl(board.D1, board.SCK, board.MOSI, board.MISO, board.D4, wires=3)

    assert tempcontroller is not None


def test_tempcontrol_update():
    tempcontroller = tempcontrol.TempControl(board.D1, board.SCK, board.MOSI, board.MISO, board.D4, wires=3)

    tempcontroller.update()
    time.sleep(1)
    tempcontroller.update()


def test_tempcontrol_enable_print():
    tempcontroller = tempcontrol.TempControl(board.D1, board.SCK, board.MOSI, board.MISO, board.D4, wires=3)

    tempcontroller.enable_print()


def test_tempcontrol_disable_print():
    tempcontroller = tempcontrol.TempControl(board.D1, board.SCK, board.MOSI, board.MISO, board.D4, wires=3)

    tempcontroller.disable_print()


def test_tempcontrol_at_temp():
    tempcontroller = tempcontrol.TempControl(board.D1, board.SCK, board.MOSI, board.MISO, board.D4, wires=3)

    tempcontroller.at_temp()


def test_tempcontrol_last_temp():
    tempcontroller = tempcontrol.TempControl(board.D1, board.SCK, board.MOSI, board.MISO, board.D4, wires=3)

    tempcontroller.get_last_temp()


def test_tempcontrol_activate():
    tempcontroller = tempcontrol.TempControl(board.D1, board.SCK, board.MOSI, board.MISO, board.D4, wires=3)

    tempcontroller.activate()


def test_tempcontrol_deactivate():
    tempcontroller = tempcontrol.TempControl(board.D1, board.SCK, board.MOSI, board.MISO, board.D4, wires=3)

    tempcontroller.deactivate()
