
class Serial():
    def __init__(self, port=None, baudrate=None, timeout=None):
        pass

    def reset_output_buffer(self):
        pass

    def reset_input_buffer(self):
        pass

    def writable(self):
        return True

    def write(self, bytes):
        print(bytes)

    def flush(self):
        pass
    
    def readline(self):
        return "DONE\r\n"