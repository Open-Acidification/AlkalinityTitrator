from titration.utils.UIState import UIState
from titration.utils import interfaces, constants, analysis
from titration.utils.routines import titration


class RunTitration(UIState.UIState):
    def __init__(self, tc):
        UIState.__init__('RunTitration', tc)
        self.data = [   # data object to hold recorded data
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

    def handleKey(self, key):
        pass

    def name(self):
        return 'RunTitration'

    def loop(self):
        self.total_sol = titration(
            constants.TARGET_PH_INIT,
            constants.INCREMENT_AMOUNT_INIT,
            self.data,
            0,
        )
        self.total_sol = titration(
            constants.TARGET_PH_MID,
            constants.INCREMENT_AMOUNT_MID,
            self.data,
            self.total_sol,
            600,
        )
        titration(
            constants.TARGET_PH_FINAL, constants.INCREMENT_AMOUNT_FINAL, self.data, self.total_sol
        )


    def titration(self,
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
        interfaces.lcd_out(
            "Titrating to {} pH".format(str(pH_target)),
            style=constants.LCD_CENT_JUST,
            line=4,
        )
        # total HCl added
        total_sol = total_sol_added

        current_pH = self.wait_pH_stable(total_sol, data)

        while current_pH - pH_target > constants.PH_ACCURACY:
            interfaces.pump_volume(solution_increment_amount, 1)
            if constants.volume_in_pump < 0.05:
                # pump in 1 mL
                interfaces.pump_volume(1.0, 0)
            total_sol += solution_increment_amount

            # TESTING SETTLING
            interfaces.lcd_out("Mixing...", style=constants.LCD_CENT_JUST, line=4)
            interfaces.delay(10)  # allow it to mix before taking measurements

            current_pH = self.wait_pH_stable(total_sol, data)
            interfaces.temperature_controller.update()

        interfaces.lcd_clear()
        interfaces.lcd_out("pH value {} reached".format(current_pH), line=1)
        if degas_time > 0:
            self.degas(degas_time)
        return total_sol


    def start(self):
        if constants.volume_in_pump < 1.0:
            p_volume = 1.0 - constants.volume_in_pump
            interfaces.pump_volume(float(p_volume), 0)
        initial_weight = interfaces.read_user_value("Sol. weight (g):")
        salinity = interfaces.read_user_value("Sol. salinity (ppt):")
        buffer_ph = constants.PH_REF_PH
        buffer_v = constants.PH_REF_VOLTAGE

        interfaces.lcd_clear()
        interfaces.lcd_out("Calibrate pH probe?", line=1)
        interfaces.lcd_out("Yes: 1", line=2)
        interfaces.lcd_out("No (use old): 0", line=3)
        interfaces.lcd_out("{0:>2.3f} pH: {1:>2.4f} V".format(buffer_ph, buffer_v), line=4)
        selection = interfaces.read_user_input()
        if selection == constants.KEY_1 or selection == "1":
            self._calibrate_pH()

        analysis.save_calibration_data()

        self.data.append((None, None, None, initial_weight, salinity, buffer_ph, buffer_v))

        # initial titration (bring solution close to 3.5)
        # todo set stir speed slow
        total_sol = 0
        interfaces.lcd_out("Bring pH to 3.5:", line=1)
        interfaces.lcd_out("Manual: 1", line=2)
        interfaces.lcd_out("Automatic: 2", line=3)
        interfaces.lcd_out("Stir speed: slow", line=4)
        interfaces.stir_speed_slow()
        user_choice = interfaces.read_user_input()

        # wait until solution is up to temperature
        interfaces.temperature_controller.activate()
        interfaces.lcd_clear()
        interfaces.lcd_out("Heating to 30 C...", line=1)
        interfaces.lcd_out("Please wait...", style=constants.LCD_CENT_JUST, line=3)
        if user_choice == "1" or user_choice == constants.KEY_1:
            interfaces.lcd_out("MANUAL SELECTED", style=constants.LCD_CENT_JUST, line=4)
        else:
            interfaces.lcd_out("AUTO SELECTED", style=constants.LCD_CENT_JUST, line=4)
        while not interfaces.temperature_controller.at_temperature():
            interfaces.temperature_controller.update()
            temperature = interfaces.temperature_controller.get_last_temperature()
            interfaces.lcd_out(
                "Temp: {0:>4.3f} C".format(temperature),
                style=constants.LCD_CENT_JUST,
                line=2,
            )

        if user_choice == "1" or user_choice == constants.KEY_1:
            # Manual
            while user_choice == "1" or user_choice == constants.KEY_1:
                p_volume = interfaces.read_user_value("Volume: ")
                interfaces.lcd_clear()
                interfaces.lcd_out("Direction (0/1): ", line=1)
                p_direction = interfaces.read_user_input()
                p_volume = float(p_volume)
                p_direction = int(p_direction)
                if p_direction == 1:
                    total_sol += p_volume
                if p_direction == 0 or p_direction == 1:
                    interfaces.pump_volume(p_volume, p_direction)
                current_pH = self.wait_pH_stable(total_sol, self.data)
                interfaces.lcd_out("Current pH: {0:>4.5f}".format(current_pH), line=1)
                interfaces.lcd_out("Add more HCl?", line=2)
                interfaces.lcd_out("(0 - No, 1 - Yes)", line=3)
                interfaces.lcd_out("", line=4)

                user_choice = interfaces.read_user_input()
            interfaces.lcd_clear()
            interfaces.lcd_out("Current pH: {0:>4.5f}".format(current_pH), line=1)
            interfaces.lcd_out("Degas?", 1)
            interfaces.lcd_out("(0 - No, 1 - Yes)", line=2)
            user_choice = interfaces.read_user_input()
            if user_choice == constants.KEY_1:
                degas_time = interfaces.read_user_value("Degas time (s):")
                self.degas(degas_time)


    def wait_pH_stable(self, total_sol, data):
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
            temperature_reading = interfaces.read_temperature()[0]
            interfaces.lcd_out("pH:   {0:>4.5f} pH".format(pH_reading), line=1)
            interfaces.lcd_out("pH V: {0:>3.4f} mV".format(pH_volts * 1000), line=2)
            interfaces.lcd_out("Temp: {0:>4.3f} C".format(temperature_reading), line=3)

            pH_values[pH_list_counter] = pH_reading

            if pH_list_counter == 9:
                valid_num_values_tested = True

            # Check that the temperature of the solution is within bounds
            if (
                abs(temperature_reading - constants.TARGET_TEMPERATURE)
                > constants.TEMPERATURE_ACCURACY
            ):
                # interfaces.lcd_out("TEMPERATURE OUT OF BOUNDS")
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

    def _calibrate_pH(self):
        """Routine for calibrating pH sensor."""
        # get first buffer pH
        buffer1_actual_pH = interfaces.read_user_value("Enter buffer pH:")
        interfaces.lcd_out("Put sensor in buffer", style=constants.LCD_CENT_JUST, line=1)
        interfaces.lcd_out("", line=2)
        interfaces.lcd_out("Press any button", style=constants.LCD_CENT_JUST, line=3)
        interfaces.lcd_out("to record value", style=constants.LCD_CENT_JUST, line=4)
        # Waits for user to press enter
        interfaces.read_user_input()
        buffer1_measured_volts = float(interfaces.read_raw_pH())
        interfaces.lcd_clear()
        interfaces.lcd_out("Recorded pH and volts:", line=1)
        interfaces.lcd_out(
            "{0:>2.5f} pH, {1:>3.4f} V".format(buffer1_actual_pH, buffer1_measured_volts),
            line=2,
        )
        interfaces.lcd_out("Press any button", style=constants.LCD_CENT_JUST, line=3)
        interfaces.lcd_out("to continue", style=constants.LCD_CENT_JUST, line=4)
        interfaces.read_user_input()

        # set calibration constants
        constants.PH_REF_VOLTAGE = buffer1_measured_volts
        constants.PH_REF_PH = buffer1_actual_pH

    def degas(self, seconds):
        interfaces.lcd_clear()
        interfaces.lcd_out("Degassing {0:.0f}".format(seconds), line=1)
        interfaces.lcd_out("seconds", line=2)
        interfaces.stir_speed_fast()
        interfaces.delay(seconds, countdown=True)
        interfaces.stir_speed_slow()

    def _setNextState(self, state):
        self.tc.setNextState(state)
