from com.kauailabs.navx.frc.AHRS import AHRS
from wpilib import SPI
import logging
logger = logging.getLogger('Navx')

class Navx:
	def __init__(self, rate=None):		
		if rate is None:
			self._ahrs = AHRS(SPI.Port.kMXP)
		else:
			self._ahrs = AHRS(SPI.Port.kMXP, rate)
			
		if not self._ahrs.isConnected():
			print("Navx is not Connected")
		elif self._ahrs.isCalibrating():
			print("Calibrating Navx")
		self._ahrs.zeroYaw()
		self.resetDisplacement()
		
	def updateDisplacement(self):
		if self._ahrs.isMoving():
			accel_g = (self._ahrs.getRawAccelX(), self._ahrs.getRawAccelY())
			sample_time = 1.0 / self._updater.getHz()
			for i in range(2):
				m_s2 = accel_g[i] * 9.80665
				self._displacement[i] += self._last_velocity[i] * sample_time + (0.5 * m_s2 * sample_time * sample_time)
				self._last_velocity[i] = self._last_velocity[i] + (m_s2 * sample_time)
		else:
			self._last_velocity = [0, 0]
			
	def resetDisplacement(self):
		self._displacement = [0, 0]
		self._last_velocity = [0, 0]

	def getAngle(self):
		return self._ahrs.getAngle()

	def stopUpdateDisplacement(self):
		self._updater.stop()

	def getDispX(self):
		return self._displacement[0]

	def getDispY(self):
		return self._displacement[1]
		
	def getVelX(self):
		return self._last_velocity[0]

	def getVelY(self):
		return self._last_velocity[1]

	def isMoving(self):
		return self._ahrs.isMoving()

	def getDisplacementUpdater(self):
		return self._updater

	def resetAngle(self):
		self._ahrs.reset()

	def getPitch(self):
		return self._ahrs.getPitch()