from Include import *

from CompiScript.CompiscriptParser import CompiscriptParser

from Lace import *

class Type(Enum):
	INT = "int"
	NONE = "nullptr"
	BOOL = "bool"
	VOID = "void"
	ARRAY = "array"
	FLOAT = "float"
	STRING = "string"

	CLASS = "class"
	FUNCTION = "function"
	VARIABLE = "variable"
	MEMBER_POINTER = "this."

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
	if isinstance(left, Container) and isinstance(right, Container):
		if left.type == Type.INT and right.type == Type.INT:
			return Type.INT
		if left.type == Type.FLOAT and right.type == Type.INT:
			return Type.FLOAT
		if left.type == Type.INT and right.type == Type.FLOAT:
			return Type.FLOAT
		if left.type == Type.FLOAT and right.type == Type.FLOAT:
			return Type.FLOAT

		if left.type == Type.FLOAT and right.type == Type.STRING:
			return Type.STRING
		if left.type == Type.STRING and right.type == Type.FLOAT:
			return Type.STRING
		if left.type == Type.INT and right.type == Type.STRING:
			return Type.STRING
		if left.type == Type.STRING and right.type == Type.INT:
			return Type.STRING

		if left.type == Type.VARIABLE and right.type == Type.VARIABLE:
			return operationType(debug, Container(left.getCode(), left.data.type), operator, Container(right.getCode(), right.data.type))
		if left.type == Type.VARIABLE and right.type != Type.VARIABLE:
			return operationType(debug, Container(left.getCode(), left.data.type), operator, right)
		if left.type != Type.VARIABLE and right.type == Type.VARIABLE:
			return operationType(debug, left, operator, Container(right.getCode(), right.data.type))

		error(debug, f"Cannot operate different Types <{left.type}>({left.getCode()}) {operator} <{right.type}>({right.getCode()})")
	error(debug, f"Cannot operate Unkown Types {type(left)}({left}) {operator} {type(right)}({right})")

T = TypeVar('T')
class Container(Generic[T]):
	def __init__(self, data: Union[str, int, float, bool, 'Class', 'Function', 'Variable', None], type: Type):
		self.data = data
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
		self.ctx         : CompiscriptParser.VariableContext = None

		self.ID          : str  = None
		self.type        : Type = Type.UNKNOWN
		self.code        : str  = None
		self.scope_depth : int  = 0

		self.member     : Class = None
		self.class_type : Class = None

	def __str__(self):
		return f"Variable {self.ID}"

class Function_Parameter:
	def __init__(self):
		self.ID   : str  = None
		self.type : Type = Type.UNKNOWN

		self.function : Function = None

	def __str__(self):
		return f"Function Parameter {self.ID}"

class Function:
	def __init__(self):
		self.ctx         : CompiscriptParser.FunctionContext = None

		self.ID          : str  = None
		self.code        : str  = None
		self.return_type : Type = Type.VOID
		self.scope_depth : int  = 0

		self.member : Class  = None
		self.variables  : List[Variable]           = []
		self.parameters : List[Function_Parameter] = []

	def __str__(self):
		return f"Function {self.ID}"

class Class:
	def __init__(self):
		self.ctx         : CompiscriptParser.ClassDeclContext = None

		self.ID          : str   = None
		self.code        : str   = None
		self.parent      : Class = None
		self.scope_depth : int   = 0

		self.initializer      : Function       = None
		self.member_functions : List[Function] = []
		self.member_variables : List[Variable] = []

	def checkFunction(self, ID: str):
		for member in self.member_functions:
			if member.ID == ID:
				return True
		return False

	def checkVariable(self, ID: str):
		for member in self.member_variables:
			if member.ID == ID:
				return True
		return False

	def lookupFunction(self, ID: str):
		for member in self.member_functions:
			if member.ID == ID:
				return member

	def lookupVariable(self, ID: str):
		for member in self.member_variables:
			if member.ID == ID:
				return member

	def __str__(self):
		return f"Class {self.ID}"