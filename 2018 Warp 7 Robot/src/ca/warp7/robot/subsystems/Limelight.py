class Limelight(object):
	# Create variables
	def __init__(self):
		self._pipelineNumber = 2
		self._table = NetworkTableInstance.getDefault().getTable("limelight")

	def getXOffset(self):
		self._xOffset = self._table.getEntry("tx").getDouble(0)
		return self._xOffset

	def getYOffset(self):
		self._yOffset = self._table.getEntry("ty").getDouble(0)
		return self._yOffset

	def getArea(self):
		self._area = self._table.getEntry("ta").getDouble(0)
		return self._area

	def getSkew(self):
		self._skew = self._table.getEntry("ts").getDouble(0)
		return self._skew

	def foundObject(self):
		found = self._table.getEntry("tv").getDouble(0)
		return found == 1

	def getLEDMode(self):
		self._LEDMode = self._table.getEntry("ledMode").getDouble(1)
		return self._LEDMode

	def getCamMode(self):
		self._camMode = self._table.getEntry("camMode").getDouble(0)
		return self._camMode

	def getNetworkPipeline(self):
		pipeline = self._table.getEntry("pipeline").getDouble(0)
		return self._pipeline

	def getPipeline(self):
		return self._pipeline

	def switchLED(self):
		if self.getLEDMode() == 0:
			self._table.getEntry("ledMode").setDouble(1)
			SmartDashboard.putString("LED Mode", "Off")
		elif self.getLEDMode() == 1:
			self._table.getEntry("ledMode").setDouble(0)
			SmartDashboard.putString("LED Mode", "On")
		elif self.getLEDMode() == 2:
			self._table.getEntry("ledMode").setDouble(1)
			SmartDashboard.putString("LED Mode", "Off")

	def switchCamera(self):
		if self.getCamMode() == 0:
			self._table.getEntry("camMode").setDouble(1)
			SmartDashboard.putString("Camera Mode", "Camera")
		elif self.getCamMode() == 1:
			self._table.getEntry("camMode").setDouble(0)
			SmartDashboard.putString("Camera Mode", "Vision")
			
	def setPipeline(self, pipeline):
		self._table.getEntry("pipeline").setDouble(pipeline)
		self._pipeline = pipeline
		SmartDashboard.putNumber("Camera Mode", pipeline)

	def mutiPipeline(self):
		if not self.foundObject():
			self.setPipeline((self.getNetworkPipeline() + 1) % self._pipelineNumber)
			