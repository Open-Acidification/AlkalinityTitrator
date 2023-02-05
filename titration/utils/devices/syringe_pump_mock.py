"""
The file for the mock SyringePump class
"""
from titration.utils import analysis
from titration.utils import constants
from titration.utils.devices.serial_mock import Serial
from titration.utils import interfaces

ARDUINO_PORT = "/dev/ttyACM0"
ARDUINO_BAUD = 9600
ARDUINO_TIMEOUT = 5

MAX_PUMP_CAPACITY = 1.1


class SyringePump:
    """
    The class for the mock syringe pump device
    """

    def __init__(self):
        """
        The constructor function for the mock syringe pump
        Initializes the arduino to control the pump motor
        """
        self.serial = Serial(
            port=ARDUINO_PORT,
            baudrate=ARDUINO_BAUD,
            timeout=ARDUINO_TIMEOUT,
        )

        self.volume_in_pump = 0
        self.max_pump_capacity = MAX_PUMP_CAPACITY

        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def set_volume_in_pump(self, volume):
        """
        The function to set the mock pump's volume

        Parameters:
            volume (float): amount of volume in the pump
        """
        self.volume_in_pump = volume

    def get_volume_in_pump(self):
        """
        The function to get the mock pump's volume
        """
        return self.volume_in_pump

    def pump_volume(self, volume, direction):
        """
        Moves volume of solution through mock pump

        Parameters:
            volume (float): amount of volume to move
            direction (int): 0 to pull solution in, 1 to pump out
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
                interfaces.lcd.print(
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
        """
        The function to convert volume to cycles
        and ensures and checks pump level and values

        Parameters:
            volume (float): the volume to add
            direction (int): the direction the pump moves
        """
        if direction == 0:
            space_in_pump = self.max_pump_capacity - self.volume_in_pump
            if volume > space_in_pump:
                interfaces.lcd.print("Filling Error", line=4)
            else:
                interfaces.lcd.print("Filling {0:1.2f} ml".format(volume), line=4)
                cycles = analysis.determine_pump_cycles(volume)
                self.drive_step_stick(cycles, direction)
                self.volume_in_pump += volume
        elif direction == 1:
            if volume > self.volume_in_pump:
                interfaces.lcd.print("Pumping Error", line=4)
            else:
                interfaces.lcd.print("Pumping {0:1.2f} ml".format(volume), line=4)
                cycles = analysis.determine_pump_cycles(volume)
                offset = self.drive_step_stick(cycles, direction)
                # offset is what is returned from drive_step_stick which originally is returned from the arduino
                if offset != 0:
                    self.drive_step_stick(offset, 0)
                    self.drive_step_stick(offset, 1)
                self.volume_in_pump -= volume

        interfaces.lcd.print(
            "Pump Vol: {0:1.2f} ml".format(self.volume_in_pump), line=4
        )

    def drive_step_stick(self, cycles, direction):
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
            if temp == b"DONE\r\n" or temp == b"":
                return 0
            else:
                return int(temp)
        else:
            interfaces.lcd.print("Arduino Unavailable", 4, constants.LCD_CENT_JUST)
