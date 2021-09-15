import serial

import titration.utils.analysis as analysis
import titration.utils.constants as constants
import titration.utils.interfaces as interfaces


class Syringe_Pump:
    def __init__(self):
        self.serial = serial.Serial(
            port=constants.ARDUINO_PORT,
            baudrate=constants.ARDUINO_BAUD,
            timeout=constants.ARDUINO_TIMEOUT,
        )

        self.volume_in_pump = constants.volume_in_pump
        self.max_pump_capacity = constants.MAX_PUMP_CAPACITY

        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def set_volume_in_pump(self, volume):
        self.volume_in_pump = volume
        constants.volume_in_pump = volume

    def get_volume_in_pump(self):
        return self.volume_in_pump

    def pump_volume(self, volume, direction):
        """
        Moves volume of solution through pump
        :param volume: amount of volume to move (float)
        :param direction: 0 to pull solution in, 1 to pump out
        """
        volume_to_add = volume

        # pull in solution
        if direction == 0:
            # if volume_to_add is greater than space in the pump
            space_in_pump = self.max_pump_capacity - self.volume_in_pump
            if volume_to_add > space_in_pump:
                volume_to_add = self.max_pump_capacity - self.volume_in_pump
            self.drive_pump(volume_to_add, direction)

        # pump out solution
        elif direction == 1:
            # volume greater than max capacity of pump
            if volume_to_add > self.max_pump_capacity:
                interfaces.lcd_out(
                    "Volume > pumpable", style=constants.LCD_CENT_JUST, line=4
                )

                # pump out all current volume
                next_volume = self.volume_in_pump
                self.drive_pump(next_volume, 1)

                # calculate new volume to add
                volume_to_add = volume_to_add - next_volume

                # keep pumping until full volume_to_add is met
                while volume_to_add > 0:
                    next_volume = min(volume_to_add, self.max_pump_capacity)
                    self.drive_pump(next_volume, 0)
                    self.drive_pump(next_volume, 1)
                    volume_to_add -= next_volume

            # volume greater than volume in pump
            elif volume_to_add > self.volume_in_pump:
                next_volume = self.volume_in_pump
                self.drive_pump(next_volume, 1)

                # calculate remaining volume to add
                volume_to_add -= next_volume

                self.drive_pump(volume_to_add, 0)
                self.drive_pump(volume_to_add, 1)

            else:
                # volume less than volume in pump
                self.drive_pump(volume_to_add, direction)

    def drive_pump(self, volume, direction):
        """Converts volume to cycles and ensures and checks pump level and values"""
        if direction == 0:
            space_in_pump = self.max_pump_capacity - self.volume_in_pump
            if volume > space_in_pump:
                interfaces.lcd_out("Filling Error", line=4)
            else:
                interfaces.lcd_out("Filling {0:1.2f} ml".format(volume), line=4)
                cycles = analysis.determine_pump_cycles(volume)
                self.drive_step_stick(cycles, direction)
                self.volume_in_pump += volume
        elif direction == 1:
            if volume > self.volume_in_pump:
                interfaces.lcd_out("Pumping Error", line=4)
            else:
                interfaces.lcd_out("Pumping {0:1.2f} ml".format(volume), line=4)
                cycles = analysis.determine_pump_cycles(volume)
                offset = self.drive_step_stick(cycles, direction)
                # offset is what is returned from drive_step_stick which originally is returned from the arduino
                if offset != 0:
                    self.drive_step_stick(offset, 0)
                    self.drive_step_stick(offset, 1)
                self.set_volume_in_pump(self.volume_in_pump - volume)

        interfaces.lcd_out("Pump Vol: {0:1.2f} ml".format(self.volume_in_pump), line=4)

    def drive_step_stick(self, cycles, direction):
        """
        cycles and direction are integers
        Communicates with arduino to add HCl through pump
        :param cycles: number of rising edges for the pump
        :param direction: direction of pump
        """
        if cycles == 0:
            return 0

        interfaces.delay(0.01)
        if self.serial.writable():
            self.serial.write(cycles.to_bytes(4, "little"))
            self.serial.write(direction.to_bytes(1, "little"))
            self.serial.flush()
            wait_time = cycles / 1000 + 0.5
            print("wait_time = ", wait_time)
            interfaces.delay(wait_time)
            temp = self.serial.readline()
            if temp == b"DONE\r\n" or temp == b"":
                return 0
            else:
                return int(temp)
        else:
            interfaces.lcd_out("Arduino Unavailable", 4, constants.LCD_CENT_JUST)
