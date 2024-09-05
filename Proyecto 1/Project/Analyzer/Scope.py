from Include import *

from .Utils import *
from .Symbols import *
from Lace import *

class Scope:
	def __init__(self, parent: 'Scope' = None):
		self.parent: Scope = parent
		self.classes   : BiMap[str, Class]    = BiMap()
		self.functions : BiMap[str, Function] = BiMap()
		self.variables : BiMap[str, Variable] = BiMap()

	def declareClass(self, value: Class, debug: Lace):
		"""Declare a new Class in the current scope."""
		if self.checkClass(value.ID, debug):
			debug << NL() << ERROR() << f"Class [{value.ID}] Redifinition" << END()
			raise Exception()
		value.scope_depth = self.scopeDepth()
		self.classes.add(value.ID, value)
		return True

	def checkClass(self, ID: str, debug: Lace) -> bool:
		"""Look up a Class in the current scope or any parent scope."""
		if ID in self.classes.forward_map.keys():
			return True
		elif self.parent is not None:
			return self.parent.checkClass(ID, debug)
		else:
			return False

	def lookupClass(self, ID: str, debug: Lace):
		"""Look up a Class in the current scope or any parent scope."""
		if ID in self.classes.forward_map.keys():
			return self.classes.getVal(ID)
		elif self.parent is not None:
			return self.parent.lookupClass(ID, debug)
		else:
			debug << NL() << ERROR() << f"Class [{ID}] not declared in this scope" << END()
			raise Exception()

	def declareFunction(self, value: Function, debug: Lace):
		"""Declare a new Function in the current scope."""
		if self.checkFunction(value.ID, debug):
			debug << NL() << ERROR() << f"Function [{value.ID}] Redifinition" << END()
			raise Exception()
		value.scope_depth = self.scopeDepth()
		self.functions.add(value.ID, value)

	def checkFunction(self, ID: str, debug: Lace) -> bool:
		"""Look up a Function in the current scope or any parent scope."""
		if ID in self.functions.forward_map.keys():
			return True
		elif self.parent is not None:
			return self.parent.checkFunction(ID, debug)
		else:
			return False

	def lookupFunction(self, ID: str, debug: Lace) -> Function:
		"""Look up a Function in the current scope or any parent scope."""
		if ID in self.functions.forward_map.keys():
			return self.functions.getVal(ID)
		elif self.parent is not None:
			return self.parent.lookupFunction(ID, debug)
		else:
			debug << NL() << ERROR() << f"Function [{ID}] not declared in this scope" << END()
			raise Exception()

	def declareVariable(self, value: Variable, debug: Lace):
		"""Declare a new Variable in the current scope."""
		if self.checkVariable(value.ID, debug):
			debug << NL() << ERROR() << f"Variable [{value.ID}] Redifinition" << END()
			raise Exception()
		value.scope_depth = self.scopeDepth()
		self.variables.add(value.ID, value)

	def checkVariable(self, ID: str, debug: Lace) -> bool:
		"""Look up a Variable in the current scope or any parent scope."""
		if ID in self.variables.forward_map.keys():
			return True
		elif self.parent is not None:
			return self.parent.checkVariable(ID, debug)
		else:
			return False

	def lookupVariable(self, ID: str, debug: Lace) -> Variable:
		"""Look up a Variable in the current scope or any parent scope."""
		if ID in self.variables.forward_map.keys():
			return self.variables.getVal(ID)
		elif self.parent is not None:
			return self.parent.lookupVariable(ID, debug)
		else:
			debug << NL() << ERROR() << f"Variable [{ID}] not declared in this scope" << END()
			raise Exception()

	def scopeDepth(self) -> int:
		"""Count how deep the current scope is relative to the global scope."""
		depth = 0
		current_scope = self
		while current_scope.parent is not None:
			depth += 1
			current_scope = current_scope.parent
		return depth

class Scope_Tracker:
	def __init__(self, debug: Lace):
		self.global_classes   : BiMap[str, Class]    = BiMap()
		self.global_functions : BiMap[str, Function] = BiMap()
		self.global_variables : BiMap[str, Variable] = BiMap()

		self.debug = debug
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
		self.current_scope.declareClass(value, self.debug)
	def lookupClass(self, value: Class):
		return self.current_scope.lookupClass(value, self.debug)
	def declareFunction(self, value: Function):
		self.current_scope.declareFunction(value, self.debug)
	def lookupFunction(self, ID: str):
		return self.current_scope.lookupFunction(ID, self.debug)
	def declareVariable(self, ID: str):
		self.current_scope.declareVariable(ID, self.debug)
	def checkVariable(self, ID: str):
		return self.current_scope.checkVariable(ID, self.debug)
	def lookupVariable(self, ID: str):
		return self.current_scope.lookupVariable(ID, self.debug)