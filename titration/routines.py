import interfaces
import constants
import analysis
import time

ROUTINE_OPTIONS = {
    1: 'Run titration',
    2: 'Calibrate sensors',
    3: 'Prime Pump',
    4: 'Update settings',
    5: 'Test Mode',
    6: 'Exit'
}


def run_routine(selection):
    """
    Selects which routine to run
    :param selection: user input used to determine which routine to run
    """
    if selection == '1':
        # run titration
        total_alkalinity_titration()
    elif selection == '2':
        # calibrate sensors
        calibration()
    elif selection == '3':
        # prime pump
        prime_pump()
    elif selection == '4':
        # edit settings
        edit_settings()
    elif selection == '5':
        # testing mode
        constants.IS_TEST = not constants.IS_TEST
        interfaces.lcd_out("Testing: {}".format(constants.IS_TEST))
    else:
        # exit
        pass


def _test_temp():
    """Tests the temperature probe"""
    for i in range(5):
        temp, res = interfaces.read_temperature()
        print("Temperature: {0:0.3f}C".format(temp))
        print("Resistance: {0:0.3f}C".format(res))
        time.sleep(0.5)


def calibration():
    """Routine for letting the user pick the sensor to calibrate. Call another routine to calibrate the sensor"""
    interfaces.display_list(constants.SENSOR_OPTIONS)
    sensor_selection = interfaces.read_user_input(['1', '2'])
    if sensor_selection == '1':
        _calibrate_pH()
    elif sensor_selection == '2':
        _calibrate_temperature()
    analysis.save_calibration_data()


def _calibrate_pH():
    """Routine for calibrating pH sensor."""
    # get first buffer pH
    interfaces.lcd_out('Enter buffer pH')
    buffer1_actual_pH = float(interfaces.read_user_input())
    interfaces.lcd_out('Lower sensor into buffer, and press enter to record value')
    # Waits for user to press enter
    input()
    buffer1_measured_volts = float(interfaces.read_raw_pH())
    interfaces.lcd_out("Recorded volts for pH {}: {}".format(buffer1_actual_pH, buffer1_measured_volts))

    # set calibration constants
    constants.PH_REF_VOLTAGE = buffer1_measured_volts
    constants.PH_REF_PH = buffer1_actual_pH


def _calibrate_temperature():
    """Routine for calibrating the temperature probe."""
    interfaces.lcd_out("What is temperature of the reference solution?")
    expected_temp = float(input())
    interfaces.lcd_out('Lower temperature probe into reference solution; hit enter when done')
    # Waits for user to press enter
    input()
    expected_resistance = analysis.calculate_expected_resistance(expected_temp)

    actual_temperature, actual_resistance = interfaces.read_temperature()
    interfaces.lcd_out("Recorded temp: {0:0.3f}".format(actual_temperature))
    diff = expected_resistance - actual_resistance
    new_ref_resistance = constants.TEMP_REF_RESISTANCE + diff * constants.TEMP_REF_RESISTANCE / expected_resistance
    constants.TEMP_REF_RESISTANCE = float(new_ref_resistance)
    # reinitialize sensors with calibrated values
    print(new_ref_resistance)
    interfaces.setup_interfaces()


def total_alkalinity_titration():
    """Runs through the full titration routine to find total alkalinity"""
    # pull in 1 ml of solution into pump for use in titration
    interfaces.pump_volume(1, 0)
    # data object to hold recorded data
    data = [('temperature', 'pH mV', 'solution volume')]

    # query user for initial solution weight
    interfaces.lcd_out("Initial solution weight (g): ")
    initial_weight = interfaces.read_user_input()
    while not initial_weight.replace('.', '').isdigit():
        interfaces.lcd_out("Please enter a numeric value.")
        initial_weight = interfaces.read_user_input()

    # initial titration (bring solution close to 3.5)
    # todo set stir speed slow
    total_sol = 0
    interfaces.lcd_out("Stir speed: slow")
    interfaces.lcd_out("Manually or automatically bring pH to 3.5?\n(Manual - 1, Automatic - 2)")
    user_choice = interfaces.read_user_input()

    if user_choice == '1':
        # Manual
        while user_choice == '1':
            p_volume = interfaces.read_user_input("Volume: ")
            p_direction = interfaces.read_user_input("Direction: ")
            if p_direction == '1':
                total_sol += p_volume
            if p_direction == '0' or p_direction == '1':
                interfaces.pump_volume(float(p_volume), int(p_direction))
            current_pH = wait_pH_stable(total_sol, data)
            interfaces.lcd_out("Current pH: {}".format(current_pH))
            interfaces.lcd_out("Continue adding solution? (0 - No, 1 - Yes")
            user_choice = interfaces.read_user_input()
    else:
        # Automatic
        total_sol = titration(constants.INITIAL_TARGET_PH, constants.INCREMENT_AMOUNT, data, 0, 3*60)

    # 3.5 -> 3.0
    # todo set stir speed fast
    interfaces.lcd_out("Stir speed: fast")
    titration(constants.FINAL_TARGET_PH, constants.INCREMENT_AMOUNT, data, total_sol)
    # save data to csv
    analysis.write_titration_data(data)


