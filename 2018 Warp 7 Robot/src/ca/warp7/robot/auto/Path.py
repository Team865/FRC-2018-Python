from scipy import interpolate

class Path:
	def __init__(self,json):
		json["points"] = json.pop("data")
		self.__dict__.update(json)
		self.pointsLength = range(0,len(self.points))
		self.xPoints = [point.point[0] for point in self.points]
		self.yPoints = [point.point[1] for point in self.points]
		
		self.splineX = interpolate.Akima1DInterpolator(self.pointsLength,self.xPoints)
		self.splineY = interpolate.Akima1DInterpolator(self.pointsLength,self.yPoints)
		
	def calculateSpline(self):
		self.splineX = interpolate.Akima1DInterpolator(self.pointsLength,self.xPoints)
		self.splineY = interpolate.Akima1DInterpolator(self.pointsLength,self.yPoints)
		
	def derivative(self, x, deriv=1):
		return [self.splineX.derivative(deriv)(x),
				self.splineY.derivative(deriv)(x)]