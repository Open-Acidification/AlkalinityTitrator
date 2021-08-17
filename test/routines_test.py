import io

from titration.utils import constants, interfaces, routines


def test_routines_requirements():
    constants.IS_TEST = True
    interfaces.setup_module_classes()
    interfaces.setup_interfaces()


def test_routines_test_mode_pump(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("0\n*\n5\nA\n0\nA\n"))
    routines.test_mode_pump()
    _ = capsys.readouterr()
    interfaces.lcd_out("", 1)
    captured = capsys.readouterr()
    assert captured.out == (
        "*====================*\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|                    |\n"
        + "|Pump Vol: 0.50 ml   |\n"
        + "*====================*\n"
    )
