#!/usr/bin/env python3
from wpilib import IterativeRobot, run
from subsystems import Climber, Drive, Lift, Intake, Limelight, Navx


class Robot(IterativeRobot):
	def robotInit(self):
		#self.limelight = 
		pass

	def autonomousInit(self):
		pass

	def autonomousPeriodic(self):
		pass

	def teleopInit(self):
		pass

	def teleopPeriodic(self):
		pass

if __name__ == "__main__":
	run(Robot)