def titration(pH_target, solution_increment_amount, data, total_sol_added, degas_time=0):
    '''
    Incrementally adds HCl depending on the input parameters, until target pH is reached
    :param pH_target: target pH for the titration
    :param solution_increment_amount: amount of HCl to add to solution. Units of mL
    :param data: list of recorded temperature, pH, and solution volume data so far
    :param total_sol_added: total amount of HCl added to the solution so far
    :param degas_time: optional parameter defining the de-gas time for the solution after the target pH has been reached
    :return: total solution added so far
    '''
    interfaces.lcd_out("Titrating to a pH of " + str(pH_target))
    # total HCl added
    total_sol = total_sol_added

    current_pH = wait_pH_stable(total_sol, data)

    while current_pH - pH_target > constants.PH_ACCURACY:
        interfaces.pump_volume(solution_increment_amount, 1)
        total_sol += solution_increment_amount
        current_pH = wait_pH_stable(total_sol, data)
    interfaces.lcd_out("pH value {} reached".format(current_pH))

    interfaces.lcd_out("Degassing " + str(degas_time) + " seconds...")
    time.sleep(degas_time)
    return total_sol


def wait_pH_stable(total_sol, data):
    """
    Continually polls probes until pH values are stable
    :param total_sol: total amount of HCl added to the solution so far
    :param data: list of recorded temperature, pH, and solution volume data so far
    :return: mean stable pH value of last 10 values
    """
    # keep track of 10 most recent pH values to ensure pH is stable
    pH_values = [0] * 10
    # a counter used for updating values in pH_values
    pH_list_counter = 0
    # flag to ensure at least 10 pH readings have been made before adding solution
    valid_num_values_tested = False

    while True:
        pH_reading, pH_volts = interfaces.read_pH()
        temp_reading = interfaces.read_temperature()[0]
        interfaces.lcd_out("pH: {}".format(pH_reading))
        interfaces.lcd_out("temp: {0:0.3f}C".format(temp_reading))
        pH_values[pH_list_counter] = pH_reading

        if pH_list_counter == 9:
            valid_num_values_tested = True

        # Check that the temperature of the solution is within bounds
        if abs(temp_reading - constants.TARGET_TEMP) > constants.TEMPERATURE_ACCURACY:
            interfaces.lcd_out("TEMPERATURE OUT OF BOUNDS")
            # TODO output to error log

        # Record data point (temp, pH volts, total HCl)
        data.append((temp_reading, pH_volts, total_sol))
        pH_list_counter = 0 if pH_list_counter >= 9 else pH_list_counter + 1

        if valid_num_values_tested and analysis.std_deviation(pH_values) < constants.TARGET_STD_DEVIATION:
            return analysis.calculate_mean(pH_values)

        time.sleep(constants.TITRATION_WAIT_TIME)


def edit_settings():
    """Resets calibration constants to default"""
    interfaces.lcd_out("Reset calibration settings to default? (Y/n)")
    selection = interfaces.read_user_input()
    if selection != 'n' or selection != 'N':
        analysis.reset_calibration()
        analysis.save_calibration_data()
        interfaces.lcd_out("Default constants restored")


def prime_pump():
    """Primes pump by pulling in and pushing out solution"""
    selection = '1'
    while selection == '1':
        p_volume = interfaces.read_user_input("Volume: ")
        interfaces.pump_volume(float(p_volume), 0)
        interfaces.pump_volume(float(p_volume), 1)


    # # draw in solution
    # interfaces.pump_volume(1, 0)
    # # push out solution
    # interfaces.pump_volume(1, 1)
