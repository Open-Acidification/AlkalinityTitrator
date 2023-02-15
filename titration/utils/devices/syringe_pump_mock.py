"""
The function for the syringe pump mock
"""
from AlkalinityTitrator.titration.utils import constants
from AlkalinityTitrator.titration.utils.devices import serial_mock

MAX_PUMP_CAPACITY = 1.1
NUM_CYCLES = {0.05: 470, 1: 9550}

# 1 mL is 9550 pump cycles
CYCLES_VOLUME_RATIO = 9550


class SyringePump:
    """
    The class for the Syringe Pump mock
    """

    def __init__(self):
        """
        The constructor for the Syringe Pump mock
        """
        self.serial = serial_mock.Serial(
            port=constants.ARDUINO_PORT,
            baudrate=constants.ARDUINO_BAUD,
            timeout=constants.ARDUINO_TIMEOUT,
        )

        self.volume_in_pump = constants.VOLUME_IN_PUMP
        self.max_pump_capacity = constants.MAX_PUMP_CAPACITY

    def set_volume_in_pump(self, volume):
        """
        The function to set the volume in the mock pump
        """
        self.volume_in_pump = volume
        constants.VOLUME_IN_PUMP = volume

    def get_volume_in_pump(self):
        """
        The function to get the volume in the pump
        """
        return self.volume_in_pump

    def pump_volume(self, volume, direction):
        """
        The function to pump an amount of volume into the solution
        """
        volume_to_add = volume

        # pull in solution
        if direction == 0:
            # check if volume to add is greater than space left
            space_in_pump = self.max_pump_capacity - self.volume_in_pump
            if volume_to_add > space_in_pump:
                volume_to_add = self.max_pump_capacity - self.volume_in_pump
            self.drive_pump(volume_to_add, direction)

        # pump out solution
        elif direction == 1:
            # volume greater than max capacity of pump
            if volume_to_add > self.max_pump_capacity:

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
        """
        Converts volume to cycles and ensures and checks pump level and values
        """
        if direction == 0:
            space_in_pump = self.max_pump_capacity - self.volume_in_pump
            if volume > space_in_pump:
                raise Exception("FILLING ERROR")
            cycles = self.__determine_pump_cycles(volume)
            self.drive_step_stick(cycles, direction)
            self.volume_in_pump += volume
        elif direction == 1:
            if volume > self.volume_in_pump:
                raise Exception("PUMPING ERROR")
            cycles = self.__determine_pump_cycles(volume)
            offset = self.drive_step_stick(cycles, direction)
            if offset != 0:
                self.drive_step_stick(offset, 0)
                self.drive_step_stick(offset, 1)
            self.volume_in_pump -= volume

    def drive_step_stick(self, cycles, direction):
        """
        cycles and direction are integers
        Communicates with arduino to add HCl through pump
        :param cycles: number of rising edges for the pump
        :param direction: direction of pump
        """
        if cycles == 0:
            return 0

        if self.serial.writable():
            self.serial.write(cycles.to_bytes(4, "little"))
            self.serial.write(direction.to_bytes(1, "little"))
            self.serial.flush()
            temp = self.serial.readline()
            if temp in (b"DONE\r\n", b""):
                return 0
            return int(temp)
        raise Exception("ARDUINO UNAVAILABLE")

    def __determine_pump_cycles(self, volume_to_add):
        """
        The function to determines the number of cycles to move given volume
        Parameters:
            volume_to_add (int): amount of volume to add in mL
        Returns:
            number of cycles (int)
        """
        if volume_to_add in NUM_CYCLES:
            return NUM_CYCLES[volume_to_add]
        if volume_to_add > 1.1:
            return 0
        pump_cycles = CYCLES_VOLUME_RATIO * volume_to_add
        return int(pump_cycles)
