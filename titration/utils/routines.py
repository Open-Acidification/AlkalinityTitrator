import numpy as np  # debugging/testing

from titration.utils import analysis, constants, interfaces

ROUTINE_OPTIONS = {
    1: "Run titration",
    2: "Calibrate sensors",
    3: "Prime Pump",
    4: "Update settings",
    5: "Test Mode",
    6: "Exit",
}


def run_routine(selection):
    """
    Selects which routine to run
    :param selection: user input used to determine which routine to run
    """
    if selection == "1" or selection == constants.KEY_1:
        # run titration
        total_alkalinity_titration()
    elif selection == "2" or selection == constants.KEY_2:
        # calibrate sensors
        calibration()
    elif selection == "3" or selection == constants.KEY_3:
        # prime pump
        prime_pump()
    elif selection == "4" or selection == constants.KEY_4:
        # edit settings
        edit_settings()
    elif selection == "5" or selection == constants.KEY_5:
        # testing mode
        test_mode()
    else:
        # exit
        pass


def test_mode():
    """Function for running specific tests for the program"""
    page = 1
    user_choice = None
    while True:
        # Swap page display if user chooses *
        if user_choice == constants.KEY_STAR:
            if page == 1:
                page = 2
            else:
                page = 1
        # Display the proper page
        if page == 1:
            interfaces.lcd.display_list(constants.ROUTINE_OPTIONS_1)
        else:
            interfaces.lcd.display_list(constants.ROUTINE_OPTIONS_2)

        user_choice = interfaces.read_user_input()

        if user_choice == "6" or user_choice == constants.KEY_6:
            break
        else:
            test_mode_selection(user_choice)


def test_mode_selection(user_choice):
    if user_choice == "1" or user_choice == constants.KEY_1:
        test_mode_read_values()

    elif user_choice == "2" or user_choice == constants.KEY_2:
        test_mode_pump()

    elif user_choice == "3" or user_choice == constants.KEY_3:
        test_mode_set_volume()

    elif user_choice == "4" or user_choice == constants.KEY_4:
        test_mode_toggle_test_mode()

    elif user_choice == "5" or user_choice == constants.KEY_5:
        test_mode_read_volume()


def test_mode_read_values(numVals=60, timestep=0.5):
    numVals = numVals
    timestep = timestep
    timeVals = np.zeros(numVals)
    tempVals = np.zeros(numVals)
    resVals = np.zeros(numVals)
    pHVals = np.zeros(numVals)
    voltVals = np.zeros(numVals)

    for i in range(numVals):
        temp, res = interfaces.temperature_sensor.read_temperature()
        pH_reading, pH_volts = interfaces.read_pH()
        interfaces.lcd.print("Temp: {0:>4.3f} C".format(temp), line=1)
        interfaces.lcd.print("Res:  {0:>4.3f} Ohms".format(res), line=2)
        interfaces.lcd.print("pH:   {0:>4.5f} pH".format(pH_reading), line=3)
        interfaces.lcd.print("pH V: {0:>3.4f} mV".format(pH_volts * 1000), line=4)
        interfaces.lcd.print("Reading: {}".format(i), line=1)
        timeVals[i] = timestep * i
        tempVals[i] = temp
        resVals[i] = res
        pHVals[i] = pH_reading
        voltVals[i] = pH_volts
        interfaces.delay(timestep)


def test_mode_pump():
    p_volume = interfaces.read_user_value("Volume: ")

    while True:
        p_direction = interfaces.read_user_value("In/Out (0/1):")
        if p_direction == 0 or p_direction == 1:
            interfaces.lcd.clear()
            interfaces.pump.pump_volume(float(p_volume), int(p_direction))
            break


def test_mode_set_volume():
    new_volume = interfaces.read_user_value("Volume in pump: ")
    interfaces.pump.set_volume_in_pump(new_volume)


def test_mode_toggle_test_mode():
    constants.IS_TEST = not constants.IS_TEST
    interfaces.lcd.clear()
    interfaces.lcd.print("Testing: {}".format(constants.IS_TEST), line=1)
    interfaces.lcd.print("Press any to cont.", line=3)
    interfaces.read_user_input()


def test_mode_read_volume():
    interfaces.lcd.clear()
    interfaces.lcd.print("Pump Vol: ", line=1)
    interfaces.lcd.print(
        "{0:1.2f}".format(constants.volume_in_pump),
        style=constants.LCD_CENT_JUST,
        line=2,
    )
    interfaces.lcd.print("Press any to cont.", line=3)
    interfaces.read_user_input()


