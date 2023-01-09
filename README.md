# Alkalinity Titrator Project

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-8-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Project motivations

As CO2 levels increase, the ocean absorbs more CO2 and becomes more acidic. There currently exists a large deficit of data on how this affects wildlife. Alkalinity Titrators are needed for ocean acidification research​. Currently, available models are  expensive ($10,000-$25,000)​. Models on the lower end of the price range are not automated and are therefore time intensive.

This project aims to make ocean acidification research more widely available by lowering the cost of alkalinity titrators.

The problems that the alkalinity-titrator seek to fix are as follows:

- Lower the cost of ocean science equipment by using inexpensive, widely-available parts
- To automate the titration process, saving time and effort when determining total alkalinity

The titration process used in this project is based on SOP 3b from

```Christian, James Robert, Andrew G. Dickson, and Christopher L. Sabine. Guide to Best Practices for Ocean CO2 Measurements. Sidney, B.C.: North Pacific Marine Science Organization, 2007.```

## Current Development Note

<<<<<<< HEAD
The most recent development in this project is the implementation of a UI State Machine framework (see the titration/utils/UIState folder for UI states implemented). While the UI State Machine framework has been fully implemented, the actual titration processes and routines have not been integrated with the UI State Machine (see GitHub Issues for for further specifications).
=======
The most recent development in this project is the implementation of a UI State Machine framework (see the titration/utils/UIState folder for UI states implemented). While the UI State Machine framework has been fully implemented, the actual titration processes and routines have not been integrated with the UI State Machine (see GitHub Issues for further specifications).
>>>>>>> upstream/main

## Setup and Installation

### Setting up the Raspberry Pi

Refer to <https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup> for instructions on setting up the raspberry pi (note: headless setup is not required if a keyboard and monitor are available). Raspbian lite has everything needed, but the desktop version can be downloaded if working with a GUI is preferable.

### Installing software

Run standard updates on the pi:

``` sh
sudo apt-get update 
sudo apt-get upgrade
```

This project utilizes SPI and I2C protocols, both of which often come disabled on the pi. To enable them, run:

``` sh
sudo raspi-config
```

and navigate to "Interfacing Options"; enable both SPI and I2C.

Install git:

``` sh
sudo apt-get install git
```

Clone alkalinity titrator repository to the pi

``` sh
git clone https://github.com/Open-Acidification/alkalinity-titrator.git
```

Run installation script

``` sh
sudo ./install.sh
```
## User Instructions

### Run on Device

To run (with the UI State Machine integrated)

``` sh
./run.sh
```

### Run in Local Environment

To run in a local environment with mocked devices (with the UI State Machine integrated)

``` sh
./run_mocked.sh
```

### Run on Device (old)

To run (the old version without the UI State Machine integrated)

``` sh
./run_old.sh
```

This is the old way to run the code until the titration processes have been integrated into the new UI State Machine.

### Run in Local Environment (old)

To run in a local environment with mocked devices (the old version without the UI State Machine integrated)

``` sh
./run_old_mocked.sh
```

This is the old way to run the code mocked until the titration processes have been integrated into the new UI State Machine.

## Testing

To perform Pytest tests for the devices and UI states.

``` sh
./test.sh
```

## Pins

### Temperature probe ([MAX31865 breakout board](https://learn.adafruit.com/adafruit-max31865-rtd-pt100-amplifier/python-circuitpython))

- PIN 1 (3.3v) to sensor VIN
- PIN 9 to sensor GND
- PIN 19/BCM 10 to sensor SDI
- PIN 21/BCM 21 to sensor SDO
- PIN 23/BCM 23 to sensor CLK
- PIN 29/BCM 5 to sensor CS (or use any other free GPIO pin)

### pH probe ([ADS1115 analog converter](https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython))

- PIN 17 (3.3v) to ADS1115 VDD - Remember the maximum input voltage to any ADC channel cannot exceed this VDD 3V value!
- PIN 6 to ADS1115 GND
- PIN 5/BCM 3 SCL to ADS1115 SCL
- PIN 3/BCM 2 to ADS1115 SDA

## Libraries

1. Circuit Python - <https://github.com/adafruit/Adafruit_CircuitPython_MAX31865>
<br>
Used for communicating with the PT1000

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://www.linkedin.com/in/kadensukachevin/"><img src="https://avatars.githubusercontent.com/u/26241731?v=4?s=100" width="100px;" alt="Kaden Sukachevin"/><br /><sub><b>Kaden Sukachevin</b></sub></a><br /><a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=kadensu" title="Code">💻</a> <a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=kadensu" title="Documentation">📖</a> <a href="https://github.com/Open-Acidification/AlkalinityTitrator/issues?q=author%3Akadensu" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/prestoncarman"><img src="https://avatars.githubusercontent.com/u/3517157?v=4?s=100" width="100px;" alt="Preston Carman"/><br /><sub><b>Preston Carman</b></sub></a><br /><a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=prestoncarman" title="Code">💻</a> <a href="https://github.com/Open-Acidification/AlkalinityTitrator/issues?q=author%3Aprestoncarman" title="Bug reports">🐛</a></td>
      <td align="center"><a href="https://github.com/KonradMcClure"><img src="https://avatars.githubusercontent.com/u/66455502?v=4?s=100" width="100px;" alt="Konrad McClure"/><br /><sub><b>Konrad McClure</b></sub></a><br /><a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=KonradMcClure" title="Code">💻</a></td>
      <td align="center"><a href="https://github.com/Noah-Griffith"><img src="https://avatars.githubusercontent.com/u/78978886?v=4?s=100" width="100px;" alt="Noah-Griffith"/><br /><sub><b>Noah-Griffith</b></sub></a><br /><a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=Noah-Griffith" title="Code">💻</a></td>
      <td align="center"><a href="https://github.com/d-cryptic"><img src="https://avatars.githubusercontent.com/u/52271502?v=4?s=100" width="100px;" alt="Barun Debnath"/><br /><sub><b>Barun Debnath</b></sub></a><br /><a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=d-cryptic" title="Code">💻</a></td>
      <td align="center"><a href="https://kieransukachevin.github.io/first%20portfolio/portfolio.html"><img src="https://avatars.githubusercontent.com/u/54186484?v=4?s=100" width="100px;" alt="Kieran Sukachevin"/><br /><sub><b>Kieran Sukachevin</b></sub></a><br /><a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=kieransukachevin" title="Tests">⚠️</a> <a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=kieransukachevin" title="Code">💻</a></td>
      <td align="center"><a href="https://github.com/jsoref"><img src="https://avatars.githubusercontent.com/u/2119212?v=4?s=100" width="100px;" alt="Josh Soref"/><br /><sub><b>Josh Soref</b></sub></a><br /><a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=jsoref" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center"><a href="https://github.com/TaylorSmith28"><img src="https://avatars.githubusercontent.com/u/83837157?v=4?s=100" width="100px;" alt="TaylorSmith28"/><br /><sub><b>TaylorSmith28</b></sub></a><br /><a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=TaylorSmith28" title="Tests">⚠️</a> <a href="https://github.com/Open-Acidification/AlkalinityTitrator/commits?author=TaylorSmith28" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
