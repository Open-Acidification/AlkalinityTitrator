"""
The file for the SyringePump class
"""
from titration.devices.library import Serial

ARDUINO_PORT = "/dev/ttyACM0"
ARDUINO_BAUD = 9600
ARDUINO_TIMEOUT = 5

# 1 mL is 9550 pump cycles
CYCLES_VOLUME_RATIO = 9550
MAX_PUMP_CAPACITY = 1.1

PUMP_IN_DIRECTION = 0
PUMP_OUT_DIRECTION = 1


class SyringePump:
    """
    The class for the Syringe Pump device
    """

    def __init__(self):
        """
        The constructor function for the syringe pump
        Initializes the arduino to control the pump motor
        """
        self._serial = Serial(
            port=ARDUINO_PORT,
            baudrate=ARDUINO_BAUD,
            timeout=ARDUINO_TIMEOUT,
        )

        self._pump_volume = 0
        self._added_volume = 0

        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()

    def get_pump_volume(self):
        """
        The function to get the pump's volume

        Returns:
            _pump_volume (float): the amount of volume in syringe
        """
        return self._pump_volume

    def get_added_volume(self):
        """
        The function to get the volume the pump added

        Returns:
            _added_volume (float): the amount of volume added to the titration solution
        """
        return self._added_volume

    def clear_added_volume(self):
        """
        The function to set the volume the pump added to zero
        """
        self._added_volume = 0

    def fill(self):
        """
        The function to fill the pump
        """
        self._drive_pump_in(MAX_PUMP_CAPACITY - self._pump_volume)

    def empty(self):
        """
        The function to empty the pump
        """
        temp = self._added_volume
        self._drive_pump_out(self._pump_volume)
        self._added_volume = temp

    def pump_in(self, volume_to_add):
        """
        The function to pull volume of solution into the syringe
        The max this function can pump in is 1.1 ml

        Parameters:
            volume (float): amount of volume to move
        """
        space_in_pump = MAX_PUMP_CAPACITY - self._pump_volume
        volume_to_add = min(volume_to_add, space_in_pump)
        self._drive_pump_in(volume_to_add)

    def pump_out(self, volume_to_add):
        """
        The function to pump volume out into to the titrator solution

        Parameters:
            volume_to_add (float): the volume to be added to the solution
        """
        if volume_to_add > MAX_PUMP_CAPACITY:

            # Pump out current volume
            volume_to_add -= self._pump_volume
            self._drive_pump_out(self._pump_volume)

            # Pumping until full volume_to_add is met
            while volume_to_add > 0:
                next_volume = min(volume_to_add, MAX_PUMP_CAPACITY)
                self._drive_pump_in(next_volume)
                self._drive_pump_out(next_volume)
                volume_to_add -= next_volume

        elif volume_to_add > self._pump_volume:

            # Pump out current volume
            volume_to_add -= self._pump_volume
            self._drive_pump_out(self._pump_volume)

            # Pump remaining volume to add
            self._drive_pump_in(volume_to_add)
            self._drive_pump_out(volume_to_add)

        else:
            self._drive_pump_out(volume_to_add)

    def _drive_pump_in(self, volume):
        """
        The function to drive the pump in to pull up liquid

        Parameters:
            volume (float): the volume to add
        """
        cycles = int(CYCLES_VOLUME_RATIO * volume)
        self._drive_step_stick(cycles, PUMP_IN_DIRECTION)
        self._pump_volume += volume

    def _drive_pump_out(self, volume):
        """
        The function to drive the pump out to to push out liquid

        Parameters:
            volume (float): the volume to add
        """
        cycles = int(CYCLES_VOLUME_RATIO * volume)
        offset = self._drive_step_stick(cycles, PUMP_OUT_DIRECTION)
        if offset != 0:
            self._drive_step_stick(offset, PUMP_IN_DIRECTION)
            self._drive_step_stick(offset, PUMP_OUT_DIRECTION)
        self._pump_volume -= volume
        self._added_volume += volume

    def _drive_step_stick(self, cycles, direction):
        """
        The function that communicates with the arduino to add HCl through pump

        Parameters:
            cycles (int): number of rising edges for the pump
            direction (int): direction of pump
        """
        if cycles == 0:
            return 0

        if self._serial.writable():
            self._serial.write(cycles.to_bytes(4, "little"))
            self._serial.write(direction.to_bytes(1, "little"))
            self._serial.flush()
            temp = self._serial.readline()
            if temp in (b"DONE\r\n", b""):
                return 0
            return int(temp)
        raise Exception("ARDUINO UNAVAILABLE")
