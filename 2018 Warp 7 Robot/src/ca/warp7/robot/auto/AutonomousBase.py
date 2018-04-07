from ca.warp7.robot.misc.DataPool import DataPool
from ca.warp7.robot.auto.Path import Path
import json
from ca.warp7.robot.Constants import *
from ca.warp7.robot.misc.RTS import RTS
from wpilib import SmartDashboard
import math

class AutonomousBaseSpline:
	
	def __init__(self,Robot):
		self.autoPool = DataPool("auto")
		self.drive = Robot.drive
		self.navx = Robot.navx
		self.path = None
			
	def autonomousInit(self, gameData, jsonPaths):
		"""
		 load autonomous data (robot types)
		 load FMS data here
		 calculate best fit path
		"""
		with open("/home/lvuser/Autos/"+jsonPaths+"/"+gameData+".json", 'r') as f:
			self.path = Path(json.load(f))
		
		self.path.calculateSpline()
	
	def autonomousPeriodic(self):
		self.navx.resetAngle()
		i=0
		while i < self.path.pointsLength:
			print(i)
			point = self.path.points[i]
			''' create runnable start point methods here '''
			if point.slowStop:
				pass #slow down to point
			
			self.drive.resetDistance()
			
			self.scaledRuntime = RTS("scaledRuntime",8)
			''' create runnable start point methods here '''
			#task = Runnable(self.lift.periodic)
			#self.liftRTS.addTask(task)
			#self.liftRTS.start()
			
			SmartDashboard.putNumber("break", 0)
			SmartDashboard.putNumber("pointDist", point.distance)
			
			overallDistance = self.getOverallDistance()
			while point.distance > overallDistance:
				overallDistance = self.getOverallDistance()
				SmartDashboard.putNumber("Left", self.drive.getLeftDistance())
				SmartDashboard.putNumber("Right", self.drive.getRightDistance())
				SmartDashboard.putNumber("Avg", self.getOverallDistance())
				
				scaledLocation = overallDistance/point.distance;
				
				derivativesPresent = self.path.derivative(i+scaledLocation,1)
			
				navAngle = self.navx.getAngle()%360
				SmartDashboard.putNumber("navAngle", navAngle)
				
				requiredAngle = math.atan2(derivativesPresent[1], derivativesPresent[0])
				requiredAngle = (requiredAngle if requiredAngle > 0 else (2 * math.pi + requiredAngle)) * 360 / (2 * math.pi)
				angleTolerance=0.3
				turnSpeed = 1-abs((navAngle-requiredAngle)/angleTolerance)
				if turnSpeed < 0:
					turnSpeed = 0
					
				SmartDashboard.putNumber("turnSpeed", turnSpeed);
				
				if (requiredAngle - navAngle) % 360 < 180: # clockwise
					self.drive.tankDrive(AUTO_SPEED,turnSpeed*AUTO_SPEED)
				else:
					self.drive.tankDrive(AUTO_SPEED*turnSpeed,AUTO_SPEED);
				
				#scaledRuntime.stop();
				SmartDashboard.putNumber("break", 1);
				#we should have a speed of zero here if slowStop is true and we are at our point
				
				''' create runnable end point methods here '''
				
			i+=1
					
		self.drive.tankDrive(0,0)
	
	def getOverallDistance(self):
		return (self.drive.getLeftDistance()+self.drive.getRightDistance())/2;
	