import time

import titration.utils.devices.board_mock as board
import titration.utils.devices.temperature_control_mock as temperature_control
import titration.utils.devices.temperature_probe_mock as temperature_probe


def test_temperature_control_create():
    sensor = temperature_probe.Temperature_Probe(
        board.SCK, board.MOSI, board.MISO, board.D0, wires=3
    )
    temperature_controller = temperature_control.TemperatureControl(sensor)

    assert temperature_controller is not None


def test_temperature_control_update():
    sensor = temperature_probe.Temperature_Probe(
        board.SCK, board.MOSI, board.MISO, board.D0, wires=3
    )
    temperature_controller = temperature_control.TemperatureControl(sensor)

    temperature_controller.update()
    time.sleep(1)
    temperature_controller.update()


def test_temperature_control_enable_print():
    sensor = temperature_probe.Temperature_Probe(
        board.SCK, board.MOSI, board.MISO, board.D0, wires=3
    )
    temperature_controller = temperature_control.TemperatureControl(sensor)

    temperature_controller.enable_print()


def test_temperature_control_disable_print():
    sensor = temperature_probe.Temperature_Probe(
        board.SCK, board.MOSI, board.MISO, board.D0, wires=3
    )
    temperature_controller = temperature_control.TemperatureControl(sensor)

    temperature_controller.disable_print()


def test_temperature_control_at_temperature():
    sensor = temperature_probe.Temperature_Probe(
        board.SCK, board.MOSI, board.MISO, board.D0, wires=3
    )
    temperature_controller = temperature_control.TemperatureControl(sensor)

    temperature_controller.at_temperature()


def test_temperature_control_last_temperature():
    sensor = temperature_probe.Temperature_Probe(
        board.SCK, board.MOSI, board.MISO, board.D0, wires=3
    )
    temperature_controller = temperature_control.TemperatureControl(sensor)

    temperature_controller.get_last_temperature()


def test_temperature_control_activate():
    sensor = temperature_probe.Temperature_Probe(
        board.SCK, board.MOSI, board.MISO, board.D0, wires=3
    )
    temperature_controller = temperature_control.TemperatureControl(sensor)

    temperature_controller.activate()


def test_temperature_control_deactivate():
    sensor = temperature_probe.Temperature_Probe(
        board.SCK, board.MOSI, board.MISO, board.D0, wires=3
    )
    temperature_controller = temperature_control.TemperatureControl(sensor)

    temperature_controller.deactivate()
