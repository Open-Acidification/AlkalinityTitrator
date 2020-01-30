'''Alkalinity titration procedure 
Author: Kaden Sukachevin

Walla Walla University 
'''
# Libraries
from time import sleep
from gpiozero as gpio

import board 
import busio
import digitalio
import adafruit_max31865

# CircuitPython? For communicating with PT1000 sensor
# Before continuing make sure your board's lib folder or root filesystem has the adafruit_max31865.mpy, and adafruit_bus_device files and folders copied over.

# Python script to continuously read data
#!/usr/bin/python
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)  # spi port 0, device 0
spi.max_speed_hz = 976000

# CONSTANTS
PH_ACCURACY = 0.01  # Needed accuracy for final pH level after titration
TARGET_PH = 3.0  # Target pH value for titration process
TARGET_TEMP = 30  # degrees C
TEMPERATURE_ACCURACY = 0.1  # degrees C
SLEEPTIME = 0.005  # time between measurements
RECORD_FREQUENCY = 5  # how many measurements/second should be recorded

# STIR SPEEDS
SLOW = 0
FAST = 1

initialize()

def displayOptions():
    print("0. Run titration\n1. Calibrate\n2. Settings")  # user options upon startup of system

    # TODO read input from keypad; runMode based on user input
    runMode = 0

    if runMode == 0:
        titrate()
    elif runMode == 1:
        calibrate()
    else:
        editSettings()


def initialize():
    '''Initialize GPIO ports'''
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.D5)
    sensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=1000.0, ref_resistor=4300.0)


def calibrate():
    '''Calibrates pH, ...'''
    # TODO implement calibration routine 


def editSettings(setting1, setting2):
    '''Updates settings with user input'''
    # TODO implement GUI allowing the user to edit certain titration values

    
    titrate(3.5, 20, SLOW)


def initialTitration():
    '''Initial titration
    (1) Adds HCL until a pH of about 3.5 is reached
    (2) Begin stirring slowly'''

    stir(SLOW)
    titrate(3.5, 20)

    stir(slow)  # start stirring slowly to ensure mixture


def titrate(pH_target, solution_increment_amount):
    '''Incrementally adds HCl depending on the input parameters, until target pH is reached

    (1) 

    If increment value is 20, don't want to add that again to get it close to 3.5...
    '''
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
            dispenseHCL(solution_increment_amount)
        pH_old = pH_new

        # TODO store temp, pH values or immediately write to file (might be slow)
        # Write to raw data file and (more usable) data file?

        sleep(SLEEPTIME)

    # TODO add degas time?

    while (current_pH - TARGET_PH) > PH_ACCURACY:
        # TODO 
        dispenseHCL(0.05)
        # TODO measure new pH level; wait until readings have settled
        current_pH = new_pH
        # TODO write out data to csv file


def dispenseHCL(amount):
    '''Adds HCL to the solution'''
    # stepper motor driver needed here


def readPh():
    '''Reads and returns the pH value from GPIO'''


def readTemperature():
    '''Reads and returns the temperature from GPIO'''
    print('Temperature: {0:0.3f}C'.format(sensor.temperature))
    print('Resistance: {0:0.3f} Ohms'.format(sensor.resistance))


def stir(speed):
    '''Speeds needed are (1) stop, (2) slow, and (3) fast
    Speed is a value between 
    '''
    # NOTE potentiometer will likely be SPI (plenty of pins for SPI)
    # NOTE gpiozero library also contains potentiometer capabilities
    
    msb = speed >> 8
    lsb = speed & 0xFF
    spi.xfer([msb, lsb])
