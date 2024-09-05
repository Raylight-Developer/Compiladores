from Include import *

from Utils import *
from Symbols import *

class Scope:
	def __init__(self, parent: 'Scope' = None):
		self.parent: Scope = parent
		self.classes   : BiMap[str, Class]    = {}
		self.functions : BiMap[str, Function] = {}
		self.variables : BiMap[str, Variable] = {}

	def declareClass(self, value: Class):
		"""Declare a new Class in the current scope."""
		if value in self.classes:
			raise KeyError(f"Class [{value.ID}] already declared in this scope")
		value.scope_depth = self.scopeDepth()
		self.classes[value.ID] = value

	def lookupClass(self, value: Class):
		"""Look up a Class in the current scope or any parent scope."""
		if value in self.classes:
			return self.classes[value.ID]
		elif self.parent is not None:
			return self.parent.lookupClass(value)
		else:
			raise KeyError(f"Class [{value.ID}] not declared in this scope")

	def declareFunction(self, value: Function):
		"""Declare a new Function in the current scope."""
		if value in self.functions:
			raise KeyError(f"Function [{value.ID}] already declared in this scope")
		value.scope_depth = self.scopeDepth()
		self.functions[value.ID] = value

	def lookupFunction(self, value: Function):
		"""Look up a Function in the current scope or any parent scope."""
		if value in self.functions:
			return self.functions[value.ID]
		elif self.parent is not None:
			return self.parent.lookupFunction(value)
		else:
			raise KeyError(f"Function [{value.ID}] not declared in this scope")

	def declareVariable(self, value: Variable):
		"""Declare a new Variable in the current scope."""
		if value in self.variables:
			raise KeyError(f"Variable [{value.ID}] already declared in this scope")
		value.scope_depth = self.scopeDepth()
		self.variables[value.ID] = value

	def lookupVariable(self, value: Variable):
		"""Look up a Variable in the current scope or any parent scope."""
		if value in self.variables:
			return self.variables[value.ID]
		elif self.parent is not None:
			return self.parent.lookupVariable(value)
		else:
			raise KeyError(f"Variable [{value.ID}] not declared in this scope")

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
		self.global_classes   : BiMap[str, Class]    = {}
		self.global_functions : BiMap[str, Function] = {}
		self.global_variables : BiMap[str, Variable] = {}

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
	def lookupFunction(self, value: Function):
		return self.current_scope.lookupFunction(value)
	def declareVariable(self, value: Variable):
		self.current_scope.declareVariable(value)
	def lookupVariable(self, value: Variable):
		return self.current_scope.lookupVariable(value)