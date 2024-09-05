from Include import *
from enum import Enum

class Type(Enum):
	INT = "int"
	VOID = "void"
	FLOAT = "float"
	STRING = "string"
	UNKNOWN = "unknown"

class Variable:
	def __init__(self):
		self.ID          : str  = None
		self.type        : Type = Type.UNKNOWN
		self.code        : str  = None
		self.scope_depth : int = 0

class Function_Parameter:
	def __init__(self):
		self.ID   : str  = None
		self.type : Type = Type.UNKNOWN

class Function:
	def __init__(self):
		self.ID          : str = None
		self.code        : str = None
		self.return_type : str = Type.VOID
		self.scope_depth : int = 0

		self.variables  : List[Variable]           = []
		self.parameters : List[Function_Parameter] = []

class Class:
	def __init__(self):
		self.ID          : str   = None
		self.code        : str   = None
		self.parent      : Class = None
		self.scope_depth : int   = 0

		self.initializer      : Function       = None
		self.member_functions : List[Function] = []
		self.member_variables : List[Variable] = []