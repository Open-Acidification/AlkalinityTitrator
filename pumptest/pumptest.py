# Test routine for pump
# pin map https://pinout.xyz/
# to setup raspberr pi for the test:



import RPi.GPIO as GPIO
import time
PIN_NUMBER = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_NUMBER, GPIO.OUT)

while(True):
    user_input = input("Press 'a' to pulse the pump; 'q' to exit.\n")
    if user_input == 'a':
        GPIO.output(PIN_NUMBER, GPIO.HIGH)
        print('Pulse')
    elif user_input == 'q':
        break
    time.sleep(1)
    GPIO.output(PIN_NUMBER, GPIO.LOW)
GPIO.cleanup()  # use this instead
