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

# keep track of solution in pump
# volume_in_pump = 0


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
    cs = digitalio.DigitalInOut(board.D6)
    temp_sensor = adafruit_max31865.MAX31865(spi=spi,
                                             cs=cs,
                                             wires=3,
                                             rtd_nominal=constants.TEMP_NOMINAL_RESISTANCE,
                                             ref_resistor=constants.TEMP_REF_RESISTANCE)

    # pump setup (through Arduino)
    if not constants.IS_TEST:
        arduino = serial.Serial(port=constants.ARDUINO_PORT,
                                baudrate=constants.ARDUINO_BAUD,
                                timeout=constants.ARDUINO_TIMEOUT)
        arduino.reset_output_buffer()
        arduino.reset_input_buffer()


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
    :returns: adjusted pH value in units of pH, raw V reading from probe
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
    Reads and pH value pH probe in V
    :return: raw V reading from probe
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
    if constants.IS_TEST:
        return _test_read_temperature()
    return temp_sensor.temperature, temp_sensor.resistance


def _test_read_temperature():
    return 29.9, 200


def pump_volume(volume, direction):
    """
    Moves volume of solution through pump
    :param volume: amount of volume to move (float)
    :param direction: 0 to pull solution in, 1 to pump out
    """
    volume_to_add = volume

    # pull in solution
    if direction == 0:
        # if volume_to_add is greater than space in the pump
        space_in_pump = constants.MAX_PUMP_CAPACITY - constants.volume_in_pump
        if volume_to_add > space_in_pump:
            volume_to_add = constants.MAX_PUMP_CAPACITY - constants.volume_in_pump
        drive_pump(volume_to_add, direction)

    # pump out solution
    elif direction == 1:
        if volume_to_add > constants.MAX_PUMP_CAPACITY:
            lcd_out("Volume greater than pumpable")
            # volume greater than max capacity of pump

            # add all current volume in pump
            next_volume = constants.volume_in_pump
            drive_pump(next_volume, 1)

            # recalculate volume to add
            volume_to_add = volume_to_add - next_volume

            while volume_to_add > 0:
                # pump in and out more solution
                next_volume = min(volume_to_add, constants.MAX_PUMP_CAPACITY)
                drive_pump(next_volume, 0)
                drive_pump(next_volume, 1)
                volume_to_add -= next_volume

        elif volume_to_add > constants.volume_in_pump:
            # volume greater than volume in pump
            next_volume = constants.volume_in_pump
            drive_pump(next_volume, 1)

            # calculate rest of volume to add
            volume_to_add -= next_volume

            drive_pump(volume_to_add, 0)
            drive_pump(volume_to_add, 1)

        else:
            # volume less than volume in pump
            drive_pump(volume_to_add, direction)


def _test_add_HCl():
    constants.hcl_call_iter += 1  # value only used for testing while reading pH doesn't work
    constants.pH_call_iter = -1


def drive_pump(volume, direction):
    """Converts volume to cycles and ensures and checks pump level and values"""
    if direction == 0:
        space_in_pump = constants.MAX_PUMP_CAPACITY - constants.volume_in_pump
        if volume > space_in_pump:
            lcd_out("Error taking in titrant")
        else:
            lcd_out("Taking in {} ml titrant".format(volume))
            cycles = analysis.determine_pump_cycles(volume)
            drive_step_stick(cycles, direction)
            constants.volume_in_pump += volume
    elif direction == 1:
        if volume > constants.volume_in_pump:
            lcd_out("Error pumping out titrant")
        else:
            lcd_out("Pumping out {} ml titrant".format(volume))
            cycles = analysis.determine_pump_cycles(volume)
            drive_step_stick(cycles, direction)
            constants.volume_in_pump -= volume

    lcd_out("Volume in pump: {}".format(constants.volume_in_pump))


def drive_step_stick(cycles, direction):
    """
    Communicates with arduino to add HCl through pump
    :param cycles: number of rising edges for the pump
    :param direction: direction of pump
    """
    if constants.IS_TEST:
        time.sleep(1)
        return _test_add_HCl()

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
    """Variable pump priming"""
    setup_interfaces()
    analysis.setup_calibration()
    while True:
        lcd_out("Volume: ")
        p_volume = read_user_input()
        lcd_out("Direction: ")
        p_direction = read_user_input()
        if p_direction == '0' or p_direction == '1':
            pump_volume(float(p_volume), int(p_direction))
