from networktables import NetworkTables

class DataPool(object):
	_table = NetworkTables.getTable("data")
	_allPools = []
	def __init__(self, name):
		DataPool._allPools.append(self)
		self._data = []
		self._keys = []
		self._name = name
		
	
	def logData(self, key, o):
		alreadyExists = False
		index = 0
		for item in self._keys:
			if item.equals(key):
				alreadyExists = True
				break;
			index += 1 
			
		if alreadyExists:
			self._data.set(index, o)
		else:
			self._data.add(o)
			self._keys.add(key)
			
	def logInt(self, key, i):
		self.logData(key, i)

	def logBoolean(self, key, b):
		self.logData(key, b)

	def logDouble(self, key, d):
		self.logData(key, d)
		
	@staticmethod
	def collectAllData():
		if not DataPool._allPools:
			return 
		
		for pool in DataPool._allPools:
			if not pool.data.isEmpty():
				poolTable = DataPool._table.getSubTable(pool.name)
				for i in range(pool.data.size()):
					binTable = poolTable.getEntry(pool.keys.get(i))
					binTable.setValue(pool.data.get(i))
	
	@staticmethod			
	def getObjectData(subTableName, valueName):
		data = NetworkTables.getTable("data").getSubTable(subTableName)
		stuff = data.getEntry(valueName)
		return stuff.getValue().getValue()
	
	@staticmethod
	def getStringData(subTableName, valueName):
		return DataPool.getObjectData(subTableName, valueName).ToString()
	
	@staticmethod
	def getDoubleData(subTableName, valueName):
		return float(DataPool.getStringData(subTableName, valueName))
	
	@staticmethod
	def getIntData(subTableName, valueName):
		return int(DataPool.getStringData(subTableName, valueName))
	
	@staticmethod
	def getBooleanData(subTableName, valueName):
		return bool(DataPool.getStringData(subTableName, valueName))

