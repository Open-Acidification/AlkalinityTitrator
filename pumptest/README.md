## Setup and Installation
### Setting up the Raspberry Pi
Refer to https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup for instructions on setting up the raspberry pi (note: headless setup is not required if a keyboard and monitor are available). Raspbian lite has everything needed, but the desktop version can be downloaded if working with a GUI is preferable. 
### Installing software
Run standard updates on the pi:
``` 
$ sudo apt-get update 
$ sudo apt-get upgrade
```
Install git:
```
$ sudo apt-get install git
```
Clone alkalinity titrator repository to the pi
```
$ git clone https://github.com/Open-Acidification/alkalinity-titrator.git
```
This project utilizes SPI and I2C protocols, both of which often come disabled on the pi. To enable them, run:
```
$ sudo raspi-config
```
and navigate to "Interfacing Options"; enable both SPI and I2C.
To install RPI.GPIO:
```
$ sudo apt-get install rpi.gpio
```
Checkout develop branch
```
$ git checkout develop
```
Navigate to the folder with the test
```
$ cd alkalinity-titrator/pumptest
```
Run the test; press 'a' to send a pulse to pin 18 (BCM 24)
```
$ python3 pumptest.py
```