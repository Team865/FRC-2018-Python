from multiprocessing import Process
from time import time as NanoTime
from time import sleep
from misc.Util import Runnable

class RTS(Process):
	def __init__(self, name, TARGET_HZ=60):
		Process.__init__(self)
		
		self._tasks = []
		self._running = False
		self._delta = 0.0
		self._OPTIMAL_TIME = 1000000000.0 / TARGET_HZ
		self._name = name
		self._TARGET_HZ = TARGET_HZ
		self._hz = TARGET_HZ

	def run(self):		
		if not self._running:
			self._running = True
			hzcont = 0
			lastHzTime = 0
			lastLoopTime = NanoTime()
			while self._running:
				now = NanoTime()
				updateLength = now - lastLoopTime
				lastLoopTime = now
				self._delta = updateLength / (self._OPTIMAL_TIME)
				lastHzTime += updateLength
				hzcont += 1
				if lastHzTime >= 1000000000:
					lastHzTime = 0
					self._hz = hzcont
					hzcont = 0
				
				for task in self._tasks:
					task.run()
				
				sleep((lastLoopTime - NanoTime() + self._OPTIMAL_TIME) / 1000000.0)
		else:
			print("RTS is already running for object:", self._name)
	
	def terminate(self, *args, **kwargs):
		self._running = False
		return Process.terminate(self, *args, **kwargs)

	def stop(self):
		self._running = False

	def addTask(self, func, args=[]):
		task = Runnable(func,args)
		self._tasks.append(task)

	def getHz(self):
		return self._hz

	def getDelta(self):
		return self._delta

	def isRunning(self):
		return self._running

	def getTargetHz(self):
		return self._TARGET_HZ

	def getName(self):
		return self._name