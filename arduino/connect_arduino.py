"""
The file to connect the Raspberry Pi to the Arduino
"""
import time
import serial

N = 2000
PORT = "/dev/ttyUSB0"
BAUD = 9600
TO = 5

arduino = serial.Serial(port=PORT, baudrate=BAUD, timeout=TO)
arduino.reset_output_buffer()
arduino.reset_input_buffer()


def drive_step_stick(cycles, direction):
    """
    The function to drive the Arduino serial communication
    """
    time.sleep(0.01)
    if arduino.writable():
        arduino.write(cycles.to_bytes(4, "little"))
        arduino.write(direction.to_bytes(1, "little"))
        arduino.flush()
        wait_time = cycles / 1000 + 0.5
        time.sleep(wait_time)
        temp = arduino.readline()
        if temp != b"DONE\r\n":
            print("Error")
            print(temp)
    else:
        print("Arduino Not Available")


print("Lets Go!")
time.sleep(3)
drive_step_stick(N, 1)
time.sleep(0.5)
drive_step_stick(N * 5, 0)
time.sleep(0.5)
drive_step_stick(5, 1)
print("Done calling functions")
