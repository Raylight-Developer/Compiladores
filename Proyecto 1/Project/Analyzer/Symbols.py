from Include import *

from enum import Enum
import ast

class Type(Enum):
	INT = "int"
	NONE = "nullptr"
	BOOL = "bool"
	LIST = "list"
	VOID = "void"
	FLOAT = "float"
	STRING = "string"
	UNKNOWN = "unknown"

def inferVariableType(code: str):
	if isinstance(code, int):
		return Type.INT
	elif isinstance(code, float):
		return Type.FLOAT
	elif isinstance(code, str):
		return Type.STRING
	else:
		return Type.UNKNOWN

class Var:
	def __init__(self, code: Union[str, int, float, bool, None] = None, type: Type = Type.UNKNOWN):
		self.code = code
		self.type = type
	
	def __str__(self):
		return f"{self.type} [{self.code}]"

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
		self.ID          : str  = None
		self.code        : str  = None
		self.return_type : Type = Type.VOID
		self.scope_depth : int  = 0

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