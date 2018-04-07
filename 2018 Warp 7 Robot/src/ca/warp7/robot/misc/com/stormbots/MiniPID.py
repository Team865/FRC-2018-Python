class MiniPID(object):
	def __init__(self, p, i, d, f=0):
		self._maxIOutput = 0
		self._maxError = 0
		self._errorSum = 0
		self._maxOutput = 0
		self._minOutput = 0
		self._setpoint = 0
		self._lastActual = 0
		self._firstRun = True
		self._reversed = False
		self._outputRampRate = 0
		self._lastOutput = 0
		self._outputFilter = 0
		self._setpointRange = 0
		self._P = p
		self._I = i
		self._D = d
		self._F = f
		self.checkSigns()

	def setP(self, p):
		self._P = p
		self.checkSigns()

	def setI(self, i):
		if self._I != 0:
			self._errorSum = self._errorSum * self._I / i
		if self._maxIOutput != 0:
			self._maxError = self._maxIOutput / i
		self._I = i
		self.checkSigns()

	def setD(self, d):
		self._D = d
		self.checkSigns()

	def setF(self, f):
		self._F = f
		self.checkSigns()

	def setPID(self, p, i, d, f=0):
		self._P = p
		self._D = d
		self._F = f
		self.setI(i)
		self.checkSigns()

	def setMaxIOutput(self, maximum):
		self._maxIOutput=maximum
		if self._I != 0:
			self._maxError = self._maxIOutput / self._I

	def setOutputLimits(self, minimum, maximum=None):
		if maximum is None:
			self.setOutputLimits(-minimum, minimum)
		else:
			if maximum < minimum:
				return 
			self._maxOutput = maximum
			self._minOutput = minimum
			if self._maxIOutput == 0 or self._maxIOutput > (maximum - minimum):
				self.setMaxIOutput(maximum - minimum)

	def setDirection(self, rev):
		self._reversed = rev

	def setSetpoint(self, setpoint):
		self._setpoint = setpoint

	def getOutput1(self, actual, setpoint):
		self._setpoint = setpoint
		if self._setpointRange != 0:
			setpoint = self.constrain(setpoint, actual - self._setpointRange, actual + self._setpointRange)
		error = setpoint - actual
		Foutput = self._F * setpoint
		Poutput = self._P * error
		if self._firstRun:
			self._lastActual = actual
			self._lastOutput = Poutput + Foutput
			self._firstRun = False
		Doutput = -self._D * (actual - self._lastActual)
		self._lastActual = actual
		Ioutput = self._I * self._errorSum
		if self._maxIOutput != 0:
			Ioutput = self.constrain(Ioutput, -self._maxIOutput, self._maxIOutput)
		output = Foutput + Poutput + Ioutput + Doutput
		if self._minOutput != self._maxOutput and not self.bounded(output, self._minOutput, self._maxOutput):
			self._errorSum = error
		elif self._outputRampRate != 0 and not self.bounded(output, self._lastOutput - self._outputRampRate, self._lastOutput + self._outputRampRate):
			self._errorSum = error
		elif self._maxIOutput != 0:
			self._errorSum = self.constrain(self._errorSum + error, -self._maxError, self._maxError)
		else:
			self._errorSum += error
		if self._outputRampRate != 0:
			output = self.constrain(output, self._lastOutput - self._outputRampRate, self._lastOutput + self._outputRampRate)
		if self._minOutput != self._maxOutput:
			output = self.constrain(output, self._minOutput, self._maxOutput)
		if self._outputFilter != 0:
			output = self._lastOutput * self._outputFilter + output * (1 - self._outputFilter)
			
		self._lastOutput = output
		return output

	def getOutput(self, actual=None,setpoint=None):
		if actual is None:
			if setpoint is None:
				return self.getOutput1(self._lastActual, self._setpoint)
			
			return self.getOutput1(self._lastActual, setpoint)
		
		else:
			if setpoint is None:
				return self.getOutput1(actual, self._setpoint)
		
		return self.getOutput1(actual, setpoint)

	def reset(self):
		self._firstRun = True
		self._errorSum = 0

	def setOutputRampRate(self, rate):
		self._outputRampRate = rate

	def setSetpointRange(self, ran):
		self._setpointRange = ran

	def setOutputFilter(self, strength):
		if strength == 0 or self.bounded(strength, 0, 1):
			self._outputFilter = strength

	def constrain(self, value, minn, maxx):
		if value > maxx:
			return maxx
		if value < minn:
			return minn
		return value

	def bounded(self, value, minn, maxx):
		return (minn < value) and (value < maxx)

	def checkSigns(self):
		if self._reversed: # all values should be below zero
			if self._P > 0:
				self._P *= -1
			if self._I > 0:
				self._I *= -1
			if self._D > 0:
				self._D *= -1
			if self._F > 0:
				self._F *= -1
		else: # all values should be above zero
			if self._P < 0:
				self._P *= -1
			if self._I < 0:
				self._I *= -1
			if self._D < 0:
				self._D *= -1
			if self._F < 0:
				self._F *= -1
				
				
if __name__ == "__main__":
	miniPID = MiniPID(0.01, 0, 0.1)
	miniPID.setOutputLimits(327.897)
	target = 11824
	actual = 11824 / 2
	output = 0
	miniPID.setSetpoint(0)
	miniPID.setSetpoint(target)
	print("Target\t\t\tActual\t\tOutput\t\tError\n")
	i = 0
	while i < 1000:
		output = miniPID.getOutput(actual, target)
		actual = actual + output
		print("{:3.2f}\t\t{:3.2f}\t\t{:3.2f}\t\t{:3.2f}\n".format(target, actual, output, (target - actual)))
		i += 1