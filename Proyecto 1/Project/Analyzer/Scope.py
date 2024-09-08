from Include import *

from .Utils import *
from .Symbols import *
from Lace import *

class Scope:
	def __init__(self, parent: 'Scope' = None):
		self.parent: Scope = parent
		self.classes   : BiMap[str, Class]    = BiMap()
		self.functions : BiMap[Union[None, str], BiMap[str, Function]] = BiMap()
		self.variables : BiMap[Union[None, str], BiMap[str, Variable]] = BiMap()
		self.functions.add(None, BiMap()) # Non-Member
		self.variables.add(None, BiMap()) # Non-Member

	def declareClass(self, value: Class, debug: Lace):
		"""Declare a new Class in the current scope."""
		if self.checkClass(value.ID, debug):
			error(debug, f"Class [{value.ID}] Redifinition in scope {value}")
		value.scope_depth = self.scopeDepth()
		self.classes.add(value.ID, value)
		self.functions.add(value, BiMap())
		self.variables.add(value, BiMap())
		return True

	def checkClass(self, ID: str, debug: Lace) -> bool:
		"""Look up a Class in the current scope or any parent scope."""
		if ID in self.classes:
			return True
		elif self.parent is not None:
			return self.parent.checkClass(ID, debug)
		else:
			return False

	def lookupClass(self, ID: str, debug: Lace):
		"""Look up a Class in the current scope or any parent scope."""
		if ID in self.classes:
			return self.classes.getVal(ID)
		elif self.parent is not None:
			return self.parent.lookupClass(ID, debug)
		else:
			error(debug, f"\tClass [{ID}] not declared in this scope")

	def printClasses(self):
		for class_scope in self.classes.getKeys():
			print(f"\t{self.classes.getVal(class_scope).ID}")
		if self.parent:
			print("Parent Scope:")
			self.parent.printClasses()
			
	def dumpClasses(self):
		print("Classes in Scope:")
		current_scope = self
		while current_scope:
			current_scope.printClasses()
			current_scope = current_scope.parent
	
	def declareFunction(self, value: Function, parent: Class | None, debug: Lace, scope_offset: int):
		"""Declare a new Function in the current scope."""
		if self.checkFunction(value.ID, parent, debug):
			if self.checkFunction(value.ID, parent.parent, debug):
				parent_func = self.lookupFunction(value.ID, parent.parent, debug)
				if parent_func.inherited:
					error(debug, f"Function [{value.ID}] Redifinition in scope {parent}")

		value.scope_depth = self.scopeDepth() + scope_offset
		if parent == None:
			self.functions.getVal(None).add(value.ID, value)
		else:
			parent_scope = self.goUpTree(self.scopeDepth() - parent.scope_depth - 1 + scope_offset)
			value.scope_depth = self.scopeDepth() - parent.scope_depth - 1 + scope_offset
			if parent.ID not in parent_scope.functions:
				parent_scope.functions.add(parent.ID, BiMap())
			parent_scope.functions.getVal(parent.ID).add(value.ID, value)

	def checkFunction(self, ID: str, parent: Class | None, debug: Lace) -> bool:
		"""Look up a Function in the current scope or any parent scope."""
		if parent == None:
			if ID in self.functions.getVal(None):
				return True
			elif self.parent is not None:
				return self.parent.checkFunction(ID, parent, debug)
		else:
			for class_scope in self.functions.getKeys():
				if class_scope == parent.ID or class_scope == None:
					if ID in self.functions.getVal(class_scope):
						return True
					elif self.parent is not None:
						return self.parent.checkFunction(ID, parent, debug)
		return False

	def lookupFunction(self, ID: str, parent: Class | None, debug: Lace) -> Function:
		"""Look up a Function in the current scope or any parent scope."""
		if parent == None:
			if ID in self.functions.getVal(parent):
				return self.functions.getVal(parent).getVal(ID)
			elif self.parent is not None:
				return self.parent.lookupFunction(ID, parent, debug)
		else:
			for class_scope in self.functions.getKeys():
				if class_scope == parent.ID or class_scope == None:
					if ID in self.functions.getVal(class_scope):
						return self.functions.getVal(class_scope).getVal(ID)
					elif self.parent is not None:
						return self.parent.lookupFunction(ID, parent, debug)
		
		error(debug, f"Function [{ID}] not declared in this scope")

	def printFunctions(self):
		for class_scope in self.functions.getKeys():
			for function in self.functions.getVal(class_scope).getKeys():
				print(f"\t{self.functions.getVal(class_scope).getVal(function)}'")
		if self.parent:
			print("Parent Scope:")
			self.parent.printFunctions()
			
	def dumpFunctionScope(self):
		print("Functions in Scope:")
		current_scope = self
		while current_scope:
			current_scope.printFunctions()
			current_scope = current_scope.parent

	def declareVariable(self, value: Variable, parent: Class | None, debug: Lace, scope_offset: int):
		"""Declare a new Variable in the current scope."""
		if self.checkVariable(value.ID, parent, debug):
			if self.checkVariable(value.ID, parent.parent, debug):
				parent_var = self.lookupVariable(value.ID, parent.parent, debug)
				if parent_var.inherited:
					error(debug, f"Variable [{value.ID}] Redifinition in scope {parent}")

		value.scope_depth = self.scopeDepth() + scope_offset
		if parent == None:
			self.variables.getVal(None).add(value.ID, value)
		else:
			parent_scope = self.goUpTree(self.scopeDepth() - parent.scope_depth - 1 + scope_offset)
			value.scope_depth = self.scopeDepth() - parent.scope_depth - 1 + scope_offset
			if parent.ID not in parent_scope.variables:
				parent_scope.variables.add(parent.ID, BiMap())
			parent_scope.variables.getVal(parent.ID).add(value.ID, value)

	def checkVariable(self, ID: str, parent: Class | None, debug: Lace) -> bool:
		"""Look up a Variable in the current scope or any parent scope."""
		if parent == None:
			if ID in self.variables.getVal(None):
				return True
			elif self.parent is not None:
				return self.parent.checkVariable(ID, parent, debug)
		else:
			for class_scope in self.variables.getKeys():
				if class_scope == parent.ID or class_scope == None:
					if ID in self.variables.getVal(class_scope):
						return True
					elif self.parent is not None:
						return self.parent.checkVariable(ID, parent, debug)
		return False

	def lookupVariable(self, ID: str, parent: Class | None, debug: Lace) -> Variable:
		"""Look up a Variable in the current scope or any parent scope."""
		if parent == None:
			if ID in self.variables.getVal(parent):
				return self.variables.getVal(parent).getVal(ID)
			elif self.parent is not None:
				return self.parent.lookupVariable(ID, parent, debug)
		else:
			for class_scope in self.variables:
				if class_scope == parent.ID or class_scope == None:
					if ID in self.variables.getVal(class_scope).getVal(class_scope):
						return self.variables.getVal(class_scope).getVal(ID)
					elif self.parent is not None:
						return self.parent.lookupVariable(ID, parent, debug)
		error(debug, f"Variable [{ID}] not declared in this scope")

	def scopeDepth(self) -> int:
		"""Count how deep the current scope is relative to the global scope."""
		depth = 0
		current_scope = self
		while current_scope.parent is not None:
			depth += 1
			current_scope = current_scope.parent
		return depth
	
	def goUpTree(node, n: int):
		current = node
		steps = 0

		while current is not None and steps < n:
			current = current.parent
			steps += 1

		return current

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
			error(self.debug, "Attempted to exit global scope")

	def declareClass(self, struct: Class):
		self.current_scope.declareClass(struct, self.debug)
	def checkClass(self, ID: str):
		return self.current_scope.checkClass(ID, self.debug)
	def lookupClass(self, ID: str):
		if self.checkClass(ID):
			return self.current_scope.lookupClass(ID, self.debug)
		else:
			error(self.debug, f"Class '{ID}' does Not Exist")
	def declareFunction(self, function: Function, parent: Class | None, scope_offset: int = 0):
		self.current_scope.declareFunction(function, parent, self.debug, scope_offset)
	def checkFunction(self, ID: str, parent: Class | None):
		return self.current_scope.checkFunction(ID, parent, self.debug)
	def lookupFunction(self, ID: str, parent: Class | None):
		if self.checkFunction(ID, parent):
			return self.current_scope.lookupFunction(ID, parent, self.debug)
		else:
			print(f"Scope: {parent.ID}")
			self.current_scope.dumpClasses()
			self.current_scope.dumpFunctionScope()
			error(self.debug, f"Function '{ID}' does Not Exist in scope {parent.ID if parent else 'Global'}")
	def declareVariable(self, variable: Variable, parent: Class | None, scope_offset: int = 0):
		self.current_scope.declareVariable(variable, parent, self.debug, scope_offset)
	def checkVariable(self, ID: str, parent: Class | None):
		return self.current_scope.checkVariable(ID, parent, self.debug)
	def lookupVariable(self, ID: str, parent: Class | None):
		if self.checkVariable(ID, parent):
			return self.current_scope.lookupVariable(ID, parent, self.debug)
		else:
			error(self.debug, f"Variable '{ID}' does Not Exist in scope {parent.ID if parent else 'Global'}")