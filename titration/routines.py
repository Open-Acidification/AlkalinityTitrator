# Code for running the different routines
import interfaces
import constants
import time


def run_routine(selection):
    """Runs routine based on input"""
    if selection == '1':
        titration()
    elif selection == '2':
        calibration()
    elif selection == '3':
        edit_settings()
    elif selection == '4':
        _test_temp()
    elif selection == '5':
        return -1


def _test_temp():
    for i in range(10):
        temp, res = interfaces.read_temperature()
        print("Temperature: {0:0.3f}C".format(temp))
        print("Resistance: {0:0.3f}C".format(res))
        print("Raw resistance: {}".format(res))
        time.sleep(1)


def calibration():
    """Routine for letting the user pick the sensor to calibrate"""
    interfaces.display_list(constants.SENSOR_OPTIONS)
    sensor_selection = interfaces.read_user_input(['1', '2'])
    if sensor_selection == '1':
        _calibrate_pH()
    elif sensor_selection == '2':
        _calibrate_temperature()


def _calibrate_pH():
    """Routine for calibrating pH sensor"""
    # get first buffer pH
    interfaces.lcd_out('Enter buffer pH')
    actual_buffer_pH1 = float(interfaces.read_user_input())
    # TODO wait until user hits another key to stop reading pH and use the value of pH on key press?
    interfaces.lcd_out('Lower sensor into buffer, and press enter to record value')
    input()  # to make the program wait indefinitely for the user to press enter
    measured_buffer_pH1 = float(interfaces.read_raw_pH()[0])
    interfaces.lcd_out("Recorded pH: {}".format(measured_buffer_pH1))

    # get second buffer pH
    interfaces.lcd_out('Enter second buffer pH')
    actual_buffer_pH2 = float(interfaces.read_user_input())
    # TODO wait until user hits another key to stop reading pH and use the value of pH on key press?
    interfaces.lcd_out('Lower sensor into buffer, and press enter to record value')
    input()  # to make the program wait indefinitely for the user to press enter
    measured_buffer_pH2 = float(interfaces.read_raw_pH()[0])
    interfaces.lcd_out("Recorded pH: {}".format(measured_buffer_pH2))

    # set calibration constants
    constants.calibrated_pH['measured'][0] = min(measured_buffer_pH1, measured_buffer_pH2)
    constants.calibrated_pH['measured'][1] = max(measured_buffer_pH1, measured_buffer_pH2)
    constants.calibrated_pH['actual'][0] = min(actual_buffer_pH1, actual_buffer_pH2)
    constants.calibrated_pH['actual'][1] = max(actual_buffer_pH1, actual_buffer_pH2)
    constants.calibrated_pH['slope'] = float((constants.calibrated_pH['actual'][1] -
                                              constants.calibrated_pH['actual'][0]) /
                                             (constants.calibrated_pH['measured'][1] -
                                              constants.calibrated_pH['measured'][0]))
    # return measured_buffer_pH1, measured_buffer_pH2, actual_buffer_pH1, actual_buffer_pH2


def _calibrate_temperature():
    """Routine for calibrating temperature sensor"""
    # TODO wait until user hits another key to stop reading pH and use the value of pH on key press?
    interfaces.lcd_out('Lower temperature probe into sufficiently cooled water; hit enter when done')
    input()  # to make the program wait indefinitely for the user to press enter

    temperature, resistance = interfaces.read_temperature()
    interfaces.lcd_out("Recorded temp: {0:0.3f}".format(temperature))
    diff = 1000.0 - resistance
    new_resistance = 4300.0 + diff
    constants.calibrated_ref_resistor_value = float(new_resistance)
    # reinitialize sensors with calibrated values
    print(new_resistance)
    interfaces.setup_interfaces()


def titration(pH_target, solution_increment_amount):
    '''Incrementally adds HCl depending on the input parameters, until target pH is reached
    '''
    # NOTE If increment value is 20, don't want to add that again to get it close to 3.5...

    # Current pH level; calculated from pH monitor readings
    pH_old = interfaces.read_pH()

    # how many iterations should the pH value be close before breaking?
    while True:
        pH_new = interfaces.read_pH()
        temp_reading = interfaces.read_temperature()
        # measure temp from GPIO
        # measure pH from GPIO
        
        # make sure temperature within correct bounds; global value for all titrations
        if (temp_reading - constants.TARGET_TEMP > constants.TEMPERATURE_ACCURACY):
            print("TEMPERATURE ERROR MESSAGE")
            break
            # Does this invalidate experiment? If so, break out
            # Log error and alert user; write last data to file

        # ensure pH hasn't changed that much since last reading (might not be robust enough)
        if ((pH_new - pH_old) < constants.STABILIZATION_CONSTANT):
            if (pH_new - pH_target < constants.PH_ACCURACY):
                break
            interfaces.dispense_HCl(solution_increment_amount)
        pH_old = pH_new

        # TODO store temp, pH values or immediately write to file (might be slow)
        # Write to raw data file and (more usable) data file?
        time.sleep(constants.SLEEP_TIME)

    # TODO add de-gas time?

    # while (current_pH - constants.TARGET_PH) > constants.PH_ACCURACY:
    #     # TODO
    #     interfaces.dispense_HCl(0.05)
    #     # TODO measure new pH level; wait until readings have settled
    #     current_pH = new_pH
    #     # TODO write out data to csv file


def edit_settings():
    pass
