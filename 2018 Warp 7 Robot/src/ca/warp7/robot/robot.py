#!/usr/bin/env python3
from wpilib import IterativeRobot, run, Compressor, DriverStation, AnalogInput, SmartDashboard
from ..robot.subsystems import Climber, Drive, Lift, Intake, Limelight, Navx
from ..robot.misc.RTS import RTS
from ..robot.misc.Util import Runnable
from ..robot.controls.DualRemote import DualRemote
from ..robot.Constants import *

class Robot(IterativeRobot):
	def robotInit(self):
		#self.navx = Navx.Navx()
		self.climber = Climber.Climber()
		self.limelight = Limelight.Limelight()
		self.drive = Drive.Drive(self)
		self.intake = None
		self.lift = Lift.Lift(self)
		self.intake = Intake.Intake(self)
		self.lift._intake = self.intake
		
		
		self.controls = DualRemote(self)
		
		self.compressor = Compressor(COMPRESSOR_PIN)
		self.driverStation = DriverStation.getInstance()
		
		self.a0 = AnalogInput(0)
		self.a1 = AnalogInput(1)
		self.a2 = AnalogInput(2)
		self.a3 = AnalogInput(3)
		
		self.autoPin = -1
		
		#self.liftRTS = RTS("liftRTS",8)
		#task = Runnable(self.lift.periodic,[])
		#self.liftRTS.addTask(task)
		#self.liftRTS.start()
		
	def autonomousInit(self):
		self.lift.zeroEncoder()
		self.lift.setLoc(0)
		self.drive.resetDistance()
		#self.navx.resetAngle()
		self.autoPin = self.autoSelector()
		
	def autonomousPeriodic(self):
		pass

	def teleopInit(self):
		self.drive.setSpeedLimit(1);
		self.drive.tankDrive(0,0);
		self.compressor.setClosedLoopControl(True);
		self.drive.resetDistance();

	def teleopPeriodic(self):
		a = 0
		while self.isOperatorControl() and self.isEnabled():
			self.controls.periodic()
			self.limelight.mutiPipeline()
			self.intake.periodic()

			b = self.lift.getEncoderVal()
			if a < b:
				a = b
			SmartDashboard.putNumber("pipeline id", self.limelight.getPipeline())
			SmartDashboard.putBoolean("inake hasCube", self.intake.hasCube())
			#drive.periodic()

			#SmartDashboard.putNumber("liftRTS hz", self.liftRTS.getHz())
			
			SmartDashboard.putNumber("0", self.a0.getAverageVoltage())
			SmartDashboard.putNumber("1", self.a1.getAverageVoltage())
			SmartDashboard.putNumber("2", self.a2.getAverageVoltage())
			SmartDashboard.putNumber("3", self.a3.getAverageVoltage())

			SmartDashboard.putNumber("Lift", a)
			SmartDashboard.putNumber("Drive Right Dist", self.drive.getRightDistance())
			SmartDashboard.putNumber("Drive Left Dist", self.drive.getLeftDistance())
			#SmartDashboard.putNumber("pitch", self.navx.getPitch())

	def autoSelector(self):
		voltage = 0
		number = 0
		if self.a0.getAverageVoltage() > voltage:
			number = 1
			voltage = self.a0.getAverageVoltage()
		
		if self.a1.getAverageVoltage() > voltage:
			number = 2
			voltage = self.a1.getAverageVoltage()
		
		if self.a2.getAverageVoltage() > voltage:
			number = 0
			voltage = self.a2.getAverageVoltage()
		
		if self.a3.getAverageVoltage() > voltage:
			number = 3
			voltage = self.a3.getAverageVoltage()
		
		print("volt:",voltage)
		return number
			
if __name__ == "__main__":
	run(Robot)