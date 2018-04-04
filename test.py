import re

def string_checker(a):
	return (a[0] == '"' and a[-1] == '"') or (a[0] == "'" and a[-1] == "'") 

class Dummy:
	pass

re1='((?:[a-z][a-z0-9_]*))'	# Variable Name 1
re2='(\\s+)'	# White Space 1
re3='(=)'	# Any Single Character 1
re4='(\\s+)'	# White Space 2
re5='((?:[a-z][a-z0-9_]*))'	# Variable Name 2
re6='(\\s+)'	# White Space 3
re7='(\\(.*\\))'	# Round Braces 1
re8='([^/]+$)'	# Wildcard 1

METHOD_CALL_SET = re.compile(re1+re2+re3+re4+re5+re6+re7,re.IGNORECASE|re.DOTALL)
METHOD_CALL = re.compile(re1+re2+re7,re.IGNORECASE|re.DOTALL)
VAR_SET = re.compile(re1+re2+re3+re4+re8,re.IGNORECASE|re.DOTALL)
	
class AutoReader:
	def __init__(self,fname):
		if not fname.endswith('.auto'):
			raise Exception("Not an auto file!")
		with open(fname, 'r') as f:
			self.autoInstructions = f.readlines()
		self.currentInstruction = 0
		self.dummyClass = Dummy()
		self.customFunc = CustomFunc(self)
	
	def runAuto(self):
		while self.currentInstruction < len(self.autoInstructions):
			instruction = self.autoInstructions[self.currentInstruction]
			print("Instruction: {}".format(instruction))
			self.run_instruction(instruction)
			self.currentInstruction += 1
			
	def run_instruction(self,instruction):
		m = METHOD_CALL.search(instruction)
		if m:
			a = m.group(1)
			b = m.group(3)[1:-1].split(',')
			for i in range(len(b)):
				if not (b[i].isdigit() or string_checker(b[i])):
					b[i] = re.sub(re1, 'self.dummyClass.'+b[i], b[i])
			b = "{}({})".format(a, ','.join(b))
			eval(b)
			
		else:
			m = METHOD_CALL_SET.search(instruction)
			if m:
				a = m.group(1)
				b = m.group(7)[1:-1].split(',')
				for i in range(len(b)):
					if not (b[i].isdigit() or string_checker(b[i])):
						b[i] = re.sub(re1, 'self.dummyClass.'+b[i], b[i])
				b = "({})".format(','.join(b))
				
			else:
				m = VAR_SET.search(instruction)
				if m:
					a = m.group(1)
					b = m.group(5)
				else:
					eval("self.customFunc."+instruction)
					return
			self.dummyClass.__dict__[a] = eval(b)
	
class CustomFunc:
	def __init__(self, autoReader):
		self.autoReader = autoReader
	
	def jump(self,a):
		self.autoReader.currentInstruction = a-2
		
	def add(self,*argv):
		a=0
		for key in argv:
			a += key
		return a
		
ar = AutoReader("wow.auto")

ar.runAuto()