'''Alkalinity titration procedure 
Author: Kaden Sukachevin

Walla Walla University 
'''
# Libraries
from time import sleep
from datetime import datetime

from gpiozero as gpio

import board 
import busio
import digitalio
import adafruit_max31865

# for use with I2C
import smbus

# CircuitPython? For communicating with PT1000 sensor
# Before continuing make sure your board's lib folder or root filesystem has the adafruit_max31865.mpy, and adafruit_bus_device files and folders copied over.

# Python script to continuously read data
#!/usr/bin/python
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)  # spi port 0, device 0
spi.max_speed_hz = 976000

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

# INITIALIZE PORTS
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
sensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=1000.0, ref_resistor=4300.0)

test_readings()

bus = smbus.SMBus(0)
address = 0x60

def bearing255():
        bear = bus.read_byte_data(address, 1)
        return bear

def bearing3599():
        bear1 = bus.read_byte_data(address, 2)
        bear2 = bus.read_byte_data(address, 3)
        bear = (bear1 << 8) + bear2
        bear = bear/10.0
        return bear

while True:
        bearing = bearing3599()     #this returns the value to 1 decimal place in degrees. 
        bear255 = bearing255()      #this returns the value as a byte between 0 and 255. 
        print bearing
        print bear255
        time.sleep(1)

# Display options to the user (including starting titration)
# display_options()

def test_readings():
    while True:
        print(datetime.now())
        print("Temperature readings: ")
        temp, res = read_temperature()
        print('Temperature: {0:0.3f}C'.format(temp))
        print('Resistance: {0:0.3f} Ohms'.format(res))

        print("pH readings: ")
        volt = read_pH()
        print('Voltage: {0:0.3f}mV'.format(volt))
        time.sleep(1)

def display_options():
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
    current_pH = 0  # TODO get this value from GPIO; should this be a global variable or passed from function to function?
    solution_weight, pH_molarity = read_user_values_for_titration()
    fast_titration()
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


def fast_titration(target_pH):
    '''Initial titration; differs from normal titration in that the goal is to reach the target pH with as little effort as possible. 
    (1) Adds HCL until a pH of about 3.5 is reached
    (2) Begin stirring slowly'''

    stir(STIR_SLOW)
    vol_to_add = determine_addition_volume(current_pH)
    while vol_to_add > 0:
        dispense_HCl(vol_to_add)
        current_pH = read_pH()
        vol_to_add = determine_addition_volume(current_pH)

    titrate(3.5, 20)

def determine_addition_volume():
    '''Function for determining how much vol cm^3 HCl should be added to get to the required pH value without passing it; returns 0 if no HCl should be added'''


def titrate(pH_target, solution_increment_amount):
    '''Incrementally adds HCl depending on the input parameters, until target pH is reached
    '''
    # NOTE If increment value is 20, don't want to add that again to get it close to 3.5...

    # Current pH level; calculated from pH monitor readings
    current_pH = 3.5

    # how many iterations should the pH value be close before breaking?
    while True:
        pH_new = pH_GPIO
        temp_reading = temp_GPIO
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


def read_pH():
    '''Reads and returns the pH value from GPIO'''
    # NOTE this function should wait and make sure pH is stable before returning a value
    

    return pH


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
