from Include import *

from Utils import *
from Symbols import *

class Scope:
	def __init__(self, id: str):
		self.id: str = id
		self.symbols = {}

class Scope_Tracker:
	def __init__(self):
		self.global_classes   : BiMap[str, Class]    = {}
		self.global_functions : BiMap[str, Function] = {}
		self.global_variables : BiMap[str, Variable] = {}

	def addGlobalClass(self, value: Class):
		pass

	def addGlobalFunction(self, value: Function):
		pass

	def addGlobalVariable(self, value: Variable):
		pass

	def enterScope(self):
		pass

	def exitScope(self):
		pass

	def addScope(self):
		pass

	def lookupScope(self, var_name):
		pass