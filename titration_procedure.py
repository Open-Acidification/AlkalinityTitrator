'''Alkalinity titration procedure 
Author: Kaden Sukachevin

Walla Walla University 
'''
# Libraries
from time import sleep
from datetime import datetime

# for pH sensor
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# for max31865 temp sensor
import board 
import busio
import digitalio
import adafruit_max31865

# CONSTANTS
PH_ACCURACY = 0.01          # Needed accuracy for final pH level after titration
TARGET_PH = 3.0             # Target pH value for titration process
TARGET_TEMP = 30            # degrees C
TEMPERATURE_ACCURACY = 0.1  # degrees C
SLEEPTIME = 0.005           # time between measurements
RECORD_FREQUENCY = 5        # how many measurements/second should be recorded

# STIR SPEEDS
STIR_STOP = 0
STIR_SLOW = 1
STIR_FAST = 2

# setup temperature sensor
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
sensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=1000.0, ref_resistor=4300.0)

# setup pH sensor
i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ads1015(i2c, data_rate=920, gain=2)
chan = AnalogIn(adc, ADS.P0, ADS.P1)

test_readings()

# Display options to the user (including starting titration)
# run_options()

def test_readings():
    '''Test function to test data readings; prints temperature and pH readings every second'''
    # print("Ideal: {}\tActual: {}\tPercDiff: {}".format(volts, diff, percent_diff))

    while True:
        print(datetime.now())
        print("Temperature readings: ")
        temp, res = read_temperature()
        print('Temperature: {0:0.3f}C'.format(temp))
        print('Resistance: {0:0.3f} Ohms'.format(res))

        print("pH readings: ")
        volts, diff, percent_diff = read_pH()
        print('Voltage: {0:0.3f}mV'.format(volts))
        time.sleep(1)

def run_options():
    print("0. Run titration\n1. Calibrate\n2. Settings")  # user options upon startup of system

    # TODO read input from keypad; runMode based on user input
    runMode = 0

    if runMode == 0:
        run_titration()
    elif runMode == 1:
        calibrate()
    else:
        edit_settings()


def run_titration():
    '''Driver for running the titration'''
    current_pH = read_pH()  
    solution_weight, pH_molarity = read_user_values_for_titration()
    initial_titration()
    titrate(TARGET_PH, 0.05)


def read_user_values_for_titration():
    '''Prompts the user to input solution weight, pH molarity'''
    # TODO output to LCD screen prompt asking user to enter solution weight, pH molarity


def calibrate():
    '''Calibrates pH, ...'''
    # TODO implement calibration routine 


def edit_settings(setting1, setting2):
    '''Updates settings with user input'''
    # TODO implement GUI allowing the user to edit certain titration values


def initial_titration(target_pH, current_pH, solution_weight, pH_molarity):
    '''Initial titration; differs from normal titration in that the goal is to reach the target pH with as little effort as possible. 
    (1) Adds HCL until a pH of about 3.5 is reached
    (2) Begin stirring slowly'''

    stir(STIR_SLOW)
    vol_to_add = determine_addition_volume(target_pH, current_pH, solution_weight, pH_molarity)
    while vol_to_add > 0:
        dispense_HCl(vol_to_add)
        current_pH = read_pH()
        vol_to_add = determine_addition_volume(current_pH)


def determine_addition_volume(target_pH, current_pH, solution_weight, pH_molarity):
    '''Function for determining how much vol cm^3 HCl should be added to get to the required pH value without passing it; returns 0 if no HCl should be added'''
    return 


def titrate(pH_target, solution_increment_amount):
    '''Incrementally adds HCl depending on the input parameters, until target pH is reached
    '''
    # NOTE If increment value is 20, don't want to add that again to get it close to 3.5...

    # Current pH level; calculated from pH monitor readings
    pH_old = read_pH()

    # how many iterations should the pH value be close before breaking?
    while True:
        pH_new = read_pH()
        temp_reading = read_temperature()
        # measure temp from GPIO
        # measure pH from GPIO
        
        # make sure temperature within correct bounds; global value for all titrations
        if (temp_reading - TARGET_TEMP > TEMPERATURE_ACCURACY):
            print("TEMPERATURE ERROR MESSAGE")
            break
            # Does this invalidate experiment? If so, break out
            # Log error and alert user; write last data to file

        # ensure pH hasn't changed that much since last reading (might not be robust enough)
        if ((pH_new - pH_old) < STABILIZATION_CONSTANT):
            if (pH_new - pH_target < PH_ACCURACY):
                break
            dispense_HCl(solution_increment_amount)
        pH_old = pH_new

        # TODO store temp, pH values or immediately write to file (might be slow)
        # Write to raw data file and (more usable) data file?

        sleep(SLEEPTIME)

    # TODO add degas time?

    while (current_pH - TARGET_PH) > PH_ACCURACY:
        # TODO 
        dispense_HCl(0.05)
        # TODO measure new pH level; wait until readings have settled
        current_pH = new_pH
        # TODO write out data to csv file



# GPIO in/out Functions

def dispense_HCl(volume):
    '''Adds HCl to the solution'''
    # stepper motor driver needed here; will likely connect to the Arduino
    # NOTE should this wait for pH to settle instead of read_pH?


def read_pH():
    '''Reads and returns the pH value from GPIO'''
    # Read pH registers; pH_val is raw value from pH probe
    # pH_val = bus.read_i2c_block_data(pH_address, reg_pH, 2) 
    # TODO check datasheet for pH probe to determine how many bits/bytes needed
    volts = chan.voltage
    diff = volts / 9.7
    volts = volts / 10
    percent_diff = (diff - volts)/volts*100

    return volts, diff, percent_diff


def convert_pH_to_voltage():
    '''Since we don't want to be converting the voltage readings to equivalent pH values each time, we will go the other way (when converting user input pH values and for readability within the code)'''
    


def read_temperature():
    '''Reads and returns the temperature from GPIO'''
    # print('Temperature: {0:0.3f}C'.format(sensor.temperature))
    # print('Resistance: {0:0.3f} Ohms'.format(sensor.resistance))
    return sensor.temperature, sensor.resistance


def stir(speed):
    '''Speeds needed are (0) STIR_STOP, (1) STIR_SLOW, and (2) STIR_FAST
    Speed is a value between 
    '''
    # NOTE potentiometer will likely be SPI (plenty of pins for SPI)
    # NOTE gpiozero library also contains potentiometer capabilities
    
    msb = speed >> 8
    lsb = speed & 0xFF
    spi.xfer([msb, lsb])
