"""
The file for the mock serial mock
"""


class Serial:
    """
    The class for the serial mock
    """

    def __init__(self, port=None, baudrate=None, timeout=None):
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

    def reset_output_buffer(self):
        pass

    def reset_input_buffer(self):
        pass

    def writable(self):
        return True

    def write(self, bytes):
        pass

    def flush(self):
        pass

    def readline(self):
        return b"DONE\r\n"
