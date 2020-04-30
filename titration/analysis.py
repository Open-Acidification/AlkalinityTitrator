# Data handling
# calculate linear fits for calibration routine
# Query and save data
# Format data for output
import csv
import json
from datetime import datetime
import constants

DATA_PATH = 'data/'

# data in/out
def write_csv(data_to_write):
    file_name = datetime.strftime(datetime.now(), '%m-%d-%Y %H:%M:%S:%f') + '.csv'
    with open(file_name, mode='w') as open_file:
        data_writer = csv.writer(open_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # TODO convert data_to_write to csv


def write_json(file_name, data):
    """Simple function to write to json"""
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def read_json(file_name):
    """Reads calibration data"""
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data


# calibration
def setup_calibration():
    """Sets up cailbration constants"""
    state_data = read_json(DATA_PATH + 'calibration_data.json')
    constants.calibrated_pH = state_data


def calculate_expected_resistance(temp):
    """Calculates the expected resistance
    https://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf"""
    A = 0.0039083
    B = -0.000000578
    C = -0.000000000004183

    if temp >= 0:
        return constants.nominal_resistance * (1 + A * temp + B * temp ** 2)

    # for temps below 0 celsius
    return constants.nominal_resistance * (1 + A * temp + B * temp ** 2 + C * (temp - 100) * temp ** 3)


# titration
def calculate_mean(values):
    pass


if __name__ == "__main__":
    print("Expected res = ", calculate_expected_resistance(0))

