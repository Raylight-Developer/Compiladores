from Include import *

from Lace import *
from enum import Enum

class Type(Enum):
	INT = "int"
	NONE = "nullptr"
	BOOL = "bool"
	LIST = "list"
	VOID = "void"
	FLOAT = "float"
	STRING = "string"

	CLASS = "class"
	FUNCTION = "function"
	VARIABLE = "variable"

	UNKNOWN = "unknown"

def inferVariableType(code: str):
	if not code:
		return Type.NONE
	if isinstance(code, int) or code.isdigit():
		return Type.INT
	elif isinstance(code, float) or is_float(code):
		return Type.FLOAT
	elif isinstance(code, bool) or is_bool(code):
		return Type.BOOL
	elif isinstance(code, str) or is_bool(code):
		return Type.STRING
	else:
		return Type.UNKNOWN

def operationType(debug: Lace, left: 'Container', operator: str, right: 'Container'):
	if left.type == Type.INT and right.type == Type.INT:
		return Type.INT
	elif left.type == Type.FLOAT and right.type == Type.INT:
		return Type.FLOAT
	elif left.type == Type.INT and right.type == Type.FLOAT:
		return Type.FLOAT
	elif left.type == Type.FLOAT and right.type == Type.FLOAT:
		return Type.FLOAT
	elif left.type == Type.VARIABLE and right.type == Type.VARIABLE:
		return operationType(debug, left.data, operator, right.data)

	elif left.type == Type.VARIABLE and right.type != Type.VARIABLE:
		return operationType(debug, left.data, operator, right)
	elif left.type != Type.VARIABLE and right.type == Type.VARIABLE:
		return operationType(debug, left, operator, right.data)

	else:
		error(debug, f"Cannot operate different Types [{left.type}] {operator} [{right.type}]")

class Container:
	def __init__(self, code: Union[str, int, float, bool, 'Class', 'Function', 'Variable', None], type: Type):
		self.data = code
		self.type = type

	def getCode(self):
		if self.type == Type.VARIABLE:
			return self.data.code
		else:
			return self.data
	
	def __str__(self):
		return f"<{self.type}>({self.data})"

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