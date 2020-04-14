# Functions to interface with sensors and peripherals
import constants


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


# old but usable?


def read_temperature():
    """Reads and returns the temperature from GPIO"""
    # print('Temperature: {0:0.3f}C'.format(sensor.temperature))
    # print('Resistance: {0:0.3f} Ohms'.format(sensor.resistance))    
    return sensor.temperature


def read_pH():
    """Reads and returns the pH value from GPIO"""
    # Read pH registers; pH_val is raw value from pH probe
    volts = chan.voltage
    diff = volts / 9.7
    volts = volts / 10
    # percent_diff = (diff - volts)/volts*100
    return volts, diff  # , percent_diff


def dispense_HCl(volume):
    """Adds HCl to the solution"""
    # stepper motor driver needed here; will likely connect to the Arduino
    # NOTE should this wait for pH to settle instead of read_pH?