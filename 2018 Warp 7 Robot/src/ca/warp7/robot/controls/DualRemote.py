from ..controls.Control import *
from ..controls.ControlsBase import ControlsBase

class DualRemote(ControlsBase):	
	
	def periodic(self):
		driver = self.driver
		operator = self.operator
		drive = self.drive
		intake = self.intake
		lift = self.lift
		climber = self.climber
		limelight = self.limelight
		
		if driver.getTrigger(kRight) == DOWN: #intake
			intake.rampSpeed(0.75)
		elif driver.getTrigger(kLeft) == DOWN: #out take
			intake.rampSpeed(-0.5)
		else:
			intake.rampSpeed(0)
		if driver.getStickButton(kRight) == PRESSED:
			drive.setDrivetrainReversed(not drive.driveReversed())
		if driver.getAButton() == PRESSED:
			intake.pistonToggle()
			
		if operator.getXButton() == DOWN:
			lift.setLoc(0.11)
			
		if driver.getBumper(kLeft) == PRESSED:
			limelight.switchCamera()
			print("switching camera")
			
		if operator.getAButton() == DOWN:
			lift.setLoc(operator.getY(kLeft))
		if operator.getBButton() == DOWN:
			climber.setSpeed(operator.getY(kRight)*-1)
			
		#drive.tankDrive(driver.getY(Hand.kLeft), driver.getY(Hand.kLeft))
		drive.cheesyDrive(-driver.getX(kRight), driver.getY(kLeft), driver.getBumper(kLeft) == DOWN, False, driver.getBumper(kRight) != DOWN)