import titration.utils.constants as c
import titration.utils.devices.serial_mock as serial


def test_serial_create():
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    assert arduino is not None


def test_serial_output_buffer():
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    arduino.reset_output_buffer()


def test_serial_input_buffer():
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    arduino.reset_input_buffer()


def test_serial_writable():
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    assert arduino.writable()


def test_serial_write(capsys):
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    arduino.write("test string")

    # diabled due to printing on syringe_pump calls
    # captured = capsys.readouterr()
    # assert captured.out == "test string\n"


def test_serial_flush():
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    arduino.flush()


def test_serial_readline():
    arduino = serial.Serial(
        port=c.ARDUINO_PORT, baudrate=c.ARDUINO_BAUD, timeout=c.ARDUINO_TIMEOUT
    )
    assert arduino.readline() == b"DONE\r\n"
