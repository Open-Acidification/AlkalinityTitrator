import time
from datetime import datetime

while True:
    print(datetime.now())
    time.sleep(1)

# def write_pot(input):
#     msb = input >> 8
#     lsb = input & 0xFF
#     print("MSB {}, LSB {}".format(msb, lsb))
#     # spi.xfer([msb, lsb])

# for i in range(0x00, 0x1FF, 1):
#     write_pot(i)
#     time.sleep(.05)
# for i in range(0x1FF, 0x00, -1):
#     write_pot(i)
#     time.sleep(.05)