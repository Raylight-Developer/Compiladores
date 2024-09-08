from Include import *

from .Utils import *
from .Symbols import *
from Lace import *

class Scope:
	def __init__(self, parent: 'Scope' = None):
		self.parent: Scope = parent
		self.classes   : BiMap[str, Class]    = BiMap()
		self.functions : BiMap[None | str, BiMap[str, Function]] = BiMap()
		self.variables : BiMap[None | str, BiMap[str, Variable]] = BiMap()
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

class Tag:
	def __init__(self, ID: str = "", type: Type = Type.NONE):
		self.ID = ID
		self.type = type

	def __eq__(self, other: 'Tag'):
		if self.ID == other.ID and self.type == other.type:
			return True
		return False
	
	def __hash__(self):
		return hash(f"{self.type}.{self.ID}")

	def __str__(self):
		return f"{self.ID} {self.type}"

class Scope_Tracker:
	def __init__(self, debug: Lace):
		self.debug = debug
		
		self.persistent_tree: List[str] = []
		self.scope_stack: List[Dict[Tag, Any]] = []

		self.current_depth = 0
		self.current_scope: Dict[Tag, Any] = {}
		self.scope_stack.append(self.current_scope)
		self.persistent_tree.append("Global {")

	def enterScope(self):
		new_scope = {}
		self.current_depth += 1
		self.persistent_tree.append('    ' * self.current_depth + f"{self.current_depth}" + " {")
		self.scope_stack.append(new_scope)
		self.current_scope = new_scope

	def exitScope(self):
		self.scope_stack.pop()
		self.persistent_tree.append('    ' * self.current_depth + "}")
		self.current_depth -= 1
		self.current_scope = self.scope_stack[-1]

	def declareClass(self, value: Class):
		computed = Tag(value.ID, Type.CLASS)
		if computed not in self.current_scope:
			self.current_scope[computed] = value
			self.persistent_tree.append('    ' * (self.current_depth + 1) + f"cls<{value.ID}> : <{value.ID}>")
		else:
			self.print()
			error(self.debug, f"Class '{value.ID}' Redefinition not allowed")

	def declareFunction(self, value: Function):
		computed = Tag(value.ID, Type.FUNCTION)
		if computed not in self.current_scope:
			self.current_scope[computed] = value
			self.persistent_tree.append('    ' * (self.current_depth + 1) + f"var<{value.ID}> : <{value.ID}>")
		else:
			self.print()
			error(self.debug, f"Function '{value.ID}' Redefinition not allowed")

	def declareVariable(self, value: Variable):
		computed = Tag(value.ID, Type.VARIABLE)
		if computed not in self.current_scope:
			self.current_scope[computed] = value
			self.persistent_tree.append('    ' * (self.current_depth + 1) + f"fun<{value.ID}> : <{value.ID}>")
		else:
			self.print()
			error(self.debug, f"Variable '{value.ID}' Redefinition not allowed")

	def lookupClass(self, ID: str) -> Class:
		computed = Tag(ID, Type.CLASS)
		for scope in reversed(self.scope_stack):
			if computed in scope:
				return scope[computed]
		self.print()
		error(self.debug, f"Class {type(ID)}b'{ID}' not in Scope  {self.current_depth}")

	def lookupFunction(self, ID: str, cls: Class | None = None) -> Function:
		computed = Tag(ID, Type.FUNCTION)
		for scope in reversed(self.scope_stack):
			if cls:
				struct = self.lookupClass(cls.ID)
				for member in struct.member_functions:
					if ID == member.ID:
						return member
			if computed in scope:
				return scope[computed]
		self.print()
		error(self.debug, f"Function '{ID}' not in Scope {cls if cls else 'Global'}")

	def lookupVariable(self, ID: str, cls: Class | None = None) -> Variable:
		computed = Tag(ID, Type.VARIABLE)
		for scope in reversed(self.scope_stack):
			if cls:
				struct = self.lookupClass(cls.ID)
				for member in struct.member_variables:
					if ID == member.ID:
						return member
			if computed in scope:
				return scope[computed]
		self.print()
		error(self.debug, f"Variable '{ID}' not in Scope {cls if cls else 'Global'}")

	def checkClass(self, ID: str) -> bool:
		computed = Tag(ID, Type.CLASS)
		for scope in reversed(self.scope_stack):
			if computed in scope:
				return True
		return False

	def checkFunction(self, ID: str, cls: Class | None = None) -> bool:
		computed = Tag(ID, Type.FUNCTION)
		for scope in reversed(self.scope_stack):
			if cls:
				struct = self.lookupClass(cls.ID)
				for member in struct.member_functions:
					if ID == member.ID:
						return True
			for scope in reversed(self.scope_stack):
				if computed in scope:
					return True
		return False

	def checkVariable(self, ID: str, cls: Class | None = None) -> bool:
		computed = Tag(ID, Type.VARIABLE)
		for scope in reversed(self.scope_stack):
			if cls:
				struct = self.lookupClass(cls.ID)
				for member in struct.member_variables:
					if ID == member.ID:
						return True
			if computed in scope:
				return True
		self.print()
		return False

	def print(self):
		print(f"Current Scope Level: {self.current_depth}")
		print("Scope Stack:")
		for i, scope in enumerate(self.scope_stack):
			print(f"    {i}" + " {")
			for key, val in scope.items():
				print(f"        {key.type}<{key.ID}> : <{val}>")
			print("    }")

		print("\nPersistent Tree:")
		print("    " + "\n    ".join(self.persistent_tree))
		print("    }")