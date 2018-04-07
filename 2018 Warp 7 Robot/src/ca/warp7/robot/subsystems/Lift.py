from ca.warp7.robot.misc.SyncGroup import SyncGroup
from wpilib import Encoder, DigitalInput, SmartDashboard
from ca.warp7.robot.Constants import *
from com.stormbots.MiniPID import MiniPID
from ctre.wpi_victorspx import WPI_VictorSPX
from math import pow

class Lift:
	def __init__(self,Robot):
		self._intake = Robot.intake
		self._drive = Robot.drive
		self._ramp = 0
		self._rampSpeed = 6
		self._LiftMotorLeft = SyncGroup(LIFT_MOTOR_LEFT_IDS, WPI_VictorSPX)
		self._LiftMotorRight = SyncGroup(LIFT_MOTOR_RIGHT_IDS, WPI_VictorSPX)
		self._LiftMotorLeft.setInverted(True)
		self._liftEncoder = Encoder(LIFT_ENCODER_A, LIFT_ENCODER_B, False, Encoder.EncodingType.k4X)
		self._liftEncoder.setDistancePerPulse(1)
		self._liftHallaffect = DigitalInput(HALL_DIO)
		self.zeroEncoder()
		self._liftPID = MiniPID(*LIFT_PID)
		self._liftPID.setOutputLimits(-0.5, 1)
		self.disableSpeedLimit = False

	def setSpeed(self, speed):
		self._LiftMotorLeft.set(speed)
		self._LiftMotorRight.set(speed)

	def rampSpeed(self, speed):
		self._ramp += (speed - self._ramp) / self._rampSpeed
		if False and speed > 0: #is max limit hit
			self._ramp = 0
		self._LiftMotorLeft.set(self._ramp)
		self._LiftMotorRight.set(self._ramp)

	def setLoc(self, scale):
		target = abs(scale)
		if target <= 0.1:
			target = 0
		SmartDashboard.putNumber("loc dfliusafusd", target)
		self._liftPID.setSetpoint(target)

	def periodic(self):
		
		if self.isBottom(): #zero switch is active zero encoder
			self.zeroEncoder()
		else:
			if self._intake.getSpeed() >= 0:
				self._intake.rampSpeed(0.3);
		
		scaledLift = self.getEncoderVal()/LIFT_HEIGHT;
		speed = self._liftPID.getOutput(scaledLift);
		
		if not self.disableSpeedLimit:
			speedLimit = pow(0.25,scaledLift);
			self._drive.setSpeedLimit(speedLimit);
		else:
			self._drive.setSpeedLimit(1);
		
		self.rampSpeed(speed);

	def getEncoderVal(self):
		return abs(self._liftEncoder.getDistance())

	def zeroEncoder(self):
		self._liftEncoder.reset()

	def isBottom(self):
		return not self._liftHallaffect.get()