def _test_temperature():
    """Tests the temperature probe"""
    for i in range(5):
        temperature, res = interfaces.temperature_sensor.read_temperature()
        interfaces.lcd.print("Temperature: {0:0.3f}C".format(temperature), 1)
        interfaces.lcd.print("Res: {0:0.3f} Ohms".format(res), 2)
        interfaces.delay(0.5)


def calibration():
    """Routine for letting the user pick the sensor to calibrate. Call another routine to calibrate the sensor"""
    interfaces.lcd.display_list(constants.SENSOR_OPTIONS)
    sensor_selection = interfaces.read_user_input()
    if sensor_selection == "1" or sensor_selection == constants.KEY_1:
        _calibrate_pH()
    elif sensor_selection == "2" or sensor_selection == constants.KEY_2:
        _calibrate_temperature()
    analysis.save_calibration_data()


def _calibrate_pH():
    """Routine for calibrating pH sensor."""
    # get first buffer pH
    buffer1_actual_pH = interfaces.read_user_value("Enter buffer pH:")
    interfaces.lcd.print("Put sensor in buffer", style=constants.LCD_CENT_JUST, line=1)
    interfaces.lcd.print("", line=2)
    interfaces.lcd.print("Press any button", style=constants.LCD_CENT_JUST, line=3)
    interfaces.lcd.print("to record value", style=constants.LCD_CENT_JUST, line=4)
    # Waits for user to press enter
    interfaces.read_user_input()
    buffer1_measured_volts = float(interfaces.ph_sensor.read_raw_pH())
    interfaces.lcd.clear()
    interfaces.lcd.print("Recorded pH and volts:", line=1)
    interfaces.lcd.print(
        "{0:>2.5f} pH, {1:>3.4f} V".format(buffer1_actual_pH, buffer1_measured_volts),
        line=2,
    )
    interfaces.lcd.print("Press any button", style=constants.LCD_CENT_JUST, line=3)
    interfaces.lcd.print("to continue", style=constants.LCD_CENT_JUST, line=4)
    interfaces.read_user_input()

    # set calibration constants
    constants.PH_REF_VOLTAGE = buffer1_measured_volts
    constants.PH_REF_PH = buffer1_actual_pH


def _calibrate_temperature():
    """Routine for calibrating the temperature probe."""
    expected_temperature = interfaces.read_user_value("Ref solution temperature?")
    interfaces.lcd.print("Put probe in sol", style=constants.LCD_CENT_JUST, line=1)
    interfaces.lcd.print("", line=2)
    interfaces.lcd.print("Press 1 to", style=constants.LCD_CENT_JUST, line=3)
    interfaces.lcd.print("record value", style=constants.LCD_CENT_JUST, line=4)
    # Waits for user to press enter
    interfaces.read_user_input()
    expected_resistance = analysis.calculate_expected_resistance(expected_temperature)
    (
        actual_temperature,
        actual_resistance,
    ) = interfaces.temperature_sensor.read_temperature()
    interfaces.lcd.clear()
    interfaces.lcd.print(
        "Recorded temperature: {0:0.3f}".format(actual_temperature), line=1
    )
    diff = expected_resistance - actual_resistance
    new_ref_resistance = (
        constants.TEMPERATURE_REF_RESISTANCE
        + diff * constants.TEMPERATURE_REF_RESISTANCE / expected_resistance
    )
    constants.TEMPERATURE_REF_RESISTANCE = float(new_ref_resistance)

    # reinitialize sensors with calibrated values
    interfaces.lcd.print("{}".format(new_ref_resistance), line=2)


