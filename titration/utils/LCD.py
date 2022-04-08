from titration.utils.UIState import UIState, MainMenu
from titration.utils import interfaces, constants
import types

if constants.IS_TEST == False:  # See conftest.py for configuration of pytest
    from titration.utils.devices import (
        keypad,
        lcd,
    )
from titration.utils.devices import (
    board_mock,
    keypad_mock,
    lcd_mock,
)
from titration.utils.devices.keypad_mock import Keypad
lcd_class: types.ModuleType = lcd_mock
board_class: types.ModuleType = board_mock
keypad_class: types.ModuleType = keypad_mock

ui_lcd = lcd_class.LCD(
    rs=board_class.D27,
    backlight=board_class.D15,
    enable=board_class.D22,
    d4=board_class.D18,
    d5=board_class.D23,
    d6=board_class.D24,
    d7=board_class.D25,
)
ui_lcd.begin(constants.LCD_WIDTH, constants.LCD_HEIGHT)

ui_keypad = keypad_class.Keypad(
    r0=board_class.D1,
    r1=board_class.D6,
    r2=board_class.D5,
    r3=board_class.D19,
    c0=board_class.D16,
    c1=board_class.D26,
    c2=board_class.D20,
    c3=board_class.D21,
)

lines = { 1: '', 2: '', 3: '', 4: ''}

def lcd_out(
    message, 
    line,
    style=constants.LCD_LEFT_JUST,
    console=False
):
    """
    Outputs given string to LCD screen
    :param info: string to be displayed on LCD screen
    """
    if constants.LCD_CONSOLE or console:
        print(message)
    else:
        ui_lcd.print(message, line, style)
    lines[line] = message
    
def lcd_clear():
    ui_lcd.clear()
    for key in lines:
        lines[key] = ''

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
        # temperature_controller.update()

        if console:
            user_input = mock_input() # Poll keypad
        else:
            user_input = ui_keypad.keypad_poll()
            pass

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

