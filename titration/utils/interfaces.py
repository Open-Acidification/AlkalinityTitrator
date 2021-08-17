"""Functions to interface with sensors and peripherals"""

import time  # time.sleep()
import types

import serial  # Pump

from titration.utils import analysis, constants
from titration.utils.devices import (
    board_mock,
    keypad,
    keypad_mock,
    lcd,
    lcd_mock,
    ph_probe,
    ph_probe_mock,
    serial_mock,
    temperature_control,
    temperature_control_mock,
    temperature_probe,
    temperature_probe_mock,
)

ph_class: types.ModuleType = None
temperature_class: types.ModuleType = None
board_class: types.ModuleType = None
lcd_class: types.ModuleType = None
keypad_class: types.ModuleType = None
temperature_control_class: types.ModuleType = None
serial_class: types.ModuleType = None

# global, pH, lcd, and temperature probes
ph_sensor = None
temperature_sensor = None
arduino = None
ui_lcd = None
ui_keypad = None
temperature_controller = None


def setup_module_classes():
    """
    Checks constants.IS_TEST and determines if classes should be
    mocked or
    """
    global ph_class, temperature_class, board_class, lcd_class, keypad_class, temperature_control_class, serial_class
    if constants.IS_TEST:
        ph_class = ph_probe_mock
        temperature_class = temperature_probe_mock
        board_class = board_mock
        lcd_class = lcd_mock
        keypad_class = keypad_mock
        temperature_control_class = temperature_control_mock
        serial_class = serial_mock
    elif constants.IS_TEST is False:
        # NOTE: The board module can only be imported if
        # running on specific hardware (i.e. Raspberry Pi)
        # It will fail on regular Windows/Linux computers
        import board  # All hardware (see above note)

        ph_class = ph_probe
        temperature_class = temperature_probe
        board_class = board
        lcd_class = lcd
        keypad_class = keypad
        temperature_control_class = temperature_control
        serial_class = serial


def setup_interfaces():
    """
    Initializes components for interfacing with pH probe,
    temperature probe, and stepper motor/syringe pump
    """
    global ph_sensor, temperature_sensor, arduino, ui_lcd, ui_keypad, temperature_controller

    # set module classes
    setup_module_classes()

    # LCD and ui_keypad setup
    ui_lcd = setup_lcd()
    ui_keypad = setup_keypad()

    # Temperature Control Setup
    temperature_sensor = setup_temperature_probe()
    temperature_controller = setup_temperature_control()
    ph_sensor = setup_ph_probe()
    arduino = setup_arduino()


def setup_lcd():
    temp_lcd = lcd_class.LCD(
        rs=board_class.D27,
        backlight=board_class.D15,
        enable=board_class.D22,
        d4=board_class.D18,
        d5=board_class.D23,
        d6=board_class.D24,
        d7=board_class.D25,
    )

    temp_lcd.begin(constants.LCD_WIDTH, constants.LCD_HEIGHT)

    return temp_lcd


def setup_keypad():
    temp_keypad = keypad_class.Keypad(
        r0=board_class.D1,
        r1=board_class.D6,
        r2=board_class.D5,
        r3=board_class.D19,
        c0=board_class.D16,
        c1=board_class.D26,
        c2=board_class.D20,
        c3=board_class.D21,
    )

    return temp_keypad


def setup_temperature_probe():
    return temperature_class.Temperature_Probe(
        board_class.SCK, board_class.MOSI, board_class.MISO, board_class.D4, wires=3
    )


def setup_temperature_control():
    # Create a new sensor attached to the 2nd probe (D0) for the temperature controller alone
    sensor = temperature_class.Temperature_Probe(
        board_class.SCK, board_class.MOSI, board_class.MISO, board_class.D0, wires=3
    )
    return temperature_control_class.Temperature_Control(constants.RELAY_PIN, sensor)


def setup_ph_probe():
    return ph_class.pH_Probe(board_class.SCL, board_class.SDA, gain=8)


