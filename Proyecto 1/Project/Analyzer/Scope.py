from Include import *

from .Utils import *
from .Symbols import *
from Lace import *

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
		self.depth_count: Dict[int, int] = {}
	
		self.current_scope: Dict[Tag, Any] = {}
		self.scope_stack.append(self.current_scope)
		self.persistent_tree.append("Global {")

	def enterScope(self):
		self.depth_count[self.current_depth] = self.depth_count.get(self.current_depth, 0) + 1

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
			value.scope_depth = self.current_depth
			value.scope_depth_count = self.depth_count.get(self.current_depth, 0)
			self.current_scope[computed] = value
			self.persistent_tree.append('    ' * (self.current_depth + 1) + f"cls<{value.ID}> : <{value.ID}>")
		else:
			self.print()
			error(self.debug, f"Class '{value.ID}' Redefinition not allowed")

	def declareFunction(self, value: Function):
		computed = Tag(value.ID, Type.FUNCTION)
		if computed not in self.current_scope:
			value.scope_depth = self.current_depth
			value.scope_depth_count = self.depth_count.get(self.current_depth, 0)
			self.current_scope[computed] = value
			self.persistent_tree.append('    ' * (self.current_depth + 1) + f"fun<{value.ID}> : <{value.ID}>")
		else:
			self.print()
			error(self.debug, f"Function '{value.ID}' Redefinition not allowed")

	def declareVariable(self, value: Variable):
		computed = Tag(value.ID, Type.VARIABLE)
		if computed not in self.current_scope:
			value.scope_depth = self.current_depth
			value.scope_depth_count = self.depth_count.get(self.current_depth, 0)
			self.current_scope[computed] = value
			self.persistent_tree.append('    ' * (self.current_depth + 1) + f"var<{value.ID}> : <{value.ID}>")
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
				for member in cls.member_functions:
					if ID == member.ID:
						return member
			if computed in scope:
				return scope[computed]
		self.print()
		for scope in reversed(self.scope_stack):
			if cls:
				for member in cls.member_variables:
					print(f"if {type(ID)}{ID} == {type(member.ID)}{member.ID}")
			if computed in scope:
				print(f"{computed}")
		error(self.debug, f"Function '{ID}' not in Scope {cls.ID if cls else 'Global'}")

	def lookupVariable(self, ID: str, cls: Class | None = None) -> Variable:
		computed = Tag(ID, Type.VARIABLE)
		for scope in reversed(self.scope_stack):
			if cls:
				for member in cls.member_variables:
					if ID == member.ID:
						return member
			if computed in scope:
				return scope[computed]
		self.print()
		for scope in reversed(self.scope_stack):
			if cls:
				for member in cls.member_variables:
					print(f"if {type(ID)}{ID} == {type(member.ID)}{member.ID}")
			if computed in scope:
				print(f"{computed}")
		error(self.debug, f"Variable '{ID}' not in Scope {cls.ID if cls else 'Global'}")

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
				for member in cls.member_functions:
					if ID == member.ID:
						return False
			if computed in scope:
				return True
		return False

	def checkVariable(self, ID: str, cls: Class | None = None) -> bool:
		computed = Tag(ID, Type.VARIABLE)
		for scope in reversed(self.scope_stack):
			if cls:
				for member in cls.member_variables:
					if ID == member.ID:
						return False
			if computed in scope:
				return True
		return False

	def dumpScope(self):
		dump: List[str] = []
		dump.append(f"Current Scope Level: {self.current_depth}")
		dump.append("Scope Stack:")
		for i, scope in enumerate(self.scope_stack):
			dump.append(f"    {i}" + " {")
			for key, val in scope.items():
				dump.append(f"        {key.type}<{key.ID}> : <{val}>")
			dump.append("    }")
		return "\n" + "\n".join(dump)
	
	def dumpScopeTree(self):
		dump: List[str] = []
		dump.append("\nPersistent Tree:")
		dump.append("    " + "\n    ".join(self.persistent_tree))
		dump.append("    }")
		return "\n" + "\n".join(dump)

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