from pad4pi import rpi_gpio
import RPi.GPIO as GPIO
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

################
GPIO_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)

# Send a signal to the relay
def OpenGarageDoor():
  try:
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(GPIO_PIN, GPIO.LOW)
  except:
    print ("Error inside function OpenGarageDoor")
    pass

GPIO.cleanup()
################

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

def get_key_pressed_value(key):
    return key

def select_menu_options(key):
    print(key)
    if key == '1':
        print("Key 1 pressed")
        try:
            GPIO.output(GPIO_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(GPIO_PIN, GPIO.LOW)
        except:
            print ("Error inside function OpenGarageDoor")
            pass
    elif key == '2':
        print("Calibrate")
    elif key == '3':
        print("Settings")

def run_options():
    print("1. Run titration\n2. Calibrate\n3. Settings")  # user options upon startup of system
    # printKey will be called each time a keypad button is pressed
    keypad.registerKeyPressHandler(select_menu_options)

    try:
        while(True):
            time.sleep(0.2)
    except:
        keypad.cleanup()


def get_user_input():
    '''Returns a string from the keypad'''
    next_val = keypad.registerKeyPressHandler(get_key_pressed_value)
    total_input = ''

    try:
        while(next_val != '*'):
            time.sleep(0.2)
            total_input += next_val
    except:
        keypad.cleanup()

    print(total_input)


get_user_input()
#run_options()
keypad.cleanup()