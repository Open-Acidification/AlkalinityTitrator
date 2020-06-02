"""Functions to interface with sensors and peripherals"""
import constants
import analysis

# for pH sensor
import adafruit_ads1x15.ads1115 as ADS
import adafruit_ads1x15.analog_in as analog_in

# for max31865 temp sensor
import board
import busio
import digitalio
import adafruit_max31865

# for pump
import time
import serial

# global, pH and temperature probes
ph_input_channel = None
temp_sensor = None
arduino = None


def setup_interfaces():
    """Initializes components for interfacing with pH probe, temperature probe, and stepper motor/syringe pump"""
    global ph_input_channel, temp_sensor, arduino
    # pH probe setup
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        ph_input_channel = analog_in.AnalogIn(ads, ADS.P0, ADS.P1)
        ads.gain = 2
        constants.IS_TEST = False
    except ValueError:
        lcd_out("Error initializing pH probe; will use test functions instead.")
        constants.IS_TEST = True

    # temperature probe setup
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.D5)
    temp_sensor = adafruit_max31865.MAX31865(spi=spi,
                                             cs=cs,
                                             wires=3,
                                             rtd_nominal=constants.TEMP_NOMINAL_RESISTANCE,
                                             ref_resistor=constants.TEMP_REF_RESISTANCE)

    # pump setup (through Arduino)
    try:
        arduino = serial.Serial(port=constants.ARDUINO_PORT,
                                baudrate=constants.ARDUINO_BAUD,
                                timeout=constants.ARDUINO_TIMEOUT)
        arduino.reset_output_buffer()
        arduino.reset_input_buffer()
    except FileNotFoundError:
        lcd_out("Port file not found")


def lcd_out(info):
    """
    Outputs given string to LCD screen
    :param info: string to be displayed on LCD screen
    """
    # TODO output to actual LCD screen
    print(info)


def display_list(list_to_display):
    """
    Display a list of options
    :param list_to_display: list to be displayed on LCD screen
    """
    for key, value in list_to_display.items():
        lcd_out(str(key) + '. ' + value)


def read_user_input(valid_inputs=None):
    """
    Reads user input from keypad
    :param valid_inputs: optional, valid inputs from the user
    :return: user input selection
    """
    # TODO interface with keypad
    # Temporarily query user input from terminal
    while True:
        user_input = input()
        if valid_inputs is None or user_input in valid_inputs:
            break
        lcd_out(constants.VALID_INPUT_WARNING)
    return user_input


def read_pH():
    """
    Reads calibration-adjusted value for pH
    :returns: adjusted pH value in units of pH, raw mV reading from probe
    """
    if constants.IS_TEST:
        return _test_read_pH()
    volts = read_raw_pH()
    temp = read_temperature()[0]
    pH_val = analysis.calculate_pH(volts, temp)
    return pH_val, volts


def _test_read_pH():
    """Test function for pH"""
    constants.pH_call_iter += 1
    return constants.test_pH_vals[constants.hcl_call_iter][constants.pH_call_iter], 1


def read_raw_pH():
    """
    Reads and pH value pH probe in mV
    :return: raw mV reading from probe
    """
    # Read pH registers; pH_val is raw value from pH probe
    volts = ph_input_channel.voltage
    diff = volts / 9.7
    volts = volts / 10
    return volts


def read_temperature():
    """
    Reads and returns the temperature from GPIO
    :returns: temperature in celsius, resistance in ohms
    """
    return temp_sensor.temperature, temp_sensor.resistance


def dispense_HCl(volume):
    """
    Adds HCl to the solution
    :param volume: volume of HCl to add
    """
    lcd_out("{} ml HCl added".format(volume))
    cycles = constants.NUM_CYCLES[volume]
    _drive_step_stick(cycles, 1)


def _drive_step_stick(cycles, direction):
    """
    Communicates with arduino to add HCl through pump
    :param cycles: number of rising edges for the pump
    :param direction: direction of pump
    """
    time.sleep(.01)
    if arduino.writable():
        arduino.write(cycles.to_bytes(4, 'little'))
        arduino.write(direction.to_bytes(1, 'little'))
        arduino.flush()
        wait_time = cycles/1000 + .5
        time.sleep(wait_time)
        temp = arduino.readline()
        if temp != b'DONE\r\n':
            lcd_out("Error writing to Arduino")
            print(temp)
    else:
        lcd_out("Arduino not available.")


if __name__ == "__main__":
    setup_interfaces()
    start = time.time()
    dispense_HCl(0.05)
    end = time.time()
    print("Time: ", end - start)
