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


# global, pH, and temperature probes
ph_sensor = None
temperature_sensor = None
arduino = None

global_keypad = keypad_class.Keypad()


temperature_controller = None
stir_controller = None

lcd = lcd_class.LiquidCrystal(
    cols=constants.LCD_WIDTH,
    rows=constants.LCD_HEIGHT,
)


def setup_interfaces():
    """
    Initializes components for interfacing with pH probe,
    temperature probe, and stepper motor/syringe pump
    """

    global ph_sensor, temperature_sensor, arduino, temperature_controller, stir_controller

    # Temperature Control Setup
    temperature_sensor = setup_temperature_probe()
    temperature_controller = setup_temperature_control()
    ph_sensor = setup_ph_probe()
    arduino = setup_syringe_pump()
    stir_controller = setup_stir_control()


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
                "Input Invalid",
                1,
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
    lcd.print("_", style="center", line=2)
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
            lcd.print("_", style="center", line=2)
        else:
            lcd.print(string, style="center", line=2)

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
