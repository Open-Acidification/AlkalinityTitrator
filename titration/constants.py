# Display
LCD_CONSOLE = False

VALID_INPUT_WARNING = 'Input Invalid'
# keypad
KEY_0 = 0
KEY_1 = 1
KEY_2 = 2
KEY_3 = 3
KEY_4 = 4
KEY_5 = 5
KEY_6 = 6
KEY_7 = 7
KEY_8 = 8
KEY_9 = 9
KEY_A = 'A'
KEY_B = 'B'
KEY_C = 'C'
KEY_D = 'D'
KEY_STAR = '*'
KEY_HASH = '#'

# user choice options
ROUTINE_OPTIONS_1 = {
    KEY_1: 'Run titration',
    KEY_2: 'Calibrate sensors',
    KEY_3: 'Prime Pump',
    KEY_STAR: 'Page 2'
}

ROUTINE_OPTIONS_2 = {
    KEY_4: 'Update settings',
    KEY_5: 'Test Mode',
    KEY_6: 'Exit',
    KEY_STAR: 'Page 1'
}

TEST_OPTIONS_1 = {
    KEY_1: "Read Values",
    KEY_2: "Pump",
    KEY_3: "Set Volume",
    KEY_STAR: "Page 2"
}

TEST_OPTIONS_2 = {
    KEY_4: "Toggle Test Mode",
    KEY_5: "Read Volume",
    KEY_6: "Exit"
    KEY_STAR: "Page 1"
}

SENSOR_OPTIONS = {
    KEY_1: 'pH',
    KEY_2: 'Temperature'
}

KEY_VALUES = {
  0: {
    0: KEY_1,
    1: KEY_2,
    2: KEY_3,
    3: KEY_A,
  },

  1: {
    0: KEY_4,
    1: KEY_5,
    2: KEY_6,
    3: KEY_B,
  },

  2: {
    0: KEY_7,
    1: KEY_8,
    2: KEY_9,
    3: KEY_C,
  },

  3: {
    0: KEY_STAR,
    1: KEY_0,
    2: KEY_HASH,
    3: KEY_D,
  }
}

# Small times steps (s) in the delay function
DELAY_STEP = 0.0001

# LCD Device Constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LEFT_JUST = 1
LCD_CENT_JUST = 2
LCD_RIGHT_JUST = 3
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
 
# LCD Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# for pH calibration constants
calibration_data_format = {
    'pH': {
        'ref_voltage': 200,
        'ref_pH': 7
    },
    'temp': {
        'ref_resistance': 4300.0,
        'nominal_resistance': 1000.0
    },
    'vol_pump': 0
}

CALIBRATION_FILENAME = 'titration/calibration.json'
# temp calibration values
TEMP_REF_RESISTANCE = 4300.0
TEMP_NOMINAL_RESISTANCE = 1000.0
# pH
UNIVERSAL_GAS_CONST = 8.31447215
FARADAY_CONST = 96485.33212
CELSIUS_TO_KELVIN = 273.15
# pH calibration values
PH_REF_VOLTAGE = -0.012
PH_REF_PH = 7.0
# titration routine
TARGET_TEMP = 30.0  # degrees C
TARGET_PH_INIT = 4.5
TARGET_PH_MID = 3.5
TARGET_PH_FINAL = 3.0
TEMPERATURE_ACCURACY = 0.25
PH_ACCURACY = 0.1
TITRATION_WAIT_TIME = 1
INCREMENT_AMOUNT_INIT = 1.0
INCREMENT_AMOUNT_MID = 0.1
INCREMENT_AMOUNT_FINAL = 0.05
TARGET_STD_DEVIATION = 0.15

# Temp Control
RELAY_PIN = 12

# pump settings
#ARDUINO_PORT = "/dev/ttyUSB0"
ARDUINO_PORT = "/dev/ttyACM0"
ARDUINO_BAUD = 9600
ARDUINO_TIMEOUT = 5
# maps vol to number of pulses needed
NUM_CYCLES = {0.05 : 470,
              1: 9550}
CYCLES_VOLUME_RATIO = 9550  # 1 mL is 9550 pump cycles
MAX_PUMP_CAPACITY = 1.1  # max capacity of pump in mL
# defaults
DEFAULT_TEMP_REF_RESISTANCE = 4300.0
DEFAULT_TEMP_NOMINAL_RESISTANCE = 1000.0
DEFAULT_PH_REF_VOLTAGE = -.012
DEFAULT_PH_REF_PH = 7.0
# data paths
DATA_PATH = ''
volume_in_pump = 0  # keep track of solution in pump

# TESTING
test_pH_vals = [[7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
                [7.0, 6.8, 6.5, 6.4, 6.0, 5.4, 5.2, 5.1, 5.1, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                [5.0, 4.5, 4.4, 4.1, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9],
                [3.9, 3.8, 3.7, 3.6, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.51, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5],
                [3.5, 3.5, 3.4, 3.43, 3.4, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3],
                [3.3, 3.28, 3.27, 3.27, 3.2, 3.2, 3.2, 3.15, 3.13, 3.12, 3.12, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1, 3.1],
                [3.1, 3.05, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]]
hcl_call_iter = 0
pH_call_iter = -1
IS_TEST = False
