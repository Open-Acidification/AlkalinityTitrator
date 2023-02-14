"""
The file for the mock serial mock
"""


class Serial:
    """
    The class for the serial mock
    """

    def __init__(self, port, baudrate, timeout):
        """
        The constructor for the mock serial class
        Initialize the port, baudrate, and timeout for the arduino

        Parameters:
            port (string): the port name that communicates with the arduino
            baudrate (int): the baudrate for the communication
            timeout (int): the time till timeout
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.input_buffer = []
        self.output_buffer = []

    def reset_output_buffer(self):
        """
        The function to reset the serial output buffer
        """
        self.output_buffer = []

    def reset_input_buffer(self):
        """
        The function to reset the serial input buffer
        """
        self.input_buffer = []

    def writable(self):
        """
        The function to tell whether the serial can be written to
        """
        return True

    def write(self, bytes):
        """
        The function to write to the serial

        Parameters:
            bytes (int): number command in byte format to be written to the serial device
        """
        self.input_buffer.append(bytes)

    def flush(self):
        """
        The function to clear both the input and output buffer
        """
        self.input_buffer = []
        self.output_buffer = []

    def readline(self):
        """
        The function to read a line from the serial
        """
        return b"DONE\r\n"
