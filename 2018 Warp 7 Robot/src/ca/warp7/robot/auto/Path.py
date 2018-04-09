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
		self.splineXDeriv1 = self.splineX.derivative(1)
		self.splineYDeriv1 = self.splineY.derivative(1)
		self.splineXDeriv2 = self.splineX.derivative(2)
		self.splineYDeriv2 = self.splineY.derivative(2)
		
	def derivative1(self, x):
		return [self.splineXDeriv1(x),
				self.splineYDeriv1(x)]
		
	def derivative2(self, x):
		return [self.splineXDeriv2(x),
				self.splineYDeriv2(x)]