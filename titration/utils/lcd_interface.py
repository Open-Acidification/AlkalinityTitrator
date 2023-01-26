from titration.utils import constants
import types

from titration.utils.devices import (
    board_mock,
    keypad_mock,
    lcd_mock,
)

lcd_class: types.ModuleType = lcd_mock
board_class: types.ModuleType = board_mock
keypad_class: types.ModuleType = keypad_mock

ui_lcd = lcd_class.LiquidCrystal(
    rs=board_class.D27,
    backlight=board_class.D15,
    enable=board_class.D22,
    d4=board_class.D18,
    d5=board_class.D23,
    d6=board_class.D24,
    d7=board_class.D25,
    cols=constants.LCD_HEIGHT,
    rows=constants.LCD_WIDTH,
)

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

lines = {1: "", 2: "", 3: "", 4: ""}


def lcd_out(message, line, style=constants.LCD_LEFT_JUST, console=False):
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
        lines[key] = ""


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

        # if console:
        # ? user_input = mock_input()  # Poll keypad
        if not console:
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
