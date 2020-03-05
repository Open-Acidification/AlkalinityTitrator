from pad4pi import rpi_gpio
import time

# Setup Keypad
KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
]

# same as calling: factory.create_4_by_4_keypad, still we put here fyi:
ROW_PINS = [26, 19, 13, 6] # BCM numbering
COL_PINS = [5, 16, 20, 21] # BCM numbering

factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

def select_menu_options(key):
    print(key)

def run_options():
    print("0. Run titration\n1. Calibrate\n2. Settings")  # user options upon startup of system
    # printKey will be called each time a keypad button is pressed
    keypad.registerKeyPressHandler(select_menu_options)

    try:
        while(True):
            time.sleep(0.2)
    except:
        keypad.cleanup()

run_options()