def total_alkalinity_titration():
    """Runs through the full titration routine to find total alkalinity"""
    # pull in 1 ml of solution into pump for use in titration
    if constants.volume_in_pump < 1.0:
        p_volume = 1.0 - constants.volume_in_pump
        interfaces.pump.pump_volume(float(p_volume), 0)
    # data object to hold recorded data
    data = [
        (
            "temperature",
            "pH V",
            "solution volume",
            "weight",
            "salinity",
            "Buffer pH",
            "Buffer pH V",
        )
    ]

    # query user for initial solution weight
    initial_weight = interfaces.read_user_value("Sol. weight (g):")
    salinity = interfaces.read_user_value("Sol. salinity (ppt):")
    buffer_ph = constants.PH_REF_PH
    buffer_v = constants.PH_REF_VOLTAGE

    interfaces.lcd.clear()
    interfaces.lcd.print("Calibrate pH probe?", line=1)
    interfaces.lcd.print("Yes: 1", line=2)
    interfaces.lcd.print("No (use old): 0", line=3)
    interfaces.lcd.print(
        "{0:>2.3f} pH: {1:>2.4f} V".format(buffer_ph, buffer_v), line=4
    )
    selection = interfaces.read_user_input()
    if selection == constants.KEY_1 or selection == "1":
        _calibrate_pH()

    analysis.save_calibration_data()

    data.append((None, None, None, initial_weight, salinity, buffer_ph, buffer_v))

    # while not initial_weight.replace('.', '').isdigit():
    # interfaces.lcd.print("Please enter a numeric value.", console=True)
    # initial_weight = interfaces.read_user_input()

    # initial titration (bring solution close to 3.5)
    # todo set stir speed slow
    total_sol = 0
    interfaces.lcd.print("Bring pH to 3.5:", line=1)
    interfaces.lcd.print("Manual: 1", line=2)
    interfaces.lcd.print("Automatic: 2", line=3)
    interfaces.lcd.print("Stir speed: slow", line=4)
    interfaces.stir_controller.motor_speed_slow()
    user_choice = interfaces.read_user_input()

    # wait until solution is up to temperature
    interfaces.temperature_controller.activate()
    interfaces.lcd.clear()
    interfaces.lcd.print("Heating to 30 C...", line=1)
    interfaces.lcd.print("Please wait...", style=constants.LCD_CENT_JUST, line=3)
    if user_choice == "1" or user_choice == constants.KEY_1:
        interfaces.lcd.print("MANUAL SELECTED", style=constants.LCD_CENT_JUST, line=4)
    else:
        interfaces.lcd.print("AUTO SELECTED", style=constants.LCD_CENT_JUST, line=4)
    while not interfaces.temperature_controller.at_temperature():
        interfaces.temperature_controller.update()
        temperature = interfaces.temperature_controller.get_last_temperature()
        interfaces.lcd.print(
            "Temp: {0:>4.3f} C".format(temperature),
            style=constants.LCD_CENT_JUST,
            line=2,
        )

    if user_choice == "1" or user_choice == constants.KEY_1:
        # Manual
        while user_choice == "1" or user_choice == constants.KEY_1:
            p_volume = interfaces.read_user_value("Volume: ")
            interfaces.lcd.clear()
            interfaces.lcd.print("Direction (0/1): ", line=1)
            p_direction = interfaces.read_user_input()
            p_volume = float(p_volume)
            p_direction = int(p_direction)
            if p_direction == 1:
                total_sol += p_volume
            if p_direction == 0 or p_direction == 1:
                interfaces.pump.pump_volume(p_volume, p_direction)
            current_pH = wait_pH_stable(total_sol, data)
            interfaces.lcd.print("Current pH: {0:>4.5f}".format(current_pH), line=1)
            interfaces.lcd.print("Add more HCl?", line=2)
            interfaces.lcd.print("(0 - No, 1 - Yes)", line=3)
            interfaces.lcd.print("", line=4)

            user_choice = interfaces.read_user_input()
        interfaces.lcd.clear()
        interfaces.lcd.print("Current pH: {0:>4.5f}".format(current_pH), line=1)
        interfaces.lcd.print("Degas?", 1)
        interfaces.lcd.print("(0 - No, 1 - Yes)", line=2)
        user_choice = interfaces.read_user_input()
        if user_choice == constants.KEY_1:
            degas_time = interfaces.read_user_value("Degas time (s):")
            degas(degas_time)

    else:
        # Automatic
        total_sol = titration(
            constants.TARGET_PH_INIT,
            constants.INCREMENT_AMOUNT_INIT,
            data,
            0,
        )
        total_sol = titration(
            constants.TARGET_PH_MID,
            constants.INCREMENT_AMOUNT_MID,
            data,
            total_sol,
            600,
        )

    # 3.5 -> 3.0
    titration(
        constants.TARGET_PH_FINAL, constants.INCREMENT_AMOUNT_FINAL, data, total_sol
    )
    # save data to csv
    analysis.write_titration_data(data)

    # save the current syringe position
    analysis.save_calibration_data()
    interfaces.stir_controller.motor_stop()
    interfaces.temperature_controller.deactivate()


