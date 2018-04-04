package ca.warp7.robot.subsystems;

import static ca.warp7.robot.Constants.CLIMBER_MOTORS_IDS;
import static ca.warp7.robot.Constants.CLIMBER_HEIGHT;

import com.ctre.phoenix.motorcontrol.can.WPI_VictorSPX;

from wpilib import Encoder
from common.syncgroup import SyncGroup

class Climber:
	def __init__(self):
		self.climberMotors = new SyncGroup(CLIMBER_MOTORS_IDS, WPI_VictorSPX.class)
		self.climberPot = Encoder(*constants.encoder_elevator)   # --> string potentiometer 
		self.setLocation = 0
		self.ramp = 0.0
		self.rampSpeed = 6.0
		self.tolerance = 0.10
		self.scaledLift = 0

	def setSpeed(self, speed):
		# Ramp to prevent brown outs
		ramp += (self.speed - self.ramp)/self.rampSpeed
		self.climberMotors.set(ramp)

	def setLoc(self, loc):
		self.setLocation = loc

	def periodic(self):
		pass

			