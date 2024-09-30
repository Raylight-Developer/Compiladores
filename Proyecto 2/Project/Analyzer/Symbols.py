from Include import *

from CompiScript.CompiscriptParser import CompiscriptParser

from Lace import *

class Type(Enum):
	INT = "int"
	NONE = "null"
	BOOL = "bool"
	VOID = "void"
	ARRAY = "array"
	FLOAT = "float"
	STRING = "string"

	CLASS = "class"
	FUNCTION = "function"
	VARIABLE = "variable"

	THIS = "this"
	SUPER = "super"
	FUN_ANON = "anon_function"
	INSTANCE = "instance"
	PARAMETER = "parameter"

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
		if left.type == Type.STRING and right.type == Type.STRING:
			return Type.STRING

		if left.type == Type.PARAMETER:
			return right.type
		if right.type == Type.PARAMETER:
			return left.type

		if left.type == Type.VARIABLE and right.type == Type.VARIABLE:
			return operationType(debug, Container(left.data.data, left.data.type), operator, Container(right.data.data, right.data.type))
		if left.type == Type.VARIABLE and right.type != Type.VARIABLE:
			return operationType(debug, Container(left.data.data, left.data.type), operator, right)
		if left.type != Type.VARIABLE and right.type == Type.VARIABLE:
			return operationType(debug, left, operator, Container(right.data.data, right.data.type))
	
		if left.type == Type.INSTANCE and right.type == Type.INSTANCE:
			return operationType(debug, Container(left.data.data, left.data.type), operator, Container(right.data.data, right.data.type))
		if left.type == Type.INSTANCE and right.type != Type.INSTANCE:
			return operationType(debug, Container(left.data.data, left.data.type), operator, right)
		if left.type != Type.INSTANCE and right.type == Type.INSTANCE:
			return operationType(debug, left, operator, Container(right.data.data, right.data.type))

		if isinstance(left, Container) and isinstance(right, Container):
			error(debug, f"Cannot operate different Types <{left.type}>({left.data}) {operator} <{right.type}>({right.data})")
		else:
			error(debug, f"Cannot operate Unkown Types {type(left)}({left}) {operator} {type(right)}({right})")
	error(debug, f"Cannot operate Unkown Types {type(left)}({left}) {operator} {type(right)}({right})")

def comparisonCheck(debug: Lace, left: 'Container', operator: str, right: 'Container'):
	if isinstance(left, Container) and isinstance(right, Container):
		if operator not in ['<=', '<', '>=', '>', '==', '!=']:
			error(debug, f"Invalid comparison operator: {operator}")
		if operator in ['<=', '<', '>=', '>']:
			if left.type == Type.INT and right.type == Type.INT:
				return True
			if left.type == Type.FLOAT and right.type == Type.INT:
				return True
			if left.type == Type.INT and right.type == Type.FLOAT:
				return True
			if left.type == Type.FLOAT and right.type == Type.FLOAT:
				return True
			
			if left.type == Type.VARIABLE and right.type == Type.VARIABLE:
				return comparisonCheck(debug, Container(left.data.data, left.data.type), operator, Container(right.data.data, right.data.type))
			if left.type == Type.VARIABLE and right.type != Type.VARIABLE:
				return comparisonCheck(debug, Container(left.data.data, left.data.type), operator, right)
			if left.type != Type.VARIABLE and right.type == Type.VARIABLE:
				return comparisonCheck(debug, left, operator, Container(right.data.data, right.data.type))
		
			if left.type == Type.INSTANCE and right.type == Type.INSTANCE:
				return comparisonCheck(debug, Container(left.data.data, left.data.type), operator, Container(right.data.data, right.data.type))
			if left.type == Type.INSTANCE and right.type != Type.INSTANCE:
				return comparisonCheck(debug, Container(left.data.data, left.data.type), operator, right)
			if left.type != Type.INSTANCE and right.type == Type.INSTANCE:
				return comparisonCheck(debug, left, operator, Container(right.data.data, right.data.type))
			error(debug, f"Cannot operate Types <{left.type}>({left.data}) {operator} <{right.type}>({right.data})")
		else:
			if left.type == Type.VARIABLE and right.type == Type.VARIABLE:
				return comparisonCheck(debug, Container(left.data.data, left.data.type), operator, Container(right.data.data, right.data.type))
			if left.type == Type.VARIABLE and right.type != Type.VARIABLE:
				return comparisonCheck(debug, Container(left.data.data, left.data.type), operator, right)
			if left.type != Type.VARIABLE and right.type == Type.VARIABLE:
				return comparisonCheck(debug, left, operator, Container(right.data.data, right.data.type))
		
			if left.type == Type.INSTANCE and right.type == Type.INSTANCE:
				return comparisonCheck(debug, Container(left.data.data, left.data.type), operator, Container(right.data.data, right.data.type))
			if left.type == Type.INSTANCE and right.type != Type.INSTANCE:
				return comparisonCheck(debug, Container(left.data.data, left.data.type), operator, right)
			if left.type != Type.INSTANCE and right.type == Type.INSTANCE:
				return comparisonCheck(debug, left, operator, Container(right.data.data, right.data.type))

			if left.type != right.type:
				error(debug, f"Cannot compare different Types <{left.type}>({left.data}) {operator} <{right.type}>({right.data})")
			return True
	error(debug, f"Cannot compare Unkown Types {type(left)}({left}) {operator} {type(right)}({right})")

