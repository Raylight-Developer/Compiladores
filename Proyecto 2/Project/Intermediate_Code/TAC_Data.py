from Include import *
from Lace import *

from .Classes import *

class Tac_Variable:
	def __init__(self):
		self.ID   : str = None
		self.name : str = None

		self.member : Tac_Class = None

		self.instance : Tac_Class = None

class Tac_Function_Parameter:
	def __init__(self):
		self.ID   : str = None
		self.name : str = None

		self.function : Tac_Function = None

class Tac_Function:
	def __init__(self):
		self.ID   : str = None
		self.name : str = None

		self.return_ID: str = None

		self.member : Tac_Class = None
		self.parameters : List[Tac_Function_Parameter] = []

	def lookupParameter(self, name: str) -> Tac_Function_Parameter:
		for param in self.parameters:
			if param.name == name:
				return param
		return None

class Tac_Class:
	def __init__(self):
		self.name : str = None
		self.code : ANT_ClassBody = None

		self.extends : Tac_Class = None

		self.initializer      : Tac_Function       = None
		self.member_functions : List[Tac_Function] = []
		self.member_variables : List[Tac_Variable] = []

	def lookupFunction(self, name: str):
		for member in self.member_functions:
			if member.name == name:
				return member
		#if self.extends:
		#	return self.extends.lookupFunction(name)
		return None

	def lookupVariable(self, name: str):
		for member in self.member_variables:
			if member.name == name:
				return member
		#if self.extends:
		#	return self.extends.lookupVariable(name)
		return None

class Tac_Scope_Tracker:
	def __init__(self):
		self.scope_stack: List[Dict[str, Union[Tac_Class, Tac_Function, Tac_Variable]]] = []

		self.current_scope: Dict[str, Union[Tac_Class, Tac_Function, Tac_Variable]] = {}
		self.scope_stack.append(self.current_scope)

	def enter(self):
		new_scope = {}
		self.scope_stack.append(new_scope)
		self.current_scope = new_scope

	def exit(self):
		self.scope_stack.pop()
		self.current_scope = self.scope_stack[-1]

	def declareClass(self, value: Tac_Class):
		self.current_scope["cls;" + value.name] = value

	def declareFunction(self, value: Tac_Function):
		self.current_scope["fun;" + value.name] = value

	def declareVariable(self, value: Tac_Variable):
		self.current_scope["var;" + value.name] = value

	def lookupClass(self, name: str) -> Tac_Class:
		for scope in reversed(self.scope_stack):
			if f"cls;{name}" in scope:
				return scope[f"cls;{name}"]
		raise Exception(f"Class '{name}' not in Scope")

	def lookupFunction(self, name: str, cls: Union[Tac_Class, Tac_Variable, None] = None) -> Tac_Function:
		for scope in reversed(self.scope_stack):
			if isinstance(cls, Tac_Class):
				for member in cls.member_functions:
					if name == member.name:
						return member
			elif isinstance(cls, Tac_Variable):
				for member in cls.instance.member_functions:
					if name == member.name:
						return member
			if f"fun;{name}" in scope:
				return scope[f"fun;{name}"]
		raise Exception(f"Function '{name}' not in Scope {cls.name if cls else 'Global'}")

	def lookupVariable(self, name: str, cls: Tac_Class | None = None) -> Tac_Variable:
		for scope in reversed(self.scope_stack):
			if cls:
				for member in cls.member_variables:
					if name == member.name:
						return member
			if f"var;{name}" in scope:
				return scope[f"var;{name}"]
		raise Exception(f"Variable '{name}' not in Scope {cls.name if cls else 'Global'}")