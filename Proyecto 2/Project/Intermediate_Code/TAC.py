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

		self.flags = {
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

		self.tac_map: Dict[str,str] = {}
		self.tac_code = Lace()
		self.visit(self.program)

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

	def visit(self, node):
		if isinstance(node, ANT_Program):
			for declaration in node.declarations:
				self.visit(declaration)
		
		elif isinstance(node, ANT_Declaration):
			self.flags["Declaration"] += 1
			if node.classDecl:
				self.visit(node.classDecl.class_body)
			elif node.funDecl:
				self.visit(node.funDecl.function)
			elif node.varDecl:
				self.visit(node.varDecl)
			elif node.statement:
				self.visit(node.statement)
			self.flags["Declaration"] -= 1

		elif isinstance(node, ANT_ClassDecl):
			self.flags["ClassDecl"] += 1
			self.visit(node.class_body)
			self.flags["ClassDecl"] -= 1

		elif isinstance(node, ANT_ClassBody):
			self.flags["ClassBody"] += 1
			for member in node.class_members:
				self.visit(member)
			self.flags["ClassBody"] -= 1

		elif isinstance(node, ANT_ClassMember):
			self.flags["ClassMember"] += 1
			self.visit(node.function)
			self.flags["ClassMember"] -= 1

		elif isinstance(node, ANT_FunDecl):
			self.flags["FunDecl"] += 1
			self.visit(node.function)
			self.flags["FunDecl"] -= 1

		elif isinstance(node, ANT_VarDecl):
			self.flags["VarDecl"] += 1
			return self.visit(node.variable)
			self.flags["VarDecl"] -= 1

		elif isinstance(node, ANT_Statement):
			self.flags["Statement"] += 1
			if node.forStmt:
				self.visit(node.forStmt)
			elif node.ifStmt:
				self.visit(node.ifStmt)
			self.flags["Statement"] -= 1

		elif isinstance(node, ANT_ExprStmt):
			self.flags["ExprStmt"] += 1
			self.visit(node.expression)
			self.flags["ExprStmt"] -= 1

		elif isinstance(node, ANT_ForStmt):
			self.flags["ForStmt"] += 1

			if node.varDecl:
				var = self.visit(node.varDecl)

				start = self.new_label()
				self.tac_code << NL() << start << ":"
				end = self.new_label()

				if node.compare_expression:
					compare = self.visit(node.compare_expression)
					self.tac_code << NL() << "IF " << compare << " GO_TO " << end
					if node.increment_expression:
						increment = self.visit(node.increment_expression)
						self.tac_code << NL() << var << " = " << increment

				self.visit(node.statement)
				self.tac_code << NL() << "GO_TO " << start

				self.tac_code << NL() << end << ":"
			elif node.exprStmt:
				self.visit(node.exprStmt)

			self.flags["ForStmt"] -= 1

		elif isinstance(node, ANT_IfStmt):
			self.flags["IfStmt"] += 1
			self.flags["IfStmt"] -= 1

		elif isinstance(node, ANT_PrintStmt):
			self.flags["PrintStmt"] += 1
			self.flags["PrintStmt"] -= 1

		elif isinstance(node, ANT_ReturnStmt):
			self.flags["ReturnStmt"] += 1
			self.flags["ReturnStmt"] -= 1

		elif isinstance(node, ANT_WhileStmt):
			self.flags["WhileStmt"] += 1
			self.flags["WhileStmt"] -= 1

		elif isinstance(node, ANT_Block):
			self.flags["Block"] += 1
			self.flags["Block"] -= 1

		elif isinstance(node, ANT_FunAnon):
			self.flags["FunAnon"] += 1
			self.flags["FunAnon"] -= 1

		elif isinstance(node, ANT_Expression):
			self.flags["Expression"] += 1
			if node.assignment:
				res = self.visit(node.assignment)
			elif node.funAnon:
				res = self.visit(node.funAnon)
			self.flags["Expression"] -= 1
			return res

		elif isinstance(node, ANT_Assignment):
			self.flags["Assignment"] += 1
			if node.IDENTIFIER:
				if not node.assignment:
					self.tac_code << NL() << self.tac_map["var;"+node.IDENTIFIER] << " = "
				if node.assignment:
					res = self.visit(node.assignment)
			elif node.logic_or:
				res = self.visit(node.logic_or)
			self.flags["Assignment"] -= 1
			return res

		elif isinstance(node, ANT_LogicOr):
			self.flags["LogicOr"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right in node.array:
					right_result = self.visit(right)
					res = self.new_temp()
					self.tac_code << NL() << f"{res} = {left} || {right_result}"
					left = res
			self.flags["LogicOr"] -= 1
			return res

		elif isinstance(node, ANT_LogicAnd):
			self.flags["LogicAnd"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right in node.array:
					right_result = self.visit(right)
					res = self.new_temp()
					self.tac_code << NL() << f"{res} = {left} && {right_result}"
					left = res
			self.flags["LogicAnd"] -= 1
			return res

		elif isinstance(node, ANT_Equality):
			self.flags["Equality"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right in node.array:
					right_result = self.visit(right)
					res = self.new_temp()
					self.tac_code << NL() << f"{res} = {left} {op} {right_result}"
					left = res
			self.flags["Equality"] -= 1
			return res

		elif isinstance(node, ANT_Comparison):
			self.flags["Comparison"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right in node.array:
					right_result = self.visit(right)
					res = self.new_temp()
					self.tac_code << NL() << f"{res} = {left} {op} {right_result}"
					left = res
			self.flags["Comparison"] -= 1
			return res

		elif isinstance(node, ANT_Term):
			self.flags["Term"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right in node.array:
					right_result = self.visit(right)
					res = self.new_temp()
					self.tac_code << NL() << f"{res} = {left} {op} {right_result}"
					left = res
			self.flags["Term"] -= 1
			return res

		elif isinstance(node, ANT_Factor):
			self.flags["Factor"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right in node.array:
					right_result = self.visit(right)
					res = self.new_temp()
					self.tac_code << NL() << f"{res} = {left} {op} {right_result}"
					left = res
				self.flags["Factor"] -= 1
			return res

		elif isinstance(node, ANT_Array):
			self.flags["Array"] += 1
			for expression in node.expressions:
				self.visit(expression)
			self.flags["Array"] -= 1

		elif isinstance(node, ANT_Instantiation):
			self.flags["Instantiation"] += 1
			self.visit(node.arguments)
			self.flags["Instantiation"] -= 1

		elif isinstance(node, ANT_Unary):
			self.flags["Unary"] += 1
			if node.call:
				res = self.visit(node.call)
			elif node.unary:
				right_result = self.visit(node.unary)
				res = self.new_temp()
				self.tac_code << NL() << f"{res} = {node.operator}{right_result}"
			self.flags["Unary"] -= 1
			return res

		elif isinstance(node, ANT_Call):
			self.flags["Call"] += 1
			if node.funAnon:
				res = self.visit(node.funAnon)
			elif node.primary:
				if len(node.calls) == 0:
					res = self.visit(node.primary)
				else:
					pass

			self.flags["Call"] -= 1
			return res

		elif isinstance(node, ANT_SuperCall):
			self.flags["SuperCall"] += 1
			self.flags["SuperCall"] -= 1

		elif isinstance(node, ANT_Primary): # Can only be called from within a call
			self.flags["Primary"] += 1
			if node.NUMBER:
				res = node.NUMBER
			elif node.STRING :
				res =  node.STRING
			elif node.IDENTIFIER:
				res =  self.tac_map["var;"+node.IDENTIFIER]
			elif node.operator:
				res =  node.operator
			elif node.expression:
				res =  self.visit(node.expression)
			elif node.superCall:
				res =  self.visit(node.superCall)
			elif node.array:
				res =  self.visit(node.array)
			elif node.instantiation:
				res =  self.visit(node.instantiation)
			self.flags["Primary"] -= 1
			return res

		elif isinstance(node, ANT_Function):
			self.flags["Function"] += 1
			self.flags["Function"] -= 1

		elif isinstance(node, ANT_Variable):
			self.flags["Variable"] += 1
			if node.expression:
				ID = self.new_temp()
				self.tac_map["var;"+node.IDENTIFIER] = ID
				expression = self.visit(node.expression)
				self.tac_code << NL() << ID << ": " << expression
			self.flags["Variable"] -= 1
			return ID

		elif isinstance(node, ANT_Parameters):
			self.flags["Parameters"] += 1
			self.flags["Parameters"] -= 1

		elif isinstance(node, ANT_Arguments):
			self.flags["Arguments)"] += 1
			self.flags["Arguments)"] -= 1