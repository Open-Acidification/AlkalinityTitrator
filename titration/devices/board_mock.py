"""
The file for mocking the CircuitPython board mock
"""


class Pin:
    """
    The Pin class for testing.
    """

    def __init__(self):
        """
        The constructor for the pin class, this allows mock pins to
        have a direction, value, and pull
        """
        self.direction = None
        self.value = None
        self.pull = None


# GPIO PINS
D0 = Pin()
D1 = Pin()
D2 = Pin()
D3 = Pin()
D4 = Pin()
D5 = Pin()
D6 = Pin()
D7 = Pin()
D8 = Pin()
D9 = Pin()
D10 = Pin()
D11 = Pin()
D12 = Pin()
D13 = Pin()
D14 = Pin()
D15 = Pin()
D16 = Pin()
D17 = Pin()
D18 = Pin()
D19 = Pin()
D20 = Pin()
D21 = Pin()
D22 = Pin()
D23 = Pin()
D24 = Pin()
D25 = Pin()
D26 = Pin()
D27 = Pin()
CE0 = Pin()
CE1 = Pin()

# SPI0 Pins
SDA = Pin()
SCL = Pin()
MISO = Pin()
MOSI = Pin()
SCLK = Pin()
SCK = Pin()

# UART0 Pins
TXD = Pin()
RXD = Pin()
TX = Pin()
RX = Pin()

# SPI1 Pins
MISO_1 = Pin()
MOSI_1 = Pin()
SCLK_1 = Pin()
SCK_1 = Pin()
