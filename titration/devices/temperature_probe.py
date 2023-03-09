"""
The file for the temperature probe device
"""

# pylint: disable = too-many-arguments

from titration.devices.library import MAX31865, SPI, DigitalInOut, board

DEFAULT_REF_RESISTANCE = 4300.0
NOMINAL_RESISTANCE = 1000.0

# Constants for calibration
A = 0.0039083
B = -0.000000578
C = -0.000000000004183


class TemperatureProbe:
    """
    The class for the temperature probe device
    """

    def __init__(self, ref_resistor=DEFAULT_REF_RESISTANCE):
        """
        The constructor for the TemperatureProbe class
        """
        self.spi = SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.c_s = DigitalInOut(board.D4)
        self.sensor = MAX31865(
            self.spi,
            self.c_s,
            wires=3,
            rtd_nominal=NOMINAL_RESISTANCE,
            ref_resistor=ref_resistor,
        )

        self.reference_resistance = ref_resistor

    def get_temperature(self):
        """
        The function to get the probe's temperature
        """
        return self.sensor.temperature

    def get_resistance(self):
        """
        The function to get the probe's resistance
        """
        return self.sensor.resistance

    def calibrate(self, temp):
        """
        The function used for calibrating the temperature probe. View this document for more
        information on how this function works:
        https://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf

        Parameters:
            temp (float): reference temperature inputted by the user
        """
        # Temperature below 0 C
        if temp >= 0:
            temp = NOMINAL_RESISTANCE * (1 + A * temp + B * temp**2)

        # Temperature above 0 C
        else:
            temp = NOMINAL_RESISTANCE * (
                1 + A * temp + B * temp**2 + C * (temp - 100) * temp**3
            )

        # Calculate new reference temperature
        diff = temp - self.sensor.resistance
        new_reference_resistance = (
            self.reference_resistance + diff * self.reference_resistance / temp
        )

        # Reinitialize the device with the new setting
        self.__init__(new_reference_resistance)