T = TypeVar('T')
class Container(Generic[T]):
	def __init__(self, data: Union[str, int, float, bool, 'Class', 'Function', 'Variable', None] = None, type: Type = Type.NONE):
		self.data = data
		self.type = type
		self.tac_data = {}

	def innermostCode(self):
		if isinstance(self.data, Variable):
			return self.data.innermostCode()
		if isinstance(self.data, Container):
			return self.data.innermostCode()
		return self.data

	def __str__(self):
		return f"<{self.type}>({self.data})"

class Variable:
	def __init__(self):
		self.ctx         : CompiscriptParser.VariableContext = None
		self.tac_data    : 'Tac_Data' = None

		self.ID          : str  = None
		self.type        : Type = Type.UNKNOWN
		self.data        : str | Class  = None

		self.scope_depth       : int = 0
		self.scope_depth_count : int = 0

		self.member : Class = None
		self.origin : str   = "Declared"

	def innermostCode(self):
		if isinstance(self.data, Class):
			return self.data
		return self.data

	def __str__(self):
		return f"VARIABLE '{self.ID}'"

class Function_Parameter:
	def __init__(self):
		self.ID   : str  = None
		self.type : Type = Type.UNKNOWN

		self.function : Function = None

	def __str__(self):
		return f"FUNCTION PARAMETER '{self.ID}'"

class Function:
	def __init__(self):
		self.ctx         : CompiscriptParser.FunctionContext = None
		self.tac_data    : 'Tac_Data' = None

		self.ID          : str  = None
		self.data        : str  = None
		self.return_type : Type = Type.VOID

		self.scope_depth       : int = 0
		self.scope_depth_count : int = 0

		self.member : Class = None
		self.origin : str   = "Declared"

		self.recursive  : bool   = False
		self.parameters : List[Function_Parameter] = []

	def checkParameter(self, ID: str):
		for param in self.parameters:
			if param.ID == ID:
				return True
		return False

	def lookupParameter(self, ID: str):
		for param in self.parameters:
			if param.ID == ID:
				return param

	def __str__(self):
		return f"FUNCTION_OBJECT '{self.ID}'"

class Class:
	def __init__(self):
		self.ctx         : CompiscriptParser.ClassDeclContext = None
		self.tac_data    : 'Tac_Data' = None

		self.ID          : str   = None
		self.parent      : Class = None

		self.scope_depth       : int = 0
		self.scope_depth_count : int = 0

		self.initializer      : Function       = None
		self.member_functions : List[Function] = []
		self.member_variables : List[Variable] = []

	def checkFunction(self, ID: str):
		for member in self.member_functions:
			if member.ID == ID:
				return True
		if self.parent:
			return self.parent.checkFunction(ID)
		return False

	def checkVariable(self, ID: str):
		for member in self.member_variables:
			if member.ID == ID:
				return True
		if self.parent:
			return self.parent.checkVariable(ID)
		return False

	def lookupFunction(self, ID: str):
		for member in self.member_functions:
			if member.ID == ID:
				return member
		if self.parent:
			return self.parent.lookupFunction(ID)

	def lookupVariable(self, ID: str):
		for member in self.member_variables:
			if member.ID == ID:
				return member
		if self.parent:
			return self.parent.lookupVariable(ID)

	def __str__(self):
		return f"CLASS_OBJECT '{self.ID}'"