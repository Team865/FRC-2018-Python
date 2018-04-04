class Lift(object):
	def __init__(self):
		self._intake = Robot.intake
		self._drive = Robot.drive
		self._ramp = 0
		self._rampSpeed = 6
		self._LiftMotorLeft = MotorGroup(LIFT_MOTOR_LEFT_IDS, WPI_VictorSPX.)
		self._LiftMotorRight = MotorGroup(LIFT_MOTOR_RIGHT_IDS, WPI_VictorSPX.)
		self._LiftMotorLeft.setInverted(True)
		self._liftEncoder = Encoder(LIFT_ENCODER_A, LIFT_ENCODER_B, False, EncodingType.k4X)
		self._liftEncoder.setDistancePerPulse(1)
		self._liftHallaffect = DigitalInput(HALL_DIO)
		self.zeroEncoder()
		self._liftPID = MiniPID(2.5, 0, 0)
		self._liftPID.setOutputLimits(-0.5, 1)

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
		target = Math.Abs(scale)
		SmartDashboard.putNumber("loc dfliusafusd", target)
		self._liftPID.setSetpoint(target)

	def periodic(self):
		if self.isBottom(): #zero switch is active zero encoder
			self.zeroEncoder()
		scaledLift = self.getEncoderVal() / LIFT_HEIGHT
		speed = self._liftPID.getOutput(scaledLift)
		invertVal = Math.Abs(1 - scaledLift)
		self._drive.setSpeedLimit(TIP_CONSTANT * invertVal)
		#if intake.hasCube():
			#rampSpeed(speed+SPEED_OFFSET_CUBE);
		#else:
			#rampSpeed(speed+SPEED_OFFSET);
		self.rampSpeed(speed)

	def getEncoderVal(self):
		return Math.Abs(self._liftEncoder.getDistance())

	def zeroEncoder(self):
		self._liftEncoder.reset()

	def isBottom(self):
		return not self._liftHallaffect.get()