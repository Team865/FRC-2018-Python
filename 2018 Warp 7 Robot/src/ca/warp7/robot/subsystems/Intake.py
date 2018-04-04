class Intake(object):
	def __init__(self):
		self._lift = Robot.lift
		self._ramp = 0.0
		self._rampSpeed = 6.0
		self._intakeMotorLeft = MotorGroup(INTAKE_MOTOR_LEFT_IDS, WPI_VictorSPX.)
		self._intakeMotorRight = MotorGroup(INTAKE_MOTOR_RIGHT_IDS, WPI_VictorSPX.)
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

	def pistonToggle(self):
		self._intakePistons.set(not self._intakePistons.get())

	def hasCube(self):
		return self._photosensor.isTriggered()

	def periodic(self):
		#if lift.isBottom():
			#photosensor.update()
		pass