def setup_arduino():
    temp_arduino = serial_class.Serial(
        port=constants.ARDUINO_PORT,
        baudrate=constants.ARDUINO_BAUD,
        timeout=constants.ARDUINO_TIMEOUT,
    )
    temp_arduino.reset_input_buffer()
    temp_arduino.reset_output_buffer()

    return temp_arduino


def delay(seconds, countdown=False):
    # Use time.sleep() if the temperature controller isn't initialized yet
    if temperature_controller is None:
        time.sleep(seconds)
        return

    timeEnd = time.time() + seconds
    timeNow = time.time()
    while timeEnd > timeNow:
        temperature_controller.update()
        timeLeft = timeEnd - timeNow
        if countdown and int(timeLeft) % 5 == 0:
            lcd_out("Time Left: {}".format(int(timeLeft)), line=4)
        timeNow = time.time()


def lcd_out(
    message,
    line,
    style=constants.LCD_LEFT_JUST,
    console=False,
):
    """
    Outputs given string to LCD screen
    :param info: string to be displayed on LCD screen
    """
    if constants.LCD_CONSOLE or console:
        print(message)
    else:
        ui_lcd.print(message, line, style)


def lcd_clear():
    ui_lcd.clear()


def display_list(dict_to_display):
    """
    Display a list of options from a dictionary. Only the first four
    options will be displayed due to only four screen rows.
    :param list_to_display: list to be displayed on LCD screen
    """
    lcd_clear()
    keys = list(dict_to_display.keys())
    values = list(dict_to_display.values())
    lines = [1, 2, 3, 4]

    for i in range(min(len(keys), 4)):
        ui_lcd.print(str(keys[i]) + ". " + values[i], lines[i])

    # Original method, slow due to screen scrolling
    # for key, value in list_to_display.items():
    #   lcd_out(str(key) + '. ' + value)


def read_user_input(valid_inputs=None, console=False):
    """
    Reads user input from keypad
    :param valid_inputs: optional, valid inputs from the user
    :return: user input selection
    """
    # TODO interface with keypad
    # Temporarily query user input from terminal
    user_input = None

    while True:
        temperature_controller.update()

        if console:
            user_input = input()
        else:
            user_input = ui_keypad.keypad_poll()

        if user_input is None:
            pass
        elif valid_inputs is None or user_input in valid_inputs:
            print("Input: ", user_input)
            break
        else:
            print("Input: ", user_input)
            lcd_out(
                constants.VALID_INPUT_WARNING,
                constants.LCD_LINE_1,
                constants.LCD_LEFT_JUST,
            )

    while True:
        if ui_keypad.keypad_poll() is None:
            break
    return user_input


def read_user_value(message):
    """Prompts the user to enter a value using the keypad"""
    instructions_1 = "* = .       B = BS"
    instructions_2 = "A = accept  C = Clr"
    inputs = []

    lcd_out(message, line=1)
    lcd_out("_", style=constants.LCD_CENT_JUST, line=2)
    lcd_out(instructions_1, line=3)
    lcd_out(instructions_2, line=4)

    # Take inputs until # is pressed
    user_input = None
    string = ""

    # Flag for preventing multiple decimals
    decimal = False
    while True:
        user_input = read_user_input()

        # A is accept, if entered, end loop
        if user_input == "A":
            break

        # B is backspace, pop a value
        elif user_input == "B":
            if len(inputs) > 0:
                popped = inputs.pop()
                if popped == "*":
                    decimal = False
                string = string[:-1]

        # C is clear, pop all values
        elif user_input == "C":
            inputs.clear()
            decimal = False
            string = "_"

        # D would be "decline", going back to the previous screen
        elif user_input == "D":
            # We would LIKE to go back to the previous routine,
            # but we can't currently support that easily
            pass

        elif user_input == "#":
            # Currently no implementation planned for this
            pass

        # Else, the value will be '.' or a number
        elif user_input.isnumeric() or user_input == "*":

            # Check for decimal. If there is already one, do nothing
            if user_input == "*":
                if not decimal:
                    inputs.append(user_input)
                    string = string + "."
                    decimal = True
            # Otherwise, add number to input list
            else:
                string = string + str(user_input)
                inputs.append(int(user_input))
        else:
            # ignore the input
            pass

        # Display updated input
        if len(inputs) == 0:
            lcd_out("_", style=constants.LCD_CENT_JUST, line=2)
        else:
            lcd_out(string, style=constants.LCD_CENT_JUST, line=2)

        # DEBUG
        # print("Inputs: ", inputs)
        # print("String: ", string)
        # print("Decimal: ", decimal)

    value = 0.0
    decimal = False
    decimal_div = 10
    for i in range(len(inputs)):
        if not decimal:
            if inputs[i] == "*":
                decimal = True
                pass
            else:
                value = value * 10 + inputs[i]
        else:
            value = value + inputs[i] / decimal_div
            decimal_div = decimal_div * 10
        # DEBUG
        # print("Value: ", value)

    # DEBUG
    # print("Final: ", value)

    return value


