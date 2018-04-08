from Constants import *

#import com.ctre.phoenix.motorcontrol.can.WPI_VictorSPX;

from wpilib import Encoder
from misc.SyncGroup import SyncGroup
from ctre.wpi_victorspx import WPI_VictorSPX

class Climber:
	def __init__(self):
		self.climberMotors = SyncGroup(CLIMBER_MOTORS_IDS, WPI_VictorSPX)
		#self.climberPot = Encoder(*constants.encoder_elevator)   # --> string potentiometer 
		self.setLocation = 0
		self.ramp = 0.0
		self.rampSpeed = 6.0
		self.tolerance = 0.10
		self.scaledLift = 0

	def setSpeed(self, speed):
		# Ramp to prevent brown outs
		self.ramp += (speed - self.ramp)/self.rampSpeed
		self.climberMotors.set(self.ramp)

	def setLoc(self, loc):
		self.setLocation = loc

	def periodic(self):
		pass

			