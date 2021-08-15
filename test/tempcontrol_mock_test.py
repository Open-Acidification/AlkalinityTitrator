import time

import src.devices.board_mock as board
import src.devices.temperature_probe_mock as temperature_probe
import src.devices.temperaturecontrol_mock as temperaturecontrol


def test_temperaturecontrol_create():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperature_controller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    assert temperature_controller is not None


def test_temperaturecontrol_update():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperature_controller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperature_controller.update()
    time.sleep(1)
    temperature_controller.update()


def test_temperaturecontrol_enable_print():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperature_controller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperature_controller.enable_print()


def test_temperaturecontrol_disable_print():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperature_controller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperature_controller.disable_print()


def test_temperaturecontrol_at_temperature():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperature_controller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperature_controller.at_temperature()


def test_temperaturecontrol_last_temperature():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperature_controller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperature_controller.get_last_temperature()


def test_temperaturecontrol_activate():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperature_controller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperature_controller.activate()


def test_temperaturecontrol_deactivate():
    sensor = temperature_probe.Temperature_Probe(board.SCK, board.MOSI, board.MISO, board.D0, wires=3)
    temperature_controller = temperaturecontrol.TemperatureControl(board.D1, sensor)

    temperature_controller.deactivate()
