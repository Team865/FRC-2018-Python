import logging
from wpilib import Encoder, Solenoid
from ..misc import Util
from ..misc.DataPool import DataPool
from ..misc.SyncGroup import SyncGroup
from ctre.wpi_victorspx import WPI_VictorSPX
from ..Constants import *


log = logging.getLogger("drivetrain")


class Drive:
	def __init__(self,Robot):
		#self.navx = Robot.navx
		
		self.speedLimit = 0.999
		
		self._leftRamp = 0.0
		self._rightRamp = 0.0
		self._rampSpeed = 6.0
		self._kOonBalanceAngleThresholdDegrees = 5.0
		self._autoBalance = True
		
		self._quickstop_accumulator = 0.0
		self._old_wheel = 0.0
		self._driveReversed = True
		
		self._drivePool = DataPool("Drive")
		# setup drive train motors
		self.rightDrive = SyncGroup(RIGHT_DRIVE_MOTOR_IDS, WPI_VictorSPX)
		self.leftDrive = SyncGroup(LEFT_DRIVE_MOTOR_IDS, WPI_VictorSPX)
		self.rightDrive.setInverted(True)
		# setup drive train gear shifter
		self.shifter = Solenoid(DRIVE_SHIFTER_PORT)
		self.shifter.set(False)
		# setup drive train encoders
		self.leftEncoder = Encoder(LEFT_DRIVE_ENCODER_A, LEFT_DRIVE_ENCODER_B, False, Encoder.EncodingType.k4X)
		self.rightEncoder = Encoder(RIGHT_DRIVE_ENCODER_A, RIGHT_DRIVE_ENCODER_B, False, Encoder.EncodingType.k4X)
		self.leftEncoder.setDistancePerPulse(DRIVE_INCHES_PER_TICK)
		self.leftEncoder.setReverseDirection(True)
		self.rightEncoder.setReverseDirection(False)
		self.rightEncoder.setDistancePerPulse(DRIVE_INCHES_PER_TICK)
		
	def cheesyDrive(self, wheel, throttle, quickturn, altQuickturn, shift):
		throttle = Util.deadband(throttle)
		wheel = Util.deadband(wheel)
		if self._driveReversed:
			wheel *= -1
			
		neg_inertia = wheel - self._old_wheel
		self._old_wheel = wheel
		wheel = Util.sinScale(wheel, 0.9, 1, 0.9)
		
		if wheel * neg_inertia > 0:
			neg_inertia_scalar = 2.5
		else:
			if abs(wheel) > .65:
				neg_inertia_scalar = 6
			else:
				neg_inertia_scalar = 4
		neg_inertia_accumulator = neg_inertia * neg_inertia_scalar
		wheel += neg_inertia_accumulator
		
		if altQuickturn:
			if abs(throttle) < 0.2:
				alpha = .1
				self._quickstop_accumulator = (1 - alpha) * self._quickstop_accumulator + alpha * self.limit(wheel, 1.0) * 5
			over_power = -wheel * .75
			angular_power = -wheel * 1
		elif quickturn:
			if abs(throttle) < 0.2:
				alpha = .1
				self._quickstop_accumulator = (1 - alpha) * self._quickstop_accumulator + alpha * self.limit(wheel, 1.0) * 5
			over_power = 1
			angular_power = -wheel * 1
		else:
			over_power = 0
			sensitivity = .9
			angular_power = throttle * wheel * sensitivity - self._quickstop_accumulator
			self._quickstop_accumulator = Util.wrap_accumulator(self._quickstop_accumulator)
			
		if shift:
			if not self.shifter.get():
				self.shifter.set(True)
		else:
			if self.shifter.get():
				self.shifter.set(False)
				
		right_pwm = left_pwm = throttle
		left_pwm += angular_power
		right_pwm -= angular_power
		if left_pwm > 1:
			right_pwm -= over_power * (left_pwm - 1)
			left_pwm = 1
		elif right_pwm > 1:
			left_pwm -= over_power * (right_pwm - 1)
			right_pwm = 1
		elif left_pwm < -1:
			right_pwm += over_power * (-1 - left_pwm)
			left_pwm = -1
		elif right_pwm < -1:
			left_pwm += over_power * (-1 - right_pwm)
			right_pwm = -1
		if self._driveReversed:
			left_pwm *= -1
			right_pwm *= -1
			
		if self.shifter.get(): # if low gear
			#leftDrive.set(left_pwm)
			#rightDrive.set(right_pwm)
			self.moveRamped(left_pwm, right_pwm)
		else:
			self.moveRamped(left_pwm, right_pwm)
		
	def setGear(self, gear):
		if self.shifter.get() != gear:
			self.shifter.set(gear)

	def tankDrive(self, left, right):
		scaledBalance = self.autoBalance()
		left = self.limit(left + scaledBalance, self.speedLimit)
		right = self.limit(right + scaledBalance, self.speedLimit)
		self.leftDrive.set(left * LEFT_DRIFT_OFFSET)
		self.rightDrive.set(right * RIGHT_DRIFT_OFFSET)

	def limit(self, wheel, d):
		return Util.limit(wheel, d)

	def moveRamped(self, desiredLeft, desiredRight):
		self._leftRamp += (desiredLeft - self._leftRamp) / self._rampSpeed
		self._rightRamp += (desiredRight - self._rightRamp) / self._rampSpeed
		self.tankDrive(self._leftRamp, self._rightRamp)

	def autoShift(self, b):
		if self.shifter.get() != b:
			self.shifter.set(b)

	def periodic(self):
		self._drivePool.logDouble("gyro_angle", self.getRotation());
		self._drivePool.logDouble("left_enc", self.rightEncoder.getDistance());
		self._drivePool.logDouble("right_enc", self.leftEncoder.getDistance());
		
	def setDrivetrainReversed(self, rev):
		self.driveReversed = rev

	def driveReversed(self):
		return self.driveReversed

	def getRotation(self):
		return self.navx.getAngle()

	def getLeftDistance(self):
		return self.leftEncoder.getDistance() * 2.54 * ROBOT_INVERTED

	def getRightDistance(self):
		return self.rightEncoder.getDistance() * 2.54 * ROBOT_INVERTED

	def resetDistance(self):
		self.leftEncoder.reset()
		self.rightEncoder.reset()

	def autoBalance(self):
		'''if self._autoBalance:
			pitchAngleDegrees = self.navx.getPitch()
			scaledPower = 1 + (0 - pitchAngleDegrees - self._kOonBalanceAngleThresholdDegrees) / self._kOonBalanceAngleThresholdDegrees
			if scaledPower > 2:
				scaledPower = 2
			#return scaledPower;'''
		return 0
	
	def setSpeedLimit(self, speedLimit):
		self.speedLimit = self.limit(speedLimit, DRIVE_SPEED_LIMIT)