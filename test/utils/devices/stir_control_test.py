from titration.utils.devices.stir_control_mock import Stir_Control
from titration.utils.devices import board_mock as board_class

stir_controller = Stir_Control(board_class.D13, debug=True)


def test_stir_controller_stir_fast(capsys):
    _ = capsys.readouterr()

    stir_controller.motor_speed_fast()

    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to 1000\n"
        + "Stirrer set to 1100\n"
        + "Stirrer set to 1200\n"
        + "Stirrer set to 1300\n"
        + "Stirrer set to 1400\n"
        + "Stirrer set to 1500\n"
        + "Stirrer set to 1600\n"
        + "Stirrer set to 1700\n"
        + "Stirrer set to 1800\n"
        + "Stirrer set to 1900\n"
        + "Stirrer set to 2000\n"
        + "Stirrer set to 2100\n"
        + "Stirrer set to 2200\n"
        + "Stirrer set to 2300\n"
        + "Stirrer set to 2400\n"
        + "Stirrer set to 2500\n"
        + "Stirrer set to 2600\n"
        + "Stirrer set to 2700\n"
        + "Stirrer set to 2800\n"
        + "Stirrer set to 2900\n"
        + "Stirrer set to 3000\n"
        + "Stirrer set to 3100\n"
        + "Stirrer set to 3200\n"
        + "Stirrer set to 3300\n"
        + "Stirrer set to 3400\n"
        + "Stirrer set to 3500\n"
        + "Stirrer set to 3600\n"
        + "Stirrer set to 3700\n"
        + "Stirrer set to 3800\n"
        + "Stirrer set to 3900\n"
        + "Stirrer set to 4000\n"
        + "Stirrer set to 4100\n"
        + "Stirrer set to 4200\n"
        + "Stirrer set to 4300\n"
        + "Stirrer set to 4400\n"
        + "Stirrer set to 4500\n"
        + "Stirrer set to 4600\n"
        + "Stirrer set to 4700\n"
        + "Stirrer set to 4800\n"
        + "Stirrer set to 4900\n"
        + "Stirrer set to 5000\n"
    )

    stir_controller.motor_stop()
    captured = capsys.readouterr()
    assert captured.out == ("Stirrer set to 0\n")


def test_stir_controller_stir_slow(capsys):
    _ = capsys.readouterr()

    stir_controller.motor_speed_slow()

    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to 1000\n"
        + "Stirrer set to 1100\n"
        + "Stirrer set to 1200\n"
        + "Stirrer set to 1300\n"
        + "Stirrer set to 1400\n"
        + "Stirrer set to 1500\n"
        + "Stirrer set to 1600\n"
        + "Stirrer set to 1700\n"
        + "Stirrer set to 1800\n"
        + "Stirrer set to 1900\n"
        + "Stirrer set to 2000\n"
        + "Stirrer set to 2100\n"
        + "Stirrer set to 2200\n"
        + "Stirrer set to 2300\n"
        + "Stirrer set to 2400\n"
        + "Stirrer set to 2500\n"
        + "Stirrer set to 2600\n"
        + "Stirrer set to 2700\n"
        + "Stirrer set to 2800\n"
        + "Stirrer set to 2900\n"
        + "Stirrer set to 3000\n"
    )

    stir_controller.motor_stop()
    captured = capsys.readouterr()
    assert captured.out == ("Stirrer set to 0\n")


def test_stir_controller_stir_set(capsys):
    _ = capsys.readouterr()

    stir_controller.set_motor_speed(5000, gradual=True)

    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to 1000\n"
        + "Stirrer set to 1100\n"
        + "Stirrer set to 1200\n"
        + "Stirrer set to 1300\n"
        + "Stirrer set to 1400\n"
        + "Stirrer set to 1500\n"
        + "Stirrer set to 1600\n"
        + "Stirrer set to 1700\n"
        + "Stirrer set to 1800\n"
        + "Stirrer set to 1900\n"
        + "Stirrer set to 2000\n"
        + "Stirrer set to 2100\n"
        + "Stirrer set to 2200\n"
        + "Stirrer set to 2300\n"
        + "Stirrer set to 2400\n"
        + "Stirrer set to 2500\n"
        + "Stirrer set to 2600\n"
        + "Stirrer set to 2700\n"
        + "Stirrer set to 2800\n"
        + "Stirrer set to 2900\n"
        + "Stirrer set to 3000\n"
        + "Stirrer set to 3100\n"
        + "Stirrer set to 3200\n"
        + "Stirrer set to 3300\n"
        + "Stirrer set to 3400\n"
        + "Stirrer set to 3500\n"
        + "Stirrer set to 3600\n"
        + "Stirrer set to 3700\n"
        + "Stirrer set to 3800\n"
        + "Stirrer set to 3900\n"
        + "Stirrer set to 4000\n"
        + "Stirrer set to 4100\n"
        + "Stirrer set to 4200\n"
        + "Stirrer set to 4300\n"
        + "Stirrer set to 4400\n"
        + "Stirrer set to 4500\n"
        + "Stirrer set to 4600\n"
        + "Stirrer set to 4700\n"
        + "Stirrer set to 4800\n"
        + "Stirrer set to 4900\n"
        + "Stirrer set to 5000\n"
    )

    stir_controller.set_motor_speed(8000, gradual=True)
    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to 5100\n"
        + "Stirrer set to 5200\n"
        + "Stirrer set to 5300\n"
        + "Stirrer set to 5400\n"
        + "Stirrer set to 5500\n"
        + "Stirrer set to 5600\n"
        + "Stirrer set to 5700\n"
        + "Stirrer set to 5800\n"
        + "Stirrer set to 5900\n"
        + "Stirrer set to 6000\n"
        + "Stirrer set to 6100\n"
        + "Stirrer set to 6200\n"
        + "Stirrer set to 6300\n"
        + "Stirrer set to 6400\n"
        + "Stirrer set to 6500\n"
        + "Stirrer set to 6600\n"
        + "Stirrer set to 6700\n"
        + "Stirrer set to 6800\n"
        + "Stirrer set to 6900\n"
        + "Stirrer set to 7000\n"
        + "Stirrer set to 7100\n"
        + "Stirrer set to 7200\n"
        + "Stirrer set to 7300\n"
        + "Stirrer set to 7400\n"
        + "Stirrer set to 7500\n"
        + "Stirrer set to 7600\n"
        + "Stirrer set to 7700\n"
        + "Stirrer set to 7800\n"
        + "Stirrer set to 7900\n"
        + "Stirrer set to 8000\n"
    )

    stir_controller.set_motor_speed(3000, gradual=True)
    captured = capsys.readouterr()
    assert captured.out == (
        "Stirrer set to 7900\n"
        + "Stirrer set to 7800\n"
        + "Stirrer set to 7700\n"
        + "Stirrer set to 7600\n"
        + "Stirrer set to 7500\n"
        + "Stirrer set to 7400\n"
        + "Stirrer set to 7300\n"
        + "Stirrer set to 7200\n"
        + "Stirrer set to 7100\n"
        + "Stirrer set to 7000\n"
        + "Stirrer set to 6900\n"
        + "Stirrer set to 6800\n"
        + "Stirrer set to 6700\n"
        + "Stirrer set to 6600\n"
        + "Stirrer set to 6500\n"
        + "Stirrer set to 6400\n"
        + "Stirrer set to 6300\n"
        + "Stirrer set to 6200\n"
        + "Stirrer set to 6100\n"
        + "Stirrer set to 6000\n"
        + "Stirrer set to 5900\n"
        + "Stirrer set to 5800\n"
        + "Stirrer set to 5700\n"
        + "Stirrer set to 5600\n"
        + "Stirrer set to 5500\n"
        + "Stirrer set to 5400\n"
        + "Stirrer set to 5300\n"
        + "Stirrer set to 5200\n"
        + "Stirrer set to 5100\n"
        + "Stirrer set to 5000\n"
        + "Stirrer set to 4900\n"
        + "Stirrer set to 4800\n"
        + "Stirrer set to 4700\n"
        + "Stirrer set to 4600\n"
        + "Stirrer set to 4500\n"
        + "Stirrer set to 4400\n"
        + "Stirrer set to 4300\n"
        + "Stirrer set to 4200\n"
        + "Stirrer set to 4100\n"
        + "Stirrer set to 4000\n"
        + "Stirrer set to 3900\n"
        + "Stirrer set to 3800\n"
        + "Stirrer set to 3700\n"
        + "Stirrer set to 3600\n"
        + "Stirrer set to 3500\n"
        + "Stirrer set to 3400\n"
        + "Stirrer set to 3300\n"
        + "Stirrer set to 3200\n"
        + "Stirrer set to 3100\n"
        + "Stirrer set to 3000\n"
    )

    stir_controller.motor_stop()
    captured = capsys.readouterr()
    assert captured.out == ("Stirrer set to 0\n")
