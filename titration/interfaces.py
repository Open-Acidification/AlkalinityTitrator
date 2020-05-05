"""Functions to interface with sensors and peripherals"""
import constants
import analysis
# for pH sensor
import adafruit_ads1x15.ads1015 as ads
import adafruit_ads1x15.analog_in as analog_in

# for max31865 temp sensor
import board
import busio
import digitalio
import adafruit_max31865

# for pump
import RPi.GPIO as GPIO
import time

# global
ph_input_channel = None
temp_sensor = None


def setup_interfaces():
    global ph_input_channel, temp_sensor
    # setup pH sensor
    #i2c = busio.I2C(board.SCL, board.SDA)
    #adc = ads.ADS1015(i2c, data_rate=920, gain=2)  # Todo: do we want a higher gain?
    #ph_input_channel = analog_in.AnalogIn(adc, ads.P0, ads.P1)
    
    print("Setting up...")
    # setup temperature sensor
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.D5)
    temp_sensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=constants.nominal_resistance, ref_resistor=constants.calibrated_ref_resistor_value)

    # setup pump
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(constants.PUMP_PIN_NUMBER, GPIO.OUT)


def lcd_out(info):
    """Outputs given string to LCD screen"""
    # TODO interface with LCD; for now, print to console
    print(info)


def display_list(list_to_display):
    """Display a list of options"""
    # NOTE this may need to be updated based on how the LCD actually displays
    # characters
    for key, value in list_to_display.items():
        lcd_out(str(key) + '. ' + value)


def read_user_input(valid_inputs=None):
    """Reads user input from keypad"""
    # TODO interface with keypad
    # TODO verify input through valid_inputs parameter?
    # Temporarily query user input from terminal
    while True:
        user_input = input()
        if valid_inputs is None or user_input in valid_inputs:
            break
        lcd_out(constants.VALID_INPUT_WARNING)
    return user_input


# def read_pH():
#     """Reads calibration-adjusted value for pH"""
#     volts = read_raw_pH()
#     temp = read_temperature()[0]
#     pH_val = analysis.calculate_pH(volts, temp)
#     return pH_val


def read_pH():
    """TEMP FUNCTION until I can test pH"""
    constants.pH_call_iter += 1
    return constants.test_pH_vals[constants.hcl_call_iter][constants.pH_call_iter]


def read_raw_pH():
    """Reads and returns the pH value from GPIO as volts"""
    # Read pH registers; pH_val is raw value from pH probe
    volts = ph_input_channel.voltage
    diff = volts / 9.7
    volts = volts / 10
    # percent_diff = (diff - volts)/volts*100
    return volts  # , percent_diff


def read_temperature():
    """Reads and returns the temperature from GPIO"""
    # print('Temperature: {0:0.3f}C'.format(sensor.temperature))
    # print('Resistance: {0:0.3f} Ohms'.format(sensor.resistance))
    return temp_sensor.temperature, temp_sensor.resistance


def dispense_HCl(volume):
    """Adds HCl to the solution"""
    # TODO stepper motor driver needed here; will likely connect to the Arduino
    # NOTE should this wait for pH to settle instead of read_pH?
    constants.hcl_call_iter += 1  # value only used for testing while reading pH doesn't work
    print("{} ml HCL added".format(volume))

    GPIO.output(constants.PUMP_PIN_NUMBER, GPIO.HIGH)
    time.sleep(constants.PUMP_PULSE_TIME)
    GPIO.output(constants.PUMP_PIN_NUMBER, GPIO.LOW)


GPIO.cleanup()  # use this instead
