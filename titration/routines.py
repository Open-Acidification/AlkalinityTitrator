# Code for running the different routines


def calibration():
    pass


def titrate(pH_target, solution_increment_amount):
    '''Incrementally adds HCl depending on the input parameters, until target pH is reached
    '''
    # NOTE If increment value is 20, don't want to add that again to get it close to 3.5...

    # Current pH level; calculated from pH monitor readings
    pH_old = read_pH()

    # how many iterations should the pH value be close before breaking?
    while True:
        pH_new = read_pH()
        temp_reading = read_temperature()
        # measure temp from GPIO
        # measure pH from GPIO
        
        # make sure temperature within correct bounds; global value for all titrations
        if (temp_reading - TARGET_TEMP > TEMPERATURE_ACCURACY):
            print("TEMPERATURE ERROR MESSAGE")
            break
            # Does this invalidate experiment? If so, break out
            # Log error and alert user; write last data to file

        # ensure pH hasn't changed that much since last reading (might not be robust enough)
        if ((pH_new - pH_old) < STABILIZATION_CONSTANT):
            if (pH_new - pH_target < PH_ACCURACY):
                break
            dispense_HCl(solution_increment_amount)
        pH_old = pH_new

        # TODO store temp, pH values or immediately write to file (might be slow)
        # Write to raw data file and (more usable) data file?

        sleep(SLEEPTIME)

    # TODO add degas time?

    while (current_pH - TARGET_PH) > PH_ACCURACY:
        # TODO 
        dispense_HCl(0.05)
        # TODO measure new pH level; wait until readings have settled
        current_pH = new_pH
        # TODO write out data to csv file


def settings():
    pass
