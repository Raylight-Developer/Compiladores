from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *

from Analyzer.Symbols import *
from Analyzer.Scope import *

from .Classes import *
from .Tree import *

class Tac_Info:
	def __init__(self, ID: str = "", data: Dict[str, Any] = {}):
		self.ID = ID
		self.data = data

class TAC_Generator():
	def __init__(self, scope_tracker: Scope_Tracker, program: CompiscriptParser.ProgramContext):
		super().__init__()
		self.scope_tracker = scope_tracker
		self.label_count = -1
		self.temp_count = -1
		self.code = Lace()
		self.tac_info: Dict[Union[Function, Variable, Class, Function_Parameter], Tac_Info] = {}
		self.tree = Tree_Generator()
		self.program: ANT_Program = self.tree.visitProgram(program)

		self.depth = {
			"Declaration": 0,
			"ClassDecl": 0,
			"ClassBody": 0,
			"ClassMember": 0,
			"FunDecl": 0,
			"VarDecl": 0,
			"Statement": 0,
			"ExprStmt": 0,
			"ForStmt": 0,
			"IfStmt": 0,
			"PrintStmt": 0,
			"ReturnStmt": 0,
			"WhileStmt": 0,
			"Block": 0,
			"FunAnon": 0,
			"Expression": 0,
			"Assignment": 0,
			"LogicOr": 0,
			"LogicAnd": 0,
			"Equality": 0,
			"Comparison": 0,
			"Term": 0,
			"Factor": 0,
			"Array": 0,
			"Instantiation": 0,
			"Unary": 0,
			"Call": 0,
			"SuperCall": 0,
			"Primary": 0,
			"Function": 0,
			"Variable": 0,
			"Parameters": 0,
			"Arguments": 0,
		}

		self.tac_code = Lace()
		self.traverseProgram(self.program)

		print(self.tac_code)

	def new_temp(self):
		self.temp_count += 1
		return f"T_{self.temp_count}"
	
	def new_label(self):
		self.label_count += 1
		return f"L_{self.label_count}"

	def declareClass(self, struct: Class):
		temp_id = self.new_temp()
		self.code << NL() << f"// Class:     [{temp_id}] {struct.ID}"
		self.tac_info[struct] = Tac_Info(temp_id, {})

	def declareFunction(self, function: Function):
		#temp_id = self.new_temp()
		block_id = self.new_label()
		self.code << NL() << "// Declare Function ["
		if function.member:
			self.code << function.member.ID << "."
		self.code << function.ID << "] {"
		self.code += 1
		self.code << NL() << block_id << ":"
		self.code -= 1
		self.code << NL() << "// }" << NL()
		self.tac_info[function] =  Tac_Info(block_id, { "Block ID" : block_id, "Block" : f"{function.data} // FUNCTION CODE" })

	def declareVariable(self, variable: Variable):
		temp_id = self.new_temp()
		#self.code << NL()
		#self.code << f"// Variable:  [{temp_id}] "
		#if variable.member:
		#	self.code << variable.member.ID << "."
		#self.code << variable.ID
		self.tac_info[variable] =  Tac_Info(temp_id)

	def declareParameter(self, parameter: Function_Parameter):
		temp_id = self.new_temp()
		#self.code << NL()
		#self.code << f"// Parameter:  [{temp_id}] "
		#self.code << parameter.function.ID << "." << parameter.ID
		self.tac_info[parameter] = Tac_Info(temp_id)

	def declareAnonFunction(self, function: Function):
		#temp_id = self.new_temp()
		block_id = self.new_label()
		#self.code << NL()
		#self.code << f"// Anon Function:  [{block_id}] [{block_id}] {function.ID}"
		self.tac_info[function] = Tac_Info(block_id, { "Block" : block_id })

	def assignVariable(self, variable: Variable):
		self.code << NL() << "// Assign Variable [" << variable.ID << "] {"
		self.code += 1
		self.code << NL()
		#expression = self.visit(variable.ctx.expression())
		expression = variable.ctx.expression().getText()
		self.code << self.tac_info[variable].ID << ": " << expression
		self.code -= 1
		self.code << NL() << "// }" << NL()

	def callFunction(self, function: Function, call_params: List[Container]):
		self.code << NL() << "// Call Function ["
		if function.member:
			if function.member.parent:
				self.code << "Super<" << function.member.parent.ID << ">."
			else:
				self.code << function.member.ID << "."
		self.code << function.ID << "] {"
		self.code += 1
		self.code << NL()
		for i, param in enumerate(call_params):
			self.code << self.tac_info[function.parameters[i]].ID << ": "
			if param.type == Type.STRING:
				self.code << '"' << param.data << '"' << NL()
			elif param.type in [Type.FLOAT, Type.INT]:
				self.code << param.data << NL()
			else:
				self.code << param.data << NL()
		self.code << self.tac_info[self.scope_tracker.lookupFunction(function.ID, function.member)].data["Block"]
		self.code -= 1
		self.code << NL() << "// }" << NL()

	def generate_if(self, if_expr: List[str] = [], if_condition: str = "", if_body: List[str] = [], else_body: List[str] = []):
		if_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(if_expr)
		self.code << NL()
		self.code << NL() << f"IF ({if_condition}) GO_TO {if_label}"
		self.code += 1
		self.code << NL() << "\n".join(else_body)
		self.code -= 1
		self.code << NL() << f"GO_TO {end_label}"
		self.code << NL()
		self.code << NL() << f"{if_label}:"
		self.code += 1
		self.code << NL() << "\n".join(if_body)
		self.code -= 1
		self.code << NL()
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"

	def generate_while(self, while_expr: List[str] = [], while_condition: str = "", while_update: str = "", while_body: List[str] = []):
		loop_start_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(while_expr)
		self.code << NL()
		self.code << NL() << f"{loop_start_label}:"
		self.code += 1
		self.code << NL() << f"IF ({while_condition}) GO_TO {end_label}"
		self.code += 1
		self.code << NL() << "\n".join(while_body)
		self.code << NL() << while_update << " // Update While Condition"
		self.code -= 1
		self.code << NL() << f"GO_TO {loop_start_label}"
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"

	def generate_for(self, for_expr: List[str] = [], for_condition: str = "", for_update: str = "", for_body: List[str] = []):
		loop_start_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(for_expr)
		self.code << NL()
		self.code << NL() << f"{loop_start_label}:"
		self.code += 1
		self.code << NL() << f"IF ({for_condition}) GO_TO {end_label}"
		self.code << NL()
		self.code << NL() << "\n".join(for_body)
		self.code << NL() << for_update << " // Update For Condition"
		self.code << NL()
		self.code << NL() << f"GO_TO {loop_start_label}"
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"

	def traverseProgram(self, node):
		if isinstance(node, ANT_Program):
			for declaration in node.declarations:
				self.traverseProgram(declaration)
		
		elif isinstance(node, ANT_Declaration):
			self.depth["Declaration"] += 1
			if node.classDecl:
				self.traverseProgram(node.classDecl.class_body)
			elif node.funDecl:
				self.traverseProgram(node.funDecl.function)
			elif node.varDecl:
				self.traverseProgram(node.varDecl)
			elif node.statement:
				self.traverseProgram(node.statement)
			self.depth["Declaration"] -= 1

		elif isinstance(node, ANT_ClassDecl):
			self.depth["ClassDecl"] += 1
			self.traverseProgram(node.class_body)
			self.depth["ClassDecl"] -= 1

		elif isinstance(node, ANT_ClassBody):
			self.depth["ClassBody"] += 1
			for member in node.class_members:
				self.traverseProgram(member)
			self.depth["ClassBody"] -= 1

		elif isinstance(node, ANT_ClassMember):
			self.depth["ClassMember"] += 1
			self.traverseProgram(node.function)
			self.depth["ClassMember"] -= 1

		elif isinstance(node, ANT_FunDecl):
			self.depth["FunDecl"] += 1
			self.traverseProgram(node.function)
			self.depth["FunDecl"] -= 1

		elif isinstance(node, ANT_VarDecl):
			self.depth["VarDecl"] += 1
			self.traverseProgram(node.variable)
			self.depth["VarDecl"] -= 1

		elif isinstance(node, ANT_Statement):
			self.depth["Statement"] += 1
			self.depth["Statement"] -= 1

		elif isinstance(node, ANT_ExprStmt):
			self.depth["ExprStmt"] += 1
			self.depth["ExprStmt"] -= 1

		elif isinstance(node, ANT_ForStmt):
			self.depth["ForStmt"] += 1
			self.depth["ForStmt"] -= 1

		elif isinstance(node, ANT_IfStmt):
			self.depth["IfStmt"] += 1
			self.depth["IfStmt"] -= 1

		elif isinstance(node, ANT_PrintStmt):
			self.depth["PrintStmt"] += 1
			self.depth["PrintStmt"] -= 1

		elif isinstance(node, ANT_ReturnStmt):
			self.depth["ReturnStmt"] += 1
			self.depth["ReturnStmt"] -= 1

		elif isinstance(node, ANT_WhileStmt):
			self.depth["WhileStmt"] += 1
			self.depth["WhileStmt"] -= 1

		elif isinstance(node, ANT_Block):
			self.depth["Block"] += 1
			self.depth["Block"] -= 1

		elif isinstance(node, ANT_FunAnon):
			self.depth["FunAnon"] += 1
			self.depth["FunAnon"] -= 1

		elif isinstance(node, ANT_Expression):
			self.depth["Expression"] += 1
			if node.assignment:
				return self.traverseProgram(node.assignment)
			elif node.funAnon:
				self.traverseProgram(node.funAnon)
			self.depth["Expression"] -= 1

		elif isinstance(node, ANT_Assignment):
			self.depth["Assignment"] += 1
			if node.logic_or:
				result = self.traverseProgram(node.logic_or)
				if node.IDENTIFIER:
					self.tac_code << f"{node.IDENTIFIER} = {result}"
				return result
			self.depth["Assignment"] -= 1

		elif isinstance(node, ANT_LogicOr):
			self.depth["LogicOr"] += 1
			left = self.traverseProgram(node.left)
			for op, right in node.array:
				right_result = self.traverseProgram(right)
				temp = self.new_temp()
				self.tac_code << NL()  << f"{temp} = {left} || {right_result}"
				left = temp
			self.depth["LogicOr"] -= 1

		elif  isinstance(node, ANT_LogicAnd):
			self.depth["LogicAnd"] += 1
			left = self.traverseProgram(node.left)
			for op, right in node.array:
				right_result = self.traverseProgram(right)
				temp = self.new_temp()
				self.tac_code << NL() << f"{temp} = {left} && {right_result}"
				left = temp
			self.depth["LogicAnd"] -= 1

		elif isinstance(node, ANT_Equality):
			self.depth["Equality"] += 1
			left = self.traverseProgram(node.left)
			for op, right in node.array:
				right_result = self.traverseProgram(right)
				temp = self.new_temp()
				self.tac_code << f"{temp} = {left} {op} {right_result}"
				left = temp
			self.depth["Equality"] -= 1

		elif isinstance(node, ANT_Comparison):
			self.depth["Comparison"] += 1
			left = self.traverseProgram(node.left)
			for op, right in node.array:
				right_result = self.traverseProgram(right)
				temp = self.new_temp()
				self.tac_code << f"{temp} = {left} {op} {right_result}"
				left = temp
			self.depth["Comparison"] -= 1

		elif isinstance(node, ANT_Term):
			self.depth["Term"] += 1
			left = self.traverseProgram(node.left)
			for op, right in node.array:
				right_result = self.traverseProgram(right)
				temp = self.new_temp()
				self.tac_code <<f"{temp} = {left} {op} {right_result}"
				left = temp
			self.depth["Term"] -= 1

		elif isinstance(node, ANT_Factor):
			self.depth["Factor"] += 1
			left = self.traverseProgram(node.left)
			for op, right in node.array:
				right_result = self.traverseProgram(right)
				temp = self.new_temp()
				self.tac_code <<f"{temp} = {left} {op} {right_result}"
				left = temp
			self.depth["Factor"] -= 1

		elif isinstance(node, ANT_Array):
			self.depth["Array"] += 1
			for expression in node.expressions:
				self.traverseProgram(expression)
			self.depth["Array"] -= 1

		elif isinstance(node, ANT_Instantiation):
			self.depth["Instantiation"] += 1
			self.traverseProgram(node.arguments)
			self.depth["Instantiation"] -= 1

		elif isinstance(node, ANT_Unary):
			self.depth["Unary"] += 1
			if node.call:
				self.traverseProgram(node.call)
			elif node.unary:
				right_result = self.traverseProgram(node.unary)
				temp = self.new_temp()
				self.tac_code <<f"{temp} = {node.operator}{right_result}"
			self.depth["Unary"] -= 1

		elif isinstance(node, ANT_Call):
			self.depth["Call"] += 1
			self.depth["Call"] -= 1

		elif isinstance(node, ANT_SuperCall):
			self.depth["SuperCall"] += 1
			self.depth["SuperCall"] -= 1

		elif isinstance(node, ANT_Primary):
			self.depth["Primary"] += 1
			if node.NUMBER:
				return str(node.NUMBER)
			elif node.STRING :
				return f'"{node.STRING}"'
			elif node.IDENTIFIER:
				return node.IDENTIFIER
			elif node.expression:
				return self.traverseProgram(node.expression)
			elif node.superCall:
				return self.traverseProgram(node.superCall)
			elif node.array:
				return self.traverseProgram(node.array)
			elif node.instantiation:
				return self.traverseProgram(node.instantiation)
			elif node.operator:
				return node.operator
			self.depth["Primary"] -= 1

		elif isinstance(node, ANT_Function):
			self.depth["Function"] += 1
			self.depth["Function"] -= 1

		elif isinstance(node, ANT_Variable):
			self.depth["Variable"] += 1
			if node.expression:
				self.tac_code << f"{node.IDENTIFIER} = "
				self.traverseProgram(node.expression)
			self.depth["Variable"] -= 1
			
		elif isinstance(node, ANT_Parameters):
			self.depth["Parameters"] += 1
			self.depth["Parameters"] -= 1

		elif isinstance(node, ANT_Arguments):
			self.depth["Arguments)"] += 1
			self.depth["Arguments)"] -= 1