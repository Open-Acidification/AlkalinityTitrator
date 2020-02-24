# Alkalinity Titrator Project
This project aims to make finding the total alkalinity of seawater easier for scientific applications pertaining to ocean acidification. 
<br>
The problems that the alkalinity-titrator seek to fix are as follows:
- Lower the cost of ocean science equipment


## Setup and Installation
### Setting up the Raspberry Pi
Refer to https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup for instructions on setting up the raspberry pi (note: headless setup is not required if a keyboard and monitor are available). Raspbian lite has everything needed, but the desktop version can be downloaded if workign with a GUI is preferable. 
<br>
Run standard updates:
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
Install Pipenv (a Python virtual environment manager)
```
$ sudo apt install pipenv
```
This project utilizes SPI and I2C protocols, both of which often come disabled on the pi. To enable them, run:
```
$ sudo raspi-config
```
and navigate to "Interfacing Options"; enable both SPI and I2C.

## User Instructions


## Libraries
1. Circuit Python - https://github.com/adafruit/Adafruit_CircuitPython_MAX31865 
<br>
Used for communicating with the PT1000 