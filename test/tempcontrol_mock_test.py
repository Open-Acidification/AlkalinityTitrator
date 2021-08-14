import time

import src.devices.board_mock as board
import src.devices.temperature_probe_mock as temperature_probe
import src.devices.temperaturecontrol_mock as temperaturecontrol


def test_temperaturecontrol_create():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperaturecontroller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    assert temperaturecontroller is not None


def test_temperaturecontrol_update():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperaturecontroller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperaturecontroller.update()
    time.sleep(1)
    temperaturecontroller.update()


def test_temperaturecontrol_enable_print():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperaturecontroller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperaturecontroller.enable_print()


def test_temperaturecontrol_disable_print():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperaturecontroller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperaturecontroller.disable_print()


def test_temperaturecontrol_at_temperature():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperaturecontroller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperaturecontroller.at_temperature()


def test_temperaturecontrol_last_temperature():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperaturecontroller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperaturecontroller.get_last_temperature()


def test_temperaturecontrol_activate():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperaturecontroller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperaturecontroller.activate()


def test_temperaturecontrol_deactivate():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperaturecontroller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperaturecontroller.deactivate()
