from controls.XboxControllerPlus import XboxControllerPlus
from Constants import *
from misc.DataPool import DataPool
from wpilib import Timer

class ControlsBase:
	def __init__(self,Robot):
		self._controlPool = DataPool("controls")
		self._timer = -1
		self.driver = XboxControllerPlus(DRIVER_ID)
		self.operator = XboxControllerPlus(OPERATOR_ID)
		
		self.lift = Robot.lift
		self.intake = Robot.intake
		self.climber = Robot.climber
		self.drive = Robot.drive
		self.limelight = Robot.limelight

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
		
