import time

import serial

n = 2000
# dir = 0
# print(n.to_bytes(4, 'big'))
# time.sleep(2)

port = "/dev/ttyUSB0"
baud = 9600
TO = 5
arduino = serial.Serial(port=port, baudrate=baud, timeout=TO)
arduino.reset_output_buffer()
arduino.reset_input_buffer()


def driveStepStick(cycles, dir):
    time.sleep(0.01)
    if arduino.writable():
        arduino.write(cycles.to_bytes(4, "little"))
        arduino.write(dir.to_bytes(1, "little"))
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
driveStepStick(n, 1)
time.sleep(0.5)
driveStepStick(n * 5, 0)
time.sleep(0.5)
driveStepStick(5, 1)
print("Done calling functions")
