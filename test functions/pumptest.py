# Test routine for pump
# pin map https://pinout.xyz/
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

while(True):
    user_input = input("Press 'a' to pulse the pump; 'q' to exit.\n")
    if user_input == 'a':
        GPIO.output(21, GPIO.HIGH)
        print('Pulse')
    elif user_input == 'q':
        break
GPIO.cleanup()  # use this instead