def titration(
    pH_target, solution_increment_amount, data, total_sol_added, degas_time=0
):
    """
    Incrementally adds HCl depending on the input parameters, until target pH is reached
    :param pH_target: target pH for the titration
    :param solution_increment_amount: amount of HCl to add to solution. Units of mL
    :param data: list of recorded temperature, pH, and solution volume data so far
    :param total_sol_added: total amount of HCl added to the solution so far
    :param degas_time: optional parameter defining the de-gas time for the solution after the target pH has been reached
    :return: total solution added so far
    """
    interfaces.lcd.print(
        "Titrating to {} pH".format(str(pH_target)),
        style=constants.LCD_CENT_JUST,
        line=4,
    )
    # total HCl added
    total_sol = total_sol_added

    current_pH = wait_pH_stable(total_sol, data)

    while current_pH - pH_target > constants.PH_ACCURACY:
        interfaces.pump.pump_volume(solution_increment_amount, 1)
        if constants.volume_in_pump < 0.05:
            # pump in 1 mL
            interfaces.pump.pump_volume(1.0, 0)
        total_sol += solution_increment_amount

        # TESTING SETTLING
        interfaces.lcd.print("Mixing...", style=constants.LCD_CENT_JUST, line=4)
        interfaces.delay(10)  # allow it to mix before taking measurements

        current_pH = wait_pH_stable(total_sol, data)
        interfaces.temperature_controller.update()

    interfaces.lcd.clear()
    interfaces.lcd.print("pH value {} reached".format(current_pH), line=1)
    if degas_time > 0:
        degas(degas_time)
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
        temperature_reading = interfaces.temperature_sensor.read_temperature()[0]
        interfaces.lcd.print("pH:   {0:>4.5f} pH".format(pH_reading), line=1)
        interfaces.lcd.print("pH V: {0:>3.4f} mV".format(pH_volts * 1000), line=2)
        interfaces.lcd.print("Temp: {0:>4.3f} C".format(temperature_reading), line=3)

        pH_values[pH_list_counter] = pH_reading

        if pH_list_counter == 9:
            valid_num_values_tested = True

        # Check that the temperature of the solution is within bounds
        if (
            abs(temperature_reading - constants.TARGET_TEMPERATURE)
            > constants.TEMPERATURE_ACCURACY
        ):
            # interfaces.lcd.print("TEMPERATURE OUT OF BOUNDS")
            # TODO output to error log
            pass

        # Record data point (temperature, pH volts, total HCl)
        data.append((temperature_reading, pH_volts, total_sol, None, None, None, None))
        pH_list_counter = 0 if pH_list_counter >= 9 else pH_list_counter + 1

        if (
            valid_num_values_tested
            and analysis.std_deviation(pH_values) < constants.TARGET_STD_DEVIATION
        ):
            return pH_reading

        interfaces.delay(constants.TITRATION_WAIT_TIME)


def degas(seconds):
    interfaces.lcd.clear()
    interfaces.lcd.print("Degassing {0:.0f}".format(seconds), line=1)
    interfaces.lcd.print("seconds", line=2)
    interfaces.stir_controller.motor_speed_fast()
    interfaces.delay(seconds, countdown=True)
    interfaces.stir_controller.motor_speed_slow()


# TODO FIX LCD LINES
def edit_settings():
    """Resets calibration constants to default"""
    interfaces.lcd.print("Reset calibration", line=1)
    interfaces.lcd.print("settings to default?", line=2)
    interfaces.lcd.print("1: Yes", line=3)
    interfaces.lcd.print("2: No", line=4)
    selection = interfaces.read_user_input()
    if selection != "n" or selection != "N":
        analysis.reset_calibration()
        analysis.save_calibration_data()
        interfaces.lcd.clear()
        interfaces.lcd.print("Default constants restored", 1)
        interfaces.lcd.print("Press any to cont.", 3)
        interfaces.read_user_input()

    interfaces.lcd.print("Set volume in pump? (Y/n)", 1)
    selection = interfaces.read_user_input()
    if selection != "n" or selection != "N":
        vol_in_pump = interfaces.read_user_value("Volume in pump: ")
        constants.volume_in_pump = vol_in_pump
        analysis.save_calibration_data()
        interfaces.lcd.print("Volume in pump set", 1)
        interfaces.lcd.print("Press any to cont.", 3)
        interfaces.read_user_input()


def prime_pump():
    """
    Primes pump by drawing in and pushing out solution.
    Depends on limit switches installed
    """
    interfaces.lcd.print("How many pumps?", 1)
    selection = interfaces.read_user_input()
    sel = int(selection)
    while sel > 0:
        while sel > 0:
            interfaces.pump.pump_volume(1, 0)
            interfaces.pump.pump_volume(1, 1)
            sel = sel - 1
        interfaces.lcd.print("How many more?", 1)
        selection = interfaces.read_user_input()
        sel = int(selection)


def auto_home():
    """
    Homes syringe to 0 mL upon calling.
    Runs on startup in titration.run(), depends on limit switches
    """
    interfaces.pump.pump_volume(1, 1)
