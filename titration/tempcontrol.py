import time
from gpiozero import LED
import board
import busio
import digitalio
import pandas as pd
import adafruit_max31865
from array import*

PID_DEFAULT_KP = 0.09
PID_DEFAULT_TI = 0.000001
PID_DEFAULT_TD = 9
PID_ANTIWINDUP_KP = 0.04
PID_ANTIWINDUP_TI = 0.004
PID_ANTIWINDUP_TD = 9

class TempControl():
	"""docstring for TempControl"""
	def __init__(self, sensor, relay_pin):
		self.sensor = sensor
		self.relay = LED(relay_pin)

	# PID Parameters
	kp = 0.09
	Ti = 0.000001
	Td = 9

	# PID Gain
	k = 0
	integral = 0
	integral_prior = 0
	derivative = 0
	error = 0
	error_prior = 0

	# Step Count - How many cycles have we done?
	stepCnt = 0

	# Time between steps (seconds) - how long to wait until next step
	timeStep = 1

	# What time was the last step taken
	# not localtime() since we need fractional seconds
	timeLast = time.time()
	timeNext = time.time()

	# What state is the relay currently in
	relayOn = False

	# Log of times measurements were taken
	timeLog = []

	# Target temperature
	setPoint = 30

	"""
	Primary function run during the titration. update() will
	check if it is time to change the state of the relay and
	update the PID control and relay status as necessary
	"""
	def update(self):
		timeNow = time.time() # not localtime() since we need fractional seconds

		# TODO: Add logging of timeNow-timeNext results (how late?)
		if (timeNow >= self.timeNext):
			if (self.relayOn):
				# we'll turn it off
				# turn off
				self.__set_relayState(False)

				# count a step
				self.stepCnt += 1

				# update error/integral_priors
				self.__update_priors()

				# set off time based on k
				self.__update_timeNext(time.time()+self.timeStep*(1-self.k))

			else:
				# we'll turn it on
					# update PID gains
					# set on time based on k

				#Get data values
	    		temp=self.sensor.temperature
	    		#timelog.append(timeNow.tm_sec)

	    		#anti-windup
	    		if (stepCnt < 250):
	    			self.__set_integral_zero()
	    		elif (stepCnt == 250):
	    			self.__set_controlparam_antiwindup()

	    		# Update PID Gain
				self.__update_gains()

				# Check if relay needs to be turned on
				if (temp < self.setPoint):
					if self.k <= 0:
						self.k = 0
						self.__update_timeNext(time.time()+self.timeStep)
					elif self.k < 1:
						self.__set_relayState(True)
						self.__update_timeNext(time.time()+self.timeStep*self.k)
					else:
						self.k = 1
						self.__set_relayState(True)
						self.__update_timeNext(time.time()+self.timeStep)
					
				# temp above setpoint
				else: 
					self.k=0
					self.__set_relayState(False)
					self.__update_timeNext(time.time()+self.timeStep)
					self.__update_priors()



		else:
			# pass until next update is called
			return

	"""
	Update the time of the last step taken with the time of the 
	step just taken with time.time()
	"""
	def __update_timeLast(self, stepTime):
		self.timeLast = stepTime;

	"""
	Update the time that the next relay action should be taken
	"""
	def __update_timeNext(self, stepTime):
		self.timeNext = stepTime;

	"""
	After 250 cycles, the PID control parameters should
	be changed to new values
	"""
	def __set_controlparam_antiwindup(self):
		self.kp = PID_ANTIWINDUP_KP
		self.Ti = PID_ANTIWINDUP_TI
		self.Td = PID_ANTIWINDUP_TD

	"""
	For the first 250 cycles, the PID parameters should
	be set to their default values. 
	"""
	def __set_controlparam_default(self):
		self.kp = PID_DEFAULT_KP
		self.Ti = PID_DEFAULT_TI
		self.Td = PID_DEFAULT_TD

	def __update_gains(self):
		self.error = self.setpoint - temp
		self.integral = self.integral_prior + self.error * self.timeStep
		self.derivative = (self.error - self.error_prior) / self.timeStep
		self.k = self.kp * (self.error + self.Ti * self.integral + self.Td * self.derivative)


	def __update_priors(self):
		self.error_prior = self.error
		self.integral_prior = self.integral

	"""
	For the first 250 cycles, the integral value should
	be zeroed to prevent windup 
	"""
	def __set_integral_zero(self):
		self.integral = 0

	def __set_relayState(self, boolean):
		self.relayOn = boolean
		if (boolean == True):
			self.relay.on()
		else:
			self.relay.off()



		
