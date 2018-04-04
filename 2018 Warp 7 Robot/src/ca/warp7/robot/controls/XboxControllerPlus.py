from wpilib import XboxController

class XboxControllerPlus():
	def __init__(self, port):
		self._controller = XboxController(port)		
		self._a = False
		self._b = False
		self._x = False
		self._y = False
		self._lb = False
		self._rb = False
		self._lt = False
		self._rt = False
		self._ls = False
		self._rs = False
		self._start = False
		self._back = False
		self._dpad = -1
		
	def getAButton(self):
		a = self._a
		b = self._controller.getAButton()
		self._a = b
		if b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
			
	def getBButton(self):
		a = self._b
		b = self._controller.getBButton()
		self._b = b
		if b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
	
	def getXButton(self):
		a = self._x
		b = self._controller.getXButton()
		self._x = b
		if b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
			
	def getYButton(self):
		a = self._y
		b = self._controller.getYButton()
		self._y = b
		if b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
			
	def getBumper(self, h):
		if h == Hand.kLeft:
			a = self._lb
		else:
			a = self._rb
		b = self._controller.getBumper(h)
		if h == Hand.kLeft:
			self._lb = b
		else:
			self._rb = b
			
		if b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
			
	def getTrigger(self, h):
		if h == Hand.kLeft:
			a = self._lt
		else:
			a = self._rt
		b = self._controller.getTriggerAxis(h) >= 0.5
		if h == Hand.kLeft:
			self._lt = b
		else:
			self._rt = b
		if b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
			
	def getStickButton(self, h):
		if h == Hand.kLeft:
			a = self._ls
		else:
			a = self._rs
		b = self._controller.getStickButton(h)
		if h == Hand.kLeft:
			self._ls = b
		else:
			self._rs = b
		if _b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
			
	def getStartButton(self):
		a = self._start
		b = self._controller.getStartButton()
		self._start = b
		if b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
			
	def getBackButton(self):
		a = self._back
		b = self._controller.getBackButton()
		self._back = b
		if b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
			
	def getDpad(self, value):
		a = self._dpad
		b = self._controller.getPOV(0)
		self._dpad = b
		if b != a:
			if b:
				return PRESSED
			else:
				return RELEASED
		elif b:
			return DOWN
		else:
			return UP
			
	def setRumble(self, type, d):
		self._controller.setRumble(type, d)

	def getX(self, hand):
		return self._controller.getX(hand)

	def getY(self, hand):
		return self._controller.getY(hand)