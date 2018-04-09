from misc.DataPool import DataPool
from auto.Path import Path
import json
from Constants import *
from multiprocessing import Process
from misc.com.stormbots.MiniPID import MiniPID
from misc.RTS import RTS
from wpilib import SmartDashboard
import math

class AutonomousBaseSpline(Process):
	
	def __init__(self,Robot):
		Process.__init__(self)
		
		self.autoPool = DataPool("auto")
		self.Robot = Robot
		self.drive = Robot.drive
		self.navx = Robot.navx
		self.path = None
		self.turnPID = MiniPID(*TURN_PID)
			
	def autonomousInit(self, gameData, jsonPaths):
		"""
		 load autonomous data (robot types)
		 load FMS data here
		 calculate best fit path
		"""
		with open("/home/lvuser/Autos/"+jsonPaths+"/"+gameData+".json", 'r') as f:
			self.path = Path(json.load(f))
		
		self.path.calculateSpline()
	
	def run(self):
		self.navx.resetAngle()
		i=0
		while self.Robot.isAutonomous() and i < self.path.pointsLength:
			print(i)
			point = self.path.points[i]
			''' create runnable start point methods here '''
			if point.slowStop:
				pass #slow down to point
			
			self.drive.resetDistance()
			
			self.scaledRuntime = RTS("scaledRuntime",8)
			''' create runnable start point methods here '''
			#self.liftRTS.addTask(self.lift.periodic)
			#self.liftRTS.start()
			
			SmartDashboard.putNumber("break", 0)
			SmartDashboard.putNumber("pointDist", point.distance)
			
			overallDistance = self.getOverallDistance()
			while self.Robot.isAutonomous() and point.distance > overallDistance:
				overallDistance = self.getOverallDistance()
				
				scaledLocation = overallDistance/point.distance;
				
				derivativesPresent = self.path.derivative1(i+scaledLocation,1)
			
				navAngle = self.navx.getAngle()%360
				SmartDashboard.putNumber("navAngle", navAngle)
				
				requiredAngle = math.atan2(derivativesPresent[1], derivativesPresent[0])
				requiredAngle = (requiredAngle if requiredAngle > 0 else (2 * math.pi + requiredAngle)) * 360 / (2 * math.pi)
				
				turnSpeed = self.turnPID.getOutput(navAngle, requiredAngle)
				SmartDashboard.putNumber("turnSpeed", turnSpeed);
					
				if turnSpeed < 0: # turn left
					turnSpeed *= -1;
					self.drive.tankDrive(AUTO_SPEED - turnSpeed, AUTO_SPEED);
				else: # turn right
					self.drive.tankDrive(AUTO_SPEED, AUTO_SPEED - turnSpeed);
				
				
				#scaledRuntime.stop();
				SmartDashboard.putNumber("break", 1);
				#we should have a speed of zero here if slowStop is true and we are at our point
				
				''' create runnable end point methods here '''
				
			i+=1
					
		self.drive.tankDrive(0,0)
	
	def getOverallDistance(self):
		return (self.drive.getLeftDistance()+self.drive.getRightDistance())/2;
	