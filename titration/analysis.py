# Data handling
# calculate linear fits for calibration routine
# Query and save data
# Format data for output
import datetime as dt
import csv
import json
import math
import constants


# data in/out
def _write_csv(file_name, data_to_write):
    """Helper function for writing to csv"""
    with open(file_name, mode='w') as open_file:
        data_writer = csv.writer(open_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for data in data_to_write:
            data_writer.writerow(data)


def write_json(file_name, data):
    """Simple function to write to json"""
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def _read_json(file_name):
    """Reads from json; returns data"""
    try:
        with open(file_name) as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return None


# calibration
def setup_calibration():
    """Sets calibration constants from persistent storage"""
    data = _read_json(constants.CALIBRATION_FILENAME)
    if data:
        constants.PH_SLOPE = data['pH']['slope']
        constants.PH_REF_VOLTAGE = data['pH']['ref_voltage']
        constants.PH_REF_PH = data['pH']['ref_pH']
        constants.TEMP_REF_RESISTANCE = data['temp']['ref_resistance']
        constants.TEMP_NOMINAL_RESISTANCE = data['temp']['nominal_resistance']
    else:
        save_calibration_data()


def save_calibration_data():
    """Saves calibration data to json file"""
    calibration_data = constants.calibration_data_format
    calibration_data['pH']['ref_voltage'] = constants.PH_REF_VOLTAGE
    calibration_data['pH']['ref_pH'] = constants.PH_REF_PH
    calibration_data['pH']['slope'] = constants.PH_SLOPE
    calibration_data['temp']['ref_resistance'] = constants.TEMP_REF_RESISTANCE
    calibration_data['temp']['nominal_resistance'] = constants.TEMP_NOMINAL_RESISTANCE
    write_json(constants.CALIBRATION_FILENAME, calibration_data)


def calculate_expected_resistance(temp):
    """Calculates the expected resistance
    https://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf"""
    A = 0.0039083
    B = -0.000000578
    C = -0.000000000004183

    if temp >= 0:
        return constants.TEMP_NOMINAL_RESISTANCE * (1 + A * temp + B * temp ** 2)

    # for temps below 0 celsius
    return constants.TEMP_NOMINAL_RESISTANCE * (1 + A * temp + B * temp ** 2 + C * (temp - 100) * temp ** 3)


# pH
def calculate_pH(voltage, temp):
    """Calculates pH value from voltage"""
    temp_k = temp + constants.CELSIUS_TO_KELVIN
    ref_voltage = constants.PH_REF_VOLTAGE
    ref_pH = constants.PH_REF_PH
    return ref_pH + (ref_voltage/1000 - voltage/1000)/(constants.UNIVERSAL_GAS_CONST * temp_k * math.log10(10)/constants.FARADAY_CONST)


# titration
def calculate_mean(values):
    """Returns the mean of given values"""
    return sum(values)/len(values)


def std_deviation(values):
    """Returns sample std deviation of values"""
    mean = calculate_mean(values)
    running_sum = 0
    for val in values:
        running_sum += (val - mean)**2
    return math.sqrt(running_sum/(len(values)-1))


def write_titration_data(data):
    """Writes titration data to csv"""
    file_name = constants.DATA_PATH + dt.datetime.strftime(dt.datetime.now(), '%m-%d-%Y %H:%M:%S:%f') + '.csv'
    _write_csv(file_name, data)


# testing
if __name__ == "__main__":
    # print("Expected res = ", calculate_expected_resistance(0))
    write_json('calibration_data.json')
