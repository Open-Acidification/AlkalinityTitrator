"""
The file for the serial mock
"""

# pylint: disable = W0107


class Serial:
    """
    The serial mock class
    """

    def __init__(self, port=None, baudrate=None, timeout=None):
        """
        The constructor for the serial class
        """
        pass

    def reset_output_buffer(self):
        """
        The function to reset the serial output buffer
        """
        pass

    def reset_input_buffer(self):
        """
        The function to reset the serial input buffer
        """
        pass

    def writable(self):
        """
        The function to tell whether or not the serial is writable
        """
        return True

    def write(self, byte):
        """
        The function to write to the mock arduino
        """
        pass

    def flush(self):
        """
        The function to flush out the serial input and output buffers
        """
        pass

    def readline(self):
        """
        The function to read a line from the serial
        """
        return b"DONE\r\n"
