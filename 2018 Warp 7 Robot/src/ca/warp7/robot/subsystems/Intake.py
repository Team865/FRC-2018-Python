from misc.LimelightPhotosensor import LimelightPhotosensor
from wpilib import Solenoid
from Constants import *
from ctre.wpi_victorspx import WPI_VictorSPX

class Intake:
	def __init__(self,Robot):
		self._lift = Robot.lift
		self._ramp = 0.0
		self._rampSpeed = 6.0
		self._intakeMotorLeft = WPI_VictorSPX(*INTAKE_MOTOR_LEFT_IDS)
		self._intakeMotorRight = WPI_VictorSPX(*INTAKE_MOTOR_RIGHT_IDS)
		self._intakeMotorRight.setInverted(True)
		self._intakePistons = Solenoid(INTAKE_PISTONS)
		self._photosensor = LimelightPhotosensor(Robot.limelight, 1)

	def rampSpeed(self, speed):
		# Ramp to prevent brown outs
		self._ramp += (speed - self._ramp) / self._rampSpeed
		self._intakeMotorLeft.set(self._ramp)
		self._intakeMotorRight.set(self._ramp)

	def setSpeed(self, speed):
		self._intakeMotorLeft.set(speed)
		self._intakeMotorRight.set(speed)
		
	def getSpeed(self):
		return self._intakeMotorLeft.get()
	
	def pistonToggle(self):
		self._intakePistons.set(not self._intakePistons.get())

	def hasCube(self):
		return self._photosensor.isTriggered()

	def periodic(self):
		#if lift.isBottom():
			#photosensor.update()
		pass