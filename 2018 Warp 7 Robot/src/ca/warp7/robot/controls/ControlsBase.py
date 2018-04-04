class ControlsBase(object):
	def __init__(self):
		self._controlPool = DataPool("controls")
		self._timer = -1
		self._driver = XboxControllerPlus(DRIVER_ID)
		self._operator = XboxControllerPlus(OPERATOR_ID)
		
		self._lift = Robot.lift
		self._intake = Robot.intake
		self._climber = Robot.climber
		self._drive = Robot.drive

	def periodic(self):
		pass

	def timePassed(self, seconds):
		if self._timer <= 0:
			self._timer = Timer.getFPGATimestamp()
		if Timer.getFPGATimestamp() - self._timer >= seconds:
			self._timer = -1
			return True
		else:
			return False