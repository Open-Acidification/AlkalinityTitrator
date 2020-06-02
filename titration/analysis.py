import datetime as dt
import csv
import json
import math
import constants


# data in/out
def _write_csv(file_name, data_to_write):
    """
    Helper function for writing out to csv
    :param file_name: file path to write to
    :param data_to_write: data to write; expects an iterable
    """
    with open(file_name, mode='w') as open_file:
        data_writer = csv.writer(open_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for data in data_to_write:
            data_writer.writerow(data)


def write_json(file_name, data):
    """
    Write to json
    :param file_name: file path to write to
    :param data: dictionary data to dump to json format
    """
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def _read_json(file_name):
    """
    Reads data from json file
    :param file_name: file path to write to
    :return: dictionary with data from json file
    """
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
        # constants.PH_SLOPE = data['pH']['slope']
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
    # calibration_data['pH']['slope'] = constants.PH_SLOPE
    calibration_data['temp']['ref_resistance'] = constants.TEMP_REF_RESISTANCE
    calibration_data['temp']['nominal_resistance'] = constants.TEMP_NOMINAL_RESISTANCE
    write_json(constants.CALIBRATION_FILENAME, calibration_data)


def calculate_expected_resistance(temp):
    """
    Calculates the expected resistance. Used for calibrating temperature probe.
    https://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf
    :param temp: temperature reading
    :return: expected probe resistance for temperature reading
    """
    A = 0.0039083
    B = -0.000000578
    C = -0.000000000004183

    if temp >= 0:
        return constants.TEMP_NOMINAL_RESISTANCE * (1 + A * temp + B * temp ** 2)

    # for temps below 0 celsius
    return constants.TEMP_NOMINAL_RESISTANCE * (1 + A * temp + B * temp ** 2 + C * (temp - 100) * temp ** 3)


def reset_calibration():
    """Reset calibraiton settings to default"""
    constants.TEMP_REF_RESISTANCE = constants.DEFAULT_TEMP_REF_RESISTANCE
    constants.TEMP_NOMINAL_RESISTANCE = constants.DEFAULT_TEMP_NOMINAL_RESISTANCE = 1000.0
    # constants.PH_SLOPE = constants.DEFAULT_PH_SLOPE = 59
    constants.PH_REF_VOLTAGE = constants.DEFAULT_PH_REF_VOLTAGE = 200
    constants.PH_REF_PH = constants.DEFAULT_PH_REF_PH = 7


# pH
def calculate_pH(voltage, temp):
    """
    Calculates pH value from pH probe voltage. The pH probes read values of mV, so to get the actual pH value, mV needs
    to be converted.
    :param voltage: voltage reading from pH probe
    :param temp: temperature of solution
    :return: actual pH value in units of pH
    """
    temp_k = temp + constants.CELSIUS_TO_KELVIN
    ref_voltage = constants.PH_REF_VOLTAGE
    ref_pH = constants.PH_REF_PH
    return ref_pH + (ref_voltage/1000 - voltage/1000) / \
           (constants.UNIVERSAL_GAS_CONST * temp_k * math.log10(10)/constants.FARADAY_CONST)


# titration
def calculate_mean(values):
    """
    Calculates mean of given values
    :param values: values to calculate mean of
    :return: mean of values
    """
    return sum(values)/len(values)


def std_deviation(values):
    """
    Calculates sample std deviation of values
    :param values: values to calculate std deviation of
    :return: std deviation of values
    """
    mean = calculate_mean(values)
    running_sum = 0
    for val in values:
        running_sum += (val - mean)**2
    return math.sqrt(running_sum/(len(values)-1))


def write_titration_data(data):
    """
    Writes titration data to csv
    Data in form of ('temperature', 'pH', 'pH volts', 'solution volume')
    :param data: titration data to write out
    """
    file_name = constants.DATA_PATH + dt.datetime.strftime(dt.datetime.now(), '%m-%d-%Y %H:%M:%S:%f') + '.csv'
    _write_csv(file_name, data)


# alkalinity
def determine_total_alkalinity(S=35, temp=25, C=0.1, d=1, pHTris=None, ETris=None, weight=None, E=None, volume=None, csv_file=None):
    """Calculates the total alkalinity of the solution"""
    pass


# testing
if __name__ == "__main__":
    # print("Expected res = ", calculate_expected_resistance(0))
    write_json('calibration_data.json')
