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

        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def set_volume_in_pump(self, volume):
        self.volume_in_pump = volume

    def get_volume_in_pump(self):
        return self.volume_in_pump

    def pull_volume_in(self, volume_to_add):
        """
        Moves volume of solution through pump
        :param volume: amount of volume to move (float)
        :param direction: 0 to pull solution in, 1 to pump out
        """
        space_in_pump = MAX_PUMP_CAPACITY - self.volume_in_pump
        volume_to_add = min(volume_to_add, space_in_pump)
        self.__drive_pump_down(volume_to_add)

    def push_volume_out(self, volume_to_add):
        """
        The function to push volume out into to the titrator solution

        Parameters:
            volume_to_add (float): the volume to be added to the solution
        """
        # volume greater than max capacity of pump
        if volume_to_add > MAX_PUMP_CAPACITY:
            # pump out all current volume
            next_volume = self.volume_in_pump
            self.__drive_pump_up(next_volume)

                # calculate new volume to add
                volume_to_add = volume_to_add - next_volume

            # keep pumping until full volume_to_add is met
            while volume_to_add > 0:
                next_volume = min(volume_to_add, MAX_PUMP_CAPACITY)
                self.__drive_pump_down(next_volume)
                self.__drive_pump_up(next_volume)
                volume_to_add -= next_volume

        # volume greater than volume in pump
        elif volume_to_add > self.volume_in_pump:
            next_volume = self.volume_in_pump
            self.__drive_pump_up(next_volume)

            else:
                # volume less than volume in pump
                self.drive_pump(volume_to_add, direction)

            self.__drive_pump_down(volume_to_add)
            self.__drive_pump_up(volume_to_add)
        else:
            # volume less than volume in pump
            self.__drive_pump_up(volume_to_add)

    def __drive_pump_down(self, volume):
        """
        The function to drive the down in to pull in liquid

        Parameters:
            volume (float): the volume to add
        """
        space_in_pump = MAX_PUMP_CAPACITY - self.volume_in_pump
        if volume > space_in_pump:
            raise Exception("Filling Error: Not enough space in pump")
        cycles = self.__determine_pump_cycles(volume)
        self.__drive_step_stick(cycles, direction=0)
        self.volume_in_pump += volume

    def __drive_pump_up(self, volume):
        """
        The function to drive the pump up to to push out liquid

        Parameters:
            volume (float): the volume to add
        """
        if volume > self.volume_in_pump:
            raise Exception("Pumping Error: Not enough solution in pump")
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
