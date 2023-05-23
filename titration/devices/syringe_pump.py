import serial
import time

ARDUINO_PORT = "/dev/ttyACM0"
ARDUINO_BAUD = 9600
ARDUINO_TIMEOUT = 5

MAX_PUMP_CAPACITY = 1.1
NUM_CYCLES = {0.05: 470, 1: 9550}

# 1 mL is 9550 pump cycles
CYCLES_VOLUME_RATIO = 9550


class Syringe_Pump:
    def __init__(self):
        self.serial = serial.Serial(
            port=ARDUINO_PORT,
            baudrate=ARDUINO_BAUD,
            timeout=ARDUINO_TIMEOUT,
        )

        self.volume_in_pump = 0
        self.max_pump_capacity = MAX_PUMP_CAPACITY

        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def set_volume_in_pump(self, volume):
        self.volume_in_pump = volume

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
            if volume <= space_in_pump:
                cycles = self.determine_pump_cycles(volume)
                self.drive_step_stick(cycles, direction)
                self.volume_in_pump += volume
        elif direction == 1:
            if volume <= self.volume_in_pump:
                cycles = self.determine_pump_cycles(volume)
                offset = self.drive_step_stick(cycles, direction)
                # offset is what is returned from drive_step_stick which originally is returned from the arduino
                if offset != 0:
                    self.drive_step_stick(offset, 0)
                    self.drive_step_stick(offset, 1)
                self.set_volume_in_pump(self.volume_in_pump - volume)

    def drive_step_stick(self, cycles, direction):
        """
        cycles and direction are integers
        Communicates with arduino to add HCl through pump
        :param cycles: number of rising edges for the pump
        :param direction: direction of pump
        """
        if cycles == 0:
            return 0

        time.sleep(0.01)
        if self.serial.writable():
            self.serial.write(cycles.to_bytes(4, "little"))
            self.serial.write(direction.to_bytes(1, "little"))
            self.serial.flush()
            wait_time = cycles / 1000 + 0.5
            print("wait_time = ", wait_time)
            time.sleep(wait_time)
            temp = self.serial.readline()
            if temp == b"DONE\r\n" or temp == b"":
                return 0
            else:
                return int(temp)
            
    def determine_pump_cycles(self, volume_to_add):
        """
        Determines the number of cycles to move given volume
        :param volume_to_add: amount of volume to add in mL
        :return: number of cycles
        """
        if volume_to_add in NUM_CYCLES:
            return NUM_CYCLES[volume_to_add]
        if volume_to_add > MAX_PUMP_CAPACITY:
            return 0
        pump_cycles = CYCLES_VOLUME_RATIO * volume_to_add
        # NOTE rounds down
        return int(pump_cycles)
