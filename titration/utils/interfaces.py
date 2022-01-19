"""Functions to interface with sensors and peripherals"""

import time  # time.sleep()
import types

from titration.utils import analysis, constants
if constants.IS_TEST == False:
    from titration.utils.devices import (
        keypad,
        lcd,
        ph_probe,

    )
from titration.utils.devices import (
    board_mock,
    keypad_mock,
    lcd_mock,
    ph_probe_mock,
    stir_control_mock,
    syringe_pump,
    syringe_pump_mock,
    temperature_control,
    temperature_control_mock,
    temperature_probe,
    temperature_probe_mock,
)

ph_class: types.ModuleType = ph_probe_mock
temperature_class: types.ModuleType = temperature_probe_mock
board_class: types.ModuleType = board_mock
lcd_class: types.ModuleType = lcd_mock
keypad_class: types.ModuleType = keypad_mock
temperature_control_class: types.ModuleType = temperature_control_mock
syringe_class: types.ModuleType = syringe_pump_mock
stir_class: types.ModuleType = stir_control_mock

# global, pH, lcd, and temperature probes
ph_sensor = None
temperature_sensor = None
arduino = None
ui_lcd = None
ui_keypad = None
temperature_controller = None
stir_controller = None


def setup_interfaces():
    """
    Initializes components for interfacing with pH probe,
    temperature probe, and stepper motor/syringe pump
    """
    global ph_sensor, temperature_sensor, arduino, ui_lcd, ui_keypad, temperature_controller, stir_controller

    # set module classes
    setup_module_classes()

    # LCD and ui_keypad setup
    ui_lcd = setup_lcd()
    ui_keypad = setup_keypad()

    # Temperature Control Setup
    temperature_sensor = setup_temperature_probe()
    temperature_controller = setup_temperature_control()
    ph_sensor = setup_ph_probe()
    arduino = setup_syringe_pump()
    stir_controller = setup_stir_control()


def setup_module_classes():
    """
    Checks constants.IS_TEST and determines if classes should be
    mocked or
    """
    global ph_class, temperature_class, board_class, lcd_class, keypad_class, temperature_control_class, syringe_class, stir_class  # noqa: E501
    if constants.IS_TEST:
        ph_class = ph_probe_mock
        temperature_class = temperature_probe_mock
        board_class = board_mock
        lcd_class = lcd_mock
        keypad_class = keypad_mock
        temperature_control_class = temperature_control_mock
        syringe_class = syringe_pump_mock
        stir_class = stir_control_mock
    elif constants.IS_TEST is False:
        # NOTE: The board module can only be imported if
        # running on specific hardware (i.e. Raspberry Pi)
        # It will fail on regular Windows/Linux computers
        import board  # All hardware (see above note)

        # Similarly, stir_control imports pwmio which will fail
        from titration.utils.devices import stir_control

        ph_class = ph_probe
        temperature_class = temperature_probe
        board_class = board
        lcd_class = lcd
        keypad_class = keypad
        temperature_control_class = temperature_control
        syringe_class = syringe_pump
        stir_class = stir_control


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


def setup_syringe_pump():
    return syringe_class.Syringe_Pump()


def setup_stir_control(debug=False):
    return stir_class.Stir_Control(board_class.D13, debug=debug)


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
            print("Input: ", user_input, type(user_input))
            break
        else:
            print("Input: ", user_input, type(user_input))
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
    arduino.pump_volume(volume, direction)


def set_pump_volume(volume):
    arduino.set_volume_in_pump(volume)


def stir_speed_fast():
    stir_controller.motor_speed_fast()


def stir_speed_slow():
    stir_controller.motor_speed_slow()


def stir_speed(pwm_speed, gradual=False):
    stir_controller.set_motor_speed(pwm_speed, gradual)


def stir_stop():
    stir_controller.motor_stop()


def _test_add_HCl():
    constants.hcl_call_iter += (
        1  # value only used for testing while reading pH doesn't work
    )
    constants.pH_call_iter = -1
