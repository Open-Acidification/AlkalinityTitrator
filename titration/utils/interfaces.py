"""Functions to interface with sensors and peripherals"""

import time

from titration.utils import analysis, constants

if constants.IS_TEST:
    from titration.utils.devices import (
        board_mock as board_class,
        keypad_mock as keypad_class,
        liquid_crystal_mock as lcd_class,
        ph_probe_mock as ph_class,
        stir_control_mock as stir_class,
        syringe_pump_mock as syringe_class,
        temperature_control_mock as temperature_control_class,
        temperature_probe_mock as temperature_class,
    )
else:
    from titration.utils.devices import (  # type: ignore
        keypad as keypad_class,
        liquid_crystal as lcd_class,
        ph_probe as ph_class,
        syringe_pump as syringe_class,
        temperature_control as temperature_control_class,
        temperature_probe as temperature_class,
    )


ph_sensor = ph_class.pH_Probe(board_class.SCL, board_class.SDA, gain=8)

temperature_sensor = temperature_class.Temperature_Probe(
    board_class.SCK, board_class.MOSI, board_class.MISO, board_class.D4, wires=3
)
pump = syringe_class.Syringe_Pump()

temperature_controller = temperature_control_class.Temperature_Control(
    constants.RELAY_PIN, temperature_sensor
)
stir_controller = stir_class.Stir_Control(board_class.D13, debug=False)

global_keypad = keypad_class.Keypad(
    r0=board_class.D1,
    r1=board_class.D6,
    r2=board_class.D5,
    r3=board_class.D19,
    c0=board_class.D16,
    c1=board_class.D26,
    c2=board_class.D20,
    c3=board_class.D21,
)

lcd = lcd_class.LiquidCrystal(
    rs=board_class.D27,
    backlight=board_class.D15,
    enable=board_class.D22,
    d4=board_class.D18,
    d5=board_class.D23,
    d6=board_class.D24,
    d7=board_class.D25,
    cols=constants.LCD_WIDTH,
    rows=constants.LCD_HEIGHT,
)


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
            lcd.print("Time Left: {}".format(int(timeLeft)), line=4)
        timeNow = time.time()


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
            user_input = input()  # Poll keypad
        else:
            user_input = global_keypad.keypad_poll()

        if user_input is None:
            pass
        elif valid_inputs is None or user_input in valid_inputs:
            print("Input: ", user_input, type(user_input))
            break
        else:
            print("Input: ", user_input, type(user_input))
            lcd.print(
                constants.VALID_INPUT_WARNING,
                constants.LCD_LINE_1,
                constants.LCD_LEFT_JUST,
            )

    while True:
        if global_keypad.keypad_poll() is None:
            break
    return user_input


def read_user_value(message):
    """Prompts the user to enter a value using the keypad"""
    instructions_1 = "* = .       B = BS"
    instructions_2 = "A = accept  C = Clr"
    inputs = []

    lcd.print(message, line=1)
    lcd.print("_", style=constants.LCD_CENT_JUST, line=2)
    lcd.print(instructions_1, line=3)
    lcd.print(instructions_2, line=4)

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
            lcd.print("_", style=constants.LCD_CENT_JUST, line=2)
        else:
            lcd.print(string, style=constants.LCD_CENT_JUST, line=2)

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
    volts = ph_sensor.read_raw_pH()
    temperature = temperature_sensor.read_temperature()[0]
    pH_val = analysis.calculate_pH(volts, temperature)
    return pH_val, volts
