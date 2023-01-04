#!/bin/sh
apt-get update              # To get the latest package lists
apt-get upgrade
apt install pipenv -y       # pipenv virtual environment
apt-get install rpi.gpio
pipenv install