def read_pH():
    """
    Reads calibration-adjusted value for pH
    :returns: adjusted pH value in units of pH, raw V reading from probe
    """
    volts = read_raw_pH()
    temperature = read_temperature()[0]
    pH_val = analysis.calculate_pH(volts, temperature)
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
    volts = ph_sensor.voltage()

    return volts


def read_temperature():
    """
    Reads and returns the temperature from GPIO
    :returns: temperature in celsius, resistance in ohms
    """
    return temperature_sensor.get_temperature(), temperature_sensor.get_resistance()


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
            lcd_out("Volume > pumpable", style=constants.LCD_CENT_JUST, line=4)
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
    constants.hcl_call_iter += (
        1  # value only used for testing while reading pH doesn't work
    )
    constants.pH_call_iter = -1


def drive_pump(volume, direction):
    """Converts volume to cycles and ensures and checks pump level and values"""
    if direction == 0:
        space_in_pump = constants.MAX_PUMP_CAPACITY - constants.volume_in_pump
        if volume > space_in_pump:
            lcd_out("Filling Error", line=4)
        else:
            lcd_out("Filling {0:1.2f} ml".format(volume), line=4)
            cycles = analysis.determine_pump_cycles(volume)
            drive_step_stick(cycles, direction)
            constants.volume_in_pump += volume
    elif direction == 1:
        if volume > constants.volume_in_pump:
            lcd_out("Pumping Error", line=4)
        else:
            lcd_out("Pumping {0:1.2f} ml".format(volume), line=4)
            cycles = analysis.determine_pump_cycles(volume)
            offset = drive_step_stick(cycles, direction)
            # offset is what is returned from drive_step_stick which originally is returned from the arduino
            if offset != 0:
                drive_step_stick(offset, 0)
                drive_step_stick(offset, 1)
            constants.volume_in_pump -= volume

    lcd_out("Pump Vol: {0:1.2f} ml".format(constants.volume_in_pump), line=4)


def drive_step_stick(cycles, direction):
    """
    cycles and direction are integers
    Communicates with arduino to add HCl through pump
    :param cycles: number of rising edges for the pump
    :param direction: direction of pump
    """
    if cycles == 0:
        return 0

    delay(0.01)
    if arduino.writable():
        arduino.write(cycles.to_bytes(4, "little"))
        arduino.write(direction.to_bytes(1, "little"))
        arduino.flush()
        wait_time = cycles / 1000 + 0.5
        print(time.ctime())
        print("wait_time = ", wait_time)
        delay(wait_time)
        print(time.ctime(), "\n\n")
        temp = arduino.readline()
        if temp == b"DONE\r\n" or temp == b"":
            return 0
        else:
            return int(temp)
    else:
        lcd_out("Arduino Unavailable", 4, constants.LCD_CENT_JUST)
