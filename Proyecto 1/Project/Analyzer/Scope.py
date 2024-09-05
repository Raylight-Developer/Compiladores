from Include import *

from .Utils import *
from .Symbols import *

class Scope:
	def __init__(self, parent: 'Scope' = None):
		self.parent: Scope = parent
		self.classes   : BiMap[str, Class]    = BiMap()
		self.functions : BiMap[str, Function] = BiMap()
		self.variables : BiMap[str, Variable] = BiMap()

	def declareClass(self, value: Class):
		"""Declare a new Class in the current scope."""
		if self.classes.get_value(value):
			raise KeyError(f"Class [{value.ID}] already declared in this scope")
		value.scope_depth = self.scopeDepth()
		self.classes.add(value.ID, value)

	def lookupClass(self, ID: str):
		"""Look up a Class in the current scope or any parent scope."""
		if ID in self.classes.forward_map.keys():
			return self.classes.get_value(ID)
		elif self.parent is not None:
			return self.parent.lookupClass(ID)
		else:
			raise KeyError(f"Class [{ID.ID}] not declared in this scope")

	def declareFunction(self, value: Function):
		"""Declare a new Function in the current scope."""
		if self.functions.get_value(value):
			raise KeyError(f"Function [{value.ID}] already declared in this scope")
		value.scope_depth = self.scopeDepth()
		self.functions.add(value.ID, value)

	def lookupFunction(self, ID: str) -> Function:
		"""Look up a Function in the current scope or any parent scope."""
		if ID in self.functions.forward_map.keys():
			return self.functions.get_value(ID)
		elif self.parent is not None:
			return self.parent.lookupFunction(ID)
		else:
			raise KeyError(f"Function [{ID.ID}] not declared in this scope")

	def declareVariable(self, value: Variable):
		"""Declare a new Variable in the current scope."""
		if self.variables.get_value(value):
			raise KeyError(f"Variable [{value.ID}] already declared in this scope")
		value.scope_depth = self.scopeDepth()
		self.variables.add(value.ID, value)

	def checkVariable(self, ID: str) -> bool:
		"""Look up a Variable in the current scope or any parent scope."""
		if ID in self.variables.forward_map.keys():
			return True
		elif self.parent is not None:
			return self.parent.checkVariable(ID)
		else:
			return False

	def lookupVariable(self, ID: str) -> Variable:
		"""Look up a Variable in the current scope or any parent scope."""
		if ID in self.variables.forward_map.keys():
			return self.variables.get_value(ID)
		elif self.parent is not None:
			return self.parent.lookupVariable(ID)
		else:
			raise KeyError(f"Variable [{ID}] not declared in this scope")

	def scopeDepth(self) -> int:
		"""Count how deep the current scope is relative to the global scope."""
		depth = 0
		current_scope = self
		while current_scope.parent is not None:
			depth += 1
			current_scope = current_scope.parent
		return depth

class Scope_Tracker:
	def __init__(self):
		self.global_classes   : BiMap[str, Class]    = BiMap()
		self.global_functions : BiMap[str, Function] = BiMap()
		self.global_variables : BiMap[str, Variable] = BiMap()

		self.global_scope = Scope()
		self.current_scope = self.global_scope

	def enterScope(self):
		self.current_scope = Scope(self.current_scope)

	def exitScope(self):
		if self.current_scope.parent is not None:
			self.current_scope = self.current_scope.parent
		else:
			raise RuntimeError("Attempted to exit global scope")

	def declareClass(self, value: Class):
		self.current_scope.declareClass(value)
	def lookupClass(self, value: Class):
		return self.current_scope.lookupClass(value)
	def declareFunction(self, value: Function):
		self.current_scope.declareFunction(value)
	def lookupFunction(self, ID: str):
		return self.current_scope.lookupFunction(ID)
	def declareVariable(self, ID: str):
		self.current_scope.declareVariable(ID)
	def checkVariable(self, ID: str):
		return self.current_scope.checkVariable(ID)
	def lookupVariable(self, ID: str):
		return self.current_scope.lookupVariable(ID)