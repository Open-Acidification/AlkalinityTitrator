# Display
LCD_CONSOLE = False

VALID_INPUT_WARNING = "Input Invalid"
# keypad
NO_KEY = ""
KEY_0 = "0"
KEY_1 = "1"
KEY_2 = "2"
KEY_3 = "3"
KEY_4 = "4"
KEY_5 = "5"
KEY_6 = "6"
KEY_7 = "7"
KEY_8 = "8"
KEY_9 = "9"
KEY_A = "A"
KEY_B = "B"
KEY_C = "C"
KEY_D = "D"
KEY_STAR = "*"
KEY_HASH = "#"

# user choice options
ROUTINE_OPTIONS_1 = {
    KEY_1: "Run titration",
    KEY_2: "Calibrate sensors",
    KEY_3: "Prime Pump",
    KEY_STAR: "Page 2",
}

ROUTINE_OPTIONS_2 = {
    KEY_4: "Update settings",
    KEY_5: "Test Mode",
    KEY_6: "Exit",
    KEY_STAR: "Page 1",
}

SENSOR_OPTIONS = {KEY_1: "pH", KEY_2: "Temperature"}

# Small times steps (s) in the delay function
DELAY_STEP = 0.0001

# LCD Device Constants
LCD_WIDTH = 20  # Maximum characters per line
LCD_HEIGHT = 4
LCD_CHR = True
LCD_CMD = False

LCD_LEFT_JUST = 1
LCD_CENT_JUST = 2
LCD_RIGHT_JUST = 3

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

# LCD Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# for pH calibration constants
calibration_data_format = {
    "pH": {"ref_voltage": 200, "ref_pH": 7},
    "temperature": {"ref_resistance": 4300.0, "nominal_resistance": 1000.0},
    "vol_pump": 0,
}

CALIBRATION_FILENAME = "data/calibration.json"
# temperature calibration values
TEMPERATURE_REF_RESISTANCE = 4300.0
TEMPERATURE_NOMINAL_RESISTANCE = 1000.0
# pH
UNIVERSAL_GAS_CONST = 8.31447215
FARADAY_CONST = 96485.33212
CELSIUS_TO_KELVIN = 273.15
# pH calibration values
PH_REF_VOLTAGE = -0.012
PH_REF_PH = 7.0
# titration routine
TARGET_TEMPERATURE = 30.0  # degrees C
TARGET_PH_INIT = 5.5
TARGET_PH_MID = 3.5
TARGET_PH_FINAL = 3.0
TEMPERATURE_ACCURACY = 0.25
PH_ACCURACY = 0.1
TITRATION_WAIT_TIME = 1
INCREMENT_AMOUNT_INIT = 0.5
INCREMENT_AMOUNT_MID = 0.1
INCREMENT_AMOUNT_FINAL = 0.05
TARGET_STD_DEVIATION = 0.15

# Temperature Control
RELAY_PIN = 12

# pump settings
# maps vol to number of pulses needed
NUM_CYCLES = {0.05: 470, 1: 9550}
CYCLES_VOLUME_RATIO = 9550  # 1 mL is 9550 pump cycles
# defaults
DEFAULT_TEMPERATURE_REF_RESISTANCE = 4300.0
DEFAULT_TEMPERATURE_NOMINAL_RESISTANCE = 1000.0
DEFAULT_PH_REF_VOLTAGE = -0.012
DEFAULT_PH_REF_PH = 7.0
# data paths
DATA_PATH = "data/"

# TESTING
test_pH_vals = [
    [
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
        7.0,
    ],
    [
        7.0,
        6.8,
        6.5,
        6.4,
        6.0,
        5.4,
        5.2,
        5.1,
        5.1,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
    ],
    [
        5.0,
        4.5,
        4.4,
        4.1,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
        3.9,
    ],
    [
        3.9,
        3.8,
        3.7,
        3.6,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.51,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
        3.5,
    ],
    [
        3.5,
        3.5,
        3.4,
        3.43,
        3.4,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
        3.3,
    ],
    [
        3.3,
        3.28,
        3.27,
        3.27,
        3.2,
        3.2,
        3.2,
        3.15,
        3.13,
        3.12,
        3.12,
        3.1,
        3.1,
        3.1,
        3.1,
        3.1,
        3.1,
        3.1,
        3.1,
        3.1,
        3.1,
        3.1,
        3.1,
        3.1,
    ],
    [
        3.1,
        3.05,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
    ],
]
hcl_call_iter = 0
pH_call_iter = -1

IS_TEST = False
