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

class TAC_Generator():
	def __init__(self, scope_tracker: Scope_Tracker, program: CompiscriptParser.ProgramContext):
		super().__init__()
		self.label_count = -1
		self.temp_count = -1

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
		self.code = Lace()
		self.visit(self.program)

	def new_temp(self):
		self.temp_count += 1
		return f"T_{self.temp_count}"
	
	def new_label(self):
		self.label_count += 1
		return f"L_{self.label_count}"

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
			res = self.visit(node.variable)
			self.flags["VarDecl"] -= 1
			return res

		elif isinstance(node, ANT_Statement):
			self.flags["Statement"] += 1
			if node.exprStmt:
				self.visit(node.exprStmt)
			if node.forStmt:
				self.visit(node.forStmt)
			elif node.ifStmt:
				self.visit(node.ifStmt)
			if node.printStmt:
				self.visit(node.printStmt)
			if node.returnStmt:
				self.visit(node.returnStmt)
			if node.whileStmt:
				self.visit(node.whileStmt)
			elif node.block:
				self.visit(node.block)
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
				self.code << NL() << "// FOR LOOP START {"
				self.code << NL() << start << ":"
				self.code +=1
				end = self.new_label()

				if node.compare_expression:
					self.code << NL() << "// COMPARE"
					compare = self.visit(node.compare_expression)
					self.code << NL() << "IF " << compare << " GO_TO " << end
					if node.increment_expression:
						self.code << NL() << "// INCREMENT"
						increment = self.visit(node.increment_expression)
						self.code << NL() << var << " = " << increment
				self.code << NL() << "// LOOP BODY START{"
				self.code += 1
				self.visit(node.statement)
				self.code -= 1
				self.code << NL() << "//} LOOP BODY END"
				self.code << NL() << "GO_TO " << start

				self.code -=1
				self.code << NL() << end << ":"
				self.code << NL() << "//} FOR LOOP END"
			elif node.exprStmt:
				self.visit(node.exprStmt)

			self.flags["ForStmt"] -= 1

		elif isinstance(node, ANT_IfStmt):
			self.flags["IfStmt"] += 1
			true = self.new_label()

			self.code << NL() << "// IF START {"
			end = self.new_label()

			if node.expression:
				self.code << NL() << "// COMPARE"
				compare = self.visit(node.expression)
				self.code << NL() << "IF " << compare << " GO_TO " << true

			if node.else_statement:
				self.code << NL() << "// FALSE"
				self.code += 1
				self.visit(node.else_statement)
				self.code << NL() << "GO_TO " << end
				self.code -= 1
	
			self.code << NL() << "// TRUE"
			self.code << NL() << true << ":"
			self.code += 1
			self.visit(node.if_statement)
			self.code << NL() << "GO_TO " << end
			self.code -= 1

			self.code << NL() << end << ":"
			self.code << NL() << "//} IF END"
			self.flags["IfStmt"] -= 1

		elif isinstance(node, ANT_PrintStmt):
			self.flags["PrintStmt"] += 1
			self.code << NL() << "// PRINT START {"
			self.code << NL() << "SYSCALL"
			self.code += 1
			expr = self.visit(node.expression)
			self.code -= 1
			self.code << NL() << "PRINT " << expr
			self.code << NL() << "SYSCALL"
			self.code << NL() << "//} PRINT END"
			self.flags["PrintStmt"] -= 1

		elif isinstance(node, ANT_ReturnStmt):
			self.flags["ReturnStmt"] += 1
			self.flags["ReturnStmt"] -= 1

		elif isinstance(node, ANT_WhileStmt):
			self.flags["WhileStmt"] += 1
			self.flags["WhileStmt"] -= 1

		elif isinstance(node, ANT_Block):
			self.flags["Block"] += 1
			for declaration in node.declarations:
				self.visit(declaration)
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
					self.code << NL() << self.tac_map["var;"+node.IDENTIFIER] << " = "
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
					self.code << NL() << f"{res} = {left} || {right_result}"
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
					self.code << NL() << f"{res} = {left} && {right_result}"
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
					self.code << NL() << f"{res} = {left} {op} {right_result}"
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
					self.code << NL() << f"{res} = {left} {op} {right_result}"
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
					self.code << NL() << f"{res} = {left} {op} {right_result}"
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
					self.code << NL() << f"{res} = {left} {op} {right_result}"
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
				self.code << NL() << f"{res} = {node.operator}{right_result}"
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
				self.code << NL() << ID << ": " << expression << " // " << node.IDENTIFIER
			self.flags["Variable"] -= 1
			return ID

		elif isinstance(node, ANT_Parameters):
			self.flags["Parameters"] += 1
			self.flags["Parameters"] -= 1

		elif isinstance(node, ANT_Arguments):
			self.flags["Arguments)"] += 1
			self.flags["Arguments)"] -= 1