import csv
import datetime as dt
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
    with open(file_name, mode="w") as open_file:
        data_writer = csv.writer(
            open_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for data in data_to_write:
            data_writer.writerow(data)


def write_json(file_name, data):
    """
    Write to json
    :param file_name: file path to write to
    :param data: dictionary data to dump to json format
    """
    with open(file_name, "w") as outfile:
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
        constants.PH_REF_VOLTAGE = data["pH"]["ref_voltage"]
        constants.PH_REF_PH = data["pH"]["ref_pH"]
        constants.TEMPERATURE_REF_RESISTANCE = data["temperature"]["ref_resistance"]
        constants.TEMPERATURE_NOMINAL_RESISTANCE = data["temperature"]["nominal_resistance"]
        constants.volume_in_pump = data["vol_pump"]
    else:
        save_calibration_data()


def save_calibration_data():
    """Saves calibration data to json file"""
    calibration_data = constants.calibration_data_format
    calibration_data["pH"]["ref_voltage"] = constants.PH_REF_VOLTAGE
    calibration_data["pH"]["ref_pH"] = constants.PH_REF_PH
    calibration_data["temperature"]["ref_resistance"] = constants.TEMPERATURE_REF_RESISTANCE
    calibration_data["temperature"]["nominal_resistance"] = constants.TEMPERATURE_NOMINAL_RESISTANCE
    calibration_data["vol_pump"] = constants.volume_in_pump
    write_json(constants.CALIBRATION_FILENAME, calibration_data)


def calculate_expected_resistance(temperature):
    """
    Calculates the expected resistance. Used for calibrating temperature probe.
    https://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf
    :param temperature: temperature reading
    :return: expected probe resistance for temperature reading
    """
    A = 0.0039083
    B = -0.000000578
    C = -0.000000000004183

    if temperature >= 0:
        return constants.TEMPERATURE_NOMINAL_RESISTANCE * (1 + A * temperature + B * temperature ** 2)

    # for temperatures below 0 celsius
    return constants.TEMPERATURE_NOMINAL_RESISTANCE * (
        1 + A * temperature + B * temperature ** 2 + C * (temperature - 100) * temperature ** 3
    )


def reset_calibration():
    """Reset calibration settings to default"""
    constants.TEMPERATURE_REF_RESISTANCE = constants.DEFAULT_TEMPERATURE_REF_RESISTANCE
    constants.TEMPERATURE_NOMINAL_RESISTANCE = constants.DEFAULT_TEMPERATURE_NOMINAL_RESISTANCE
    constants.PH_REF_VOLTAGE = constants.DEFAULT_PH_REF_VOLTAGE
    constants.PH_REF_PH = constants.DEFAULT_PH_REF_PH


# pH
def calculate_pH(voltage, temperature):
    """
    Calculates pH value from pH probe voltage. The pH probes read values of V, so to get the actual pH value, V needs
    to be converted.
    :param voltage: voltage reading from pH probe
    :param temperature: temperature of solution
    :return: actual pH value in units of pH
    """
    temperature_k = temperature + constants.CELSIUS_TO_KELVIN
    ref_voltage = constants.PH_REF_VOLTAGE
    ref_pH = constants.PH_REF_PH
    return ref_pH + (ref_voltage - voltage) / (
        constants.UNIVERSAL_GAS_CONST * temperature_k * math.log(10) / constants.FARADAY_CONST
    )


# titration
def calculate_mean(values):
    """
    Calculates mean of given values
    :param values: values to calculate mean of
    :return: mean of values
    """
    return sum(values) / len(values)


def std_deviation(values):
    """
    Calculates sample std deviation of values
    :param values: values to calculate std deviation of
    :return: std deviation of values
    """
    mean = calculate_mean(values)
    running_sum = 0
    for val in values:
        running_sum += (val - mean) ** 2
    return math.sqrt(running_sum / (len(values) - 1))


def write_titration_data(data):
    """
    Writes titration data to csv
    Data in form of ('temperature', 'pH', 'pH volts', 'solution volume')
    :param data: titration data to write out
    """
    file_name = (
        constants.DATA_PATH
        + dt.datetime.strftime(dt.datetime.now(), "%m-%d-%Y %H_%M_%S_%f")
        + ".csv"
    )
    _write_csv(file_name, data)


# pump
def determine_pump_cycles(volume_to_add):
    """
    Determines the number of cycles to move given volume
    :param volume_to_add: amount of volume to add in mL
    :return: number of cycles
    """
    if volume_to_add in constants.NUM_CYCLES:
        return constants.NUM_CYCLES[volume_to_add]
    if volume_to_add > constants.MAX_PUMP_CAPACITY:
        return 0
    pump_cycles = constants.CYCLES_VOLUME_RATIO * volume_to_add
    # NOTE rounds down
    return int(pump_cycles)


# alkalinity
def determine_total_alkalinity(
    S=35,
    temperature=25,
    C=0.1,
    d=1,
    pHTris=None,
    ETris=None,
    weight=None,
    E=None,
    volume=None,
    csv_file=None,
):
    """Calculates the total alkalinity of the solution"""
    pass


# testing
if __name__ == "__main__":
    # print("Expected res = ", calculate_expected_resistance(0))
    while True:
        option = input("1 - Save Calibration data\n2 - Write csv")
        if option == "1":
            save_calibration_data()
            setup_calibration()
        if option == "2":
            _write_csv("test_data", [(1, 2, 3), (4, 5, 6)])
