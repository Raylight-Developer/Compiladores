from Include import *
from Lace import *

class ANT_Program:
	def __init__(self):
		self.declarations : List[ANT_Declaration]  = []

class ANT_Declaration:
	def __init__(self):
		self.classDecl: ANT_ClassDecl = None
		self.funDecl: ANT_FunDecl = None
		self.varDecl: ANT_VarDecl = None
		self.statement: ANT_Statement = None
	def __str__(self) -> str:
		if self.classDecl:
			return "classDecl"
		if self.funDecl:
			return "funDecl"
		if self.varDecl:
			return "varDecl"
		if self.statement:
			return "statement"

class ANT_ClassDecl:
	def __init__(self):
		self.IDENTIFIER: str = None
		self.extends: str = None
		self.class_body: ANT_ClassBody = None

class ANT_ClassBody:
	def __init__(self):
		self.class_members: List[ANT_ClassMember] = []

class ANT_ClassMember:
	def __init__(self):
		self.function: ANT_Function = None

class ANT_FunDecl:
	def __init__(self):
		self.function: ANT_Function = None

class ANT_VarDecl:
	def __init__(self):
		self.variable: ANT_Variable = None

class ANT_Statement:
	def __init__(self):
		self.exprStmt: ANT_ExprStmt = None
		self.forStmt : ANT_ForStmt = None
		self.ifStmt: ANT_IfStmt = None
		self.printStmt: ANT_PrintStmt = None
		self.returnStmt: ANT_ReturnStmt = None
		self.whileStmt: ANT_WhileStmt = None
		self.block: ANT_Block = None

	def __str__(self) -> str:
		if self.exprStmt:
			return "exprStmt"
		if self.forStmt :
			return "forStmt"
		if self.ifStmt:
			return "ifStmt"
		if self.printStmt:
			return "printStmt"
		if self.returnStmt:
			return "erturnStmt"
		if self.whileStmt:
			return "whileStmt"
		if self.block:
			return "blockStmt"

class ANT_ExprStmt:
	def __init__(self):
		self.expression: ANT_Expression = None

class ANT_ForStmt:
	def __init__(self):
		self.varDecl: ANT_VarDecl = None
		self.exprStmt: ANT_ExprStmt = None
		self.compare_expression: ANT_Expression = None
		self.increment_expression: ANT_Expression = None
		self.statement: ANT_Statement = None

class ANT_IfStmt:
	def __init__(self):
		self.expression: ANT_Expression = None
		self.if_statement: ANT_Statement = None
		self.else_statement: ANT_Statement = None

class ANT_PrintStmt:
	def __init__(self):
		self.expression: ANT_Expression = None

class ANT_ReturnStmt:
	def __init__(self):
		self.expression: ANT_Expression = None

class ANT_WhileStmt:
	def __init__(self):
		self.expression: ANT_Expression = None
		self.statement: ANT_Statement = None

class ANT_Block:
	def __init__(self):
		self.declarations: List[ANT_Declaration] = []

class ANT_FunAnon:
	def __init__(self):
		self.parameters: ANT_Parameters = None
		self.block: ANT_Block = None

class ANT_Expression:
	def __init__(self):
		self.assignment: ANT_Assignment = None
		self.funAnon: ANT_FunAnon = None

class ANT_Assignment:
	def __init__(self):
		self.call: ANT_Call = None
		self.IDENTIFIER: str = None
		self.assignment: ANT_Assignment = None
	# OR
		self.logic_or: ANT_LogicOr = None

class ANT_LogicOr:
	def __init__(self):
		self.left:  ANT_LogicAnd = None
		self.array: List[Tuple[str, ANT_LogicAnd]] = []

class ANT_LogicAnd:
	def __init__(self):
		self.left:  ANT_Equality = None
		self.array: List[Tuple[str, ANT_Equality]] = []

class ANT_Equality:
	def __init__(self):
		self.left:  ANT_Comparison = None
		self.array: List[Tuple[str, ANT_Comparison]] = []

class ANT_Comparison:
	def __init__(self):
		self.left:  ANT_Term = None
		self.array: List[Tuple[str, ANT_Term]] = []

class ANT_Term:
	def __init__(self):
		self.left:  ANT_Factor = None
		self.array: List[Tuple[str, ANT_Factor]] = []

class ANT_Factor:
	def __init__(self):
		self.left:  ANT_Unary = None
		self.array: List[Tuple[str, ANT_Unary]] = []

class ANT_Array:
	def __init__(self):
		self.expressions: List[ANT_Expression] = []

class ANT_Instantiation:
	def __init__(self):
		self.IDENTIFIER: str = None
		self.arguments: ANT_Arguments = None

class ANT_Unary:
	def __init__(self):
		self.operator: str = None
		self.unary: ANT_Unary = None
	# OR
		self.call: ANT_Call = None

class ANT_Call:
	def __init__(self):
		self.primary: ANT_Primary = None
		self.calls: List[ANT_CallSuffix] = []
	# OR
		self.funAnon: ANT_FunAnon = None

class ANT_CallSuffix:
	def __init__(self):
		self.IDENTIFIER: str = None
		self.expression: ANT_Expression = None
		self.arguments: ANT_Arguments = None
		self.empty: bool = False

class ANT_SuperCall:
	def __init__(self):
		self.IDENTIFIER: str = None

class ANT_Primary:
	def __init__(self):
		self.operator: str = None
	# OR
		self.NUMBER: Union[int, float] = None
		self.STRING: str = None
		self.IDENTIFIER: str = None
		self.expression: ANT_Expression = None
	# OR
		self.superCall: ANT_SuperCall = None
	# OR
		self.array: ANT_Array = None
		self.instantiation: ANT_Instantiation = None

class ANT_Function:
	def __init__(self):
		self.IDENTIFIER: str = None
		self.parameters: ANT_Parameters = None
		self.block: ANT_Block = None

class ANT_Variable:
	def __init__(self):
		self.IDENTIFIER: str = None
		self.expression: ANT_Expression = None

class ANT_Parameters:
	def __init__(self):
		self.identifiers: List[str] = []

class ANT_Arguments:
	def __init__(self):
		self.expressions: List[ANT_Expression] = []