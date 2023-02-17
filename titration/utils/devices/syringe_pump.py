"""
<<<<<<< HEAD
The file for the syringe pump class
"""
import serial
from titration.utils import constants
=======
The file for the SyringePump class
"""
from titration.utils import constants

if constants.IS_TEST:
    from titration.utils.devices.serial_mock import Serial
else:
    from serial import Serial  # type: ignore

ARDUINO_PORT = "/dev/ttyACM0"
ARDUINO_BAUD = 9600
ARDUINO_TIMEOUT = 5
>>>>>>> main

MAX_PUMP_CAPACITY = 1.1
NUM_CYCLES = {0.05: 470, 1: 9550}

# 1 mL is 9550 pump cycles
CYCLES_VOLUME_RATIO = 9550


class SyringePump:
    """
<<<<<<< HEAD
    The class for the Syringe Pump device
=======
    The class for the syringe pump device
>>>>>>> main
    """

    def __init__(self):
        """
<<<<<<< HEAD
        The constructor for the Syringe Pump class
        """
        self.serial = serial.Serial(
            port=constants.ARDUINO_PORT,
            baudrate=constants.ARDUINO_BAUD,
            timeout=constants.ARDUINO_TIMEOUT,
        )

        self.volume_in_pump = constants.VOLUME_IN_PUMP
        self.max_pump_capacity = constants.MAX_PUMP_CAPACITY
=======
        The constructor function for the syringe pump
        Initializes the arduino to control the pump motor
        """
        self.serial = Serial(
            port=ARDUINO_PORT,
            baudrate=ARDUINO_BAUD,
            timeout=ARDUINO_TIMEOUT,
        )

        self.volume_in_pump = 0
>>>>>>> main

        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def set_volume_in_pump(self, volume):
        """
<<<<<<< HEAD
        The function to set volume in pump
        """
        self.volume_in_pump = volume
        constants.VOLUME_IN_PUMP = volume

    def get_volume_in_pump(self):
        """
        The function to get the volume in the pump
=======
        The function to set the pump's volume

        Parameters:
            volume (float): amount of volume in the pump
        """
        if volume > MAX_PUMP_CAPACITY:
            raise Exception(
                "Set Volume Error: Volume set is higher than maximum capacity"
            )
        elif volume < 0:
            raise Exception("Set Volume Error: Volume set cannot be a negative value")
        else:
            self.volume_in_pump = volume

    def get_volume_in_pump(self):
        """
        The function to get the pump's volume

        Returns:
            volume_in_pump (float): the amount of volume in syringe
>>>>>>> main
        """
        return self.volume_in_pump

    def pump_volume_in(self, volume_to_add):
        """
        The function to pull volume of solution into the syringe

        Parameters:
            volume (float): amount of volume to move
        """
        space_in_pump = MAX_PUMP_CAPACITY - self.volume_in_pump
        if volume_to_add > space_in_pump:
            volume_to_add = space_in_pump
        self.__drive_pump_in(volume_to_add)

    def pump_volume_out(self, volume_to_add):
        """
        The function to pump volume out into to the titrator solution

        Parameters:
            volume_to_add (float): the volume to be added to the solution
        """
        # volume greater than max capacity of pump
        if volume_to_add > MAX_PUMP_CAPACITY:

            # pump out all current volume
            next_volume = self.volume_in_pump
            self.__drive_pump_out(next_volume)

            # calculate new volume to add
            volume_to_add = volume_to_add - next_volume

            # keep pumping until full volume_to_add is met
            while volume_to_add > 0:
                next_volume = min(volume_to_add, MAX_PUMP_CAPACITY)
                self.__drive_pump_in(next_volume)
                self.__drive_pump_out(next_volume)
                volume_to_add -= next_volume

        # volume greater than volume in pump
        elif volume_to_add > self.volume_in_pump:
            next_volume = self.volume_in_pump
            self.__drive_pump_out(next_volume)

            # calculate remaining volume to add
            volume_to_add -= next_volume

<<<<<<< HEAD
    def drive_pump(self, volume, direction):
        """
        Converts volume to cycles and ensures and checks pump level and values
        """
        if direction == 0:
            space_in_pump = self.max_pump_capacity - self.volume_in_pump
            if volume <= space_in_pump:
                cycles = self.__determine_pump_cycles(volume)
                self.drive_step_stick(cycles, direction)
                self.volume_in_pump += volume
        elif direction == 1:
            if volume <= self.volume_in_pump:
                cycles = self.__determine_pump_cycles(volume)
                offset = self.drive_step_stick(cycles, direction)
                if offset != 0:
                    self.drive_step_stick(offset, 0)
                    self.drive_step_stick(offset, 1)
                self.set_volume_in_pump(self.volume_in_pump - volume)
=======
            self.__drive_pump_in(volume_to_add)
            self.__drive_pump_out(volume_to_add)
        else:
            # volume less than volume in pump
            self.__drive_pump_out(volume_to_add)
>>>>>>> main

    def __drive_pump_in(self, volume):
        """
        The function to drive the pump in to pull up liquid

        Parameters:
            volume (float): the volume to add
        """
        space_in_pump = MAX_PUMP_CAPACITY - self.volume_in_pump
        if volume > space_in_pump:
            raise Exception("Filling Error: Not enough space in pump")
        else:
            cycles = self.__determine_pump_cycles(volume)
            self.__drive_step_stick(cycles, direction=0)
            self.volume_in_pump += volume

    def __drive_pump_out(self, volume):
        """
        The function to drive the pump out to to push out liquid

        Parameters:
            volume (float): the volume to add
        """
        if volume > self.volume_in_pump:
            raise Exception("Pumping Error: Not enough solution in pump")
        else:
            cycles = self.__determine_pump_cycles(volume)
            offset = self.__drive_step_stick(cycles, direction=1)
            if offset != 0:
                self.__drive_step_stick(offset, 0)
                self.__drive_step_stick(offset, 1)
            self.volume_in_pump -= volume

    def __drive_step_stick(self, cycles, direction):
        """
        The function that communicates with the arduino to add HCl through pump

        Parameters:
            cycles (int): number of rising edges for the pump
            direction (int): direction of pump
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
