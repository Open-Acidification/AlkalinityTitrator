"""
The file to hold the titrator constants
"""

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
    KEY_5: "Demo Mode",
    KEY_6: "Exit",
    KEY_STAR: "Page 1",
}

SENSOR_OPTIONS = {KEY_1: "pH", KEY_2: "Temperature"}

# Small times steps (s) in the delay function
DELAY_STEP = 0.0001

# LCD Device Constants
LCD_WIDTH = 20  # Maximum characters per line
LCD_HEIGHT = 4

# for pH calibration constants
calibration_data_format = {
    "pH": {"ref_voltage": 200, "ref_pH": 7},
    "temperature": {"ref_resistance": 4300.0, "nominal_resistance": 1000.0},
    "vol_pump": 0,
}

CALIBRATION_FILENAME = "data/calibration.json"
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

IS_TEST = False
