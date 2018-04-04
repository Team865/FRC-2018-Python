class LimelightPhotosensor:
	def __init__(self, limelight, pipeline):
		self._found = False
		self._limelight = limelight
		self._pipeline = pipeline

	def update(self):
		self._found = self._limelight.getPipeline() == self._pipeline and self._limelight.foundObject()

	def isTriggered(self):
		return self._found