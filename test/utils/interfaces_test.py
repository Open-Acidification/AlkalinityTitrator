"""
The file to test the lcd interface
"""
from titration.utils import constants, interfaces


def setup_module(module):
    constants.IS_TEST = True
    interfaces.setup_module_classes()
    interfaces.ui_lcd = interfaces.setup_lcd()
    interfaces.stir_controller = interfaces.setup_stir_control(debug=True)


def test_interfaces_lcd(capsys):
    # flush stdout
    _ = capsys.readouterr()

    interfaces.lcd_out("Test string", 1, constants.LCD_LEFT_JUST)

    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|Test string         |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "*====================*\n"
    )


def test_interfaces_stir_fast(capsys):
    _ = capsys.readouterr()

    interfaces.stir_speed_fast()

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

    interfaces.stir_stop()
    captured = capsys.readouterr()
    assert captured.out == ("Stirrer set to 0\n")


def test_interfaces_stir_slow(capsys):
    _ = capsys.readouterr()

    interfaces.stir_speed_slow()

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

    interfaces.stir_stop()
    captured = capsys.readouterr()
    assert captured.out == ("Stirrer set to 0\n")


def test_interfaces_stir_set(capsys):
    _ = capsys.readouterr()

    interfaces.stir_speed(5000, gradual=True)

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

    interfaces.stir_speed(8000, gradual=True)
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

    interfaces.stir_speed(3000, gradual=True)
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

    interfaces.stir_stop()
    captured = capsys.readouterr()
    assert captured.out == ("Stirrer set to 0\n")
