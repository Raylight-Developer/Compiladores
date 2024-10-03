from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *

from Analyzer.Symbols import *
from Analyzer.Scope import *

from .TAC_Data import *
from .Classes import *
from .Tree import *

class TAC_Generator():
	def __init__(self, program: CompiscriptParser.ProgramContext):
		super().__init__()
		self.label_count = -1
		self.temp_count = -1

		self.tree = Tree_Generator()
		self.scope = Tac_Scope_Tracker()
		self.program: ANT_Program = self.tree.visitProgram(program)

		self.cls: Tac_Class = None
		self.fun: Tac_Function = None
		self.var: Tac_Variable = None

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
			"CallSuffix": 0,
			"SuperCall": 0,
			"Primary": 0,
			"Function": 0,
			"Variable": 0,
			"Parameters": 0,
			"Arguments": 0,
		}

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
				self.visit(node.classDecl)
			elif node.funDecl:
				self.visit(node.funDecl)
			elif node.varDecl:
				self.visit(node.varDecl)
			elif node.statement:
				self.visit(node.statement)
			self.flags["Declaration"] -= 1

		elif isinstance(node, ANT_ClassDecl):
			self.flags["ClassDecl"] += 1

			cls = Tac_Class()
			cls.name = node.IDENTIFIER
			self.scope.declareClass(cls)
			self.cls = cls

			self.scope.enter()
			self.visit(node.class_body)
			self.scope.exit()

			self.cls = None

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
			res = self.visit(node.function)
			self.flags["FunDecl"] -= 1
			return res

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
				fun = self.visit(node.varDecl)

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
						self.code << NL() << fun << " = " << increment
				self.code << NL() << "// FOR LOOP BODY START {"
				self.code += 1
				self.visit(node.statement)
				self.code -= 1
				self.code << NL() << "//} FOR LOOP BODY END"
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

			start = self.new_label()
			self.code << NL() << "// WHILE LOOP START {"
			self.code << NL() << start << ":"
			self.code +=1
			end = self.new_label()

			if node.expression:
				self.code << NL() << "// COMPARE"
				compare = self.visit(node.expression)
				self.code << NL() << "IF " << compare << " GO_TO " << end
			
			self.code << NL() << "// WHILE LOOP BODY START {"
			self.code += 1
			self.visit(node.statement)
			self.code -= 1
			self.code << NL() << "//} WHILE LOOP BODY END"
			self.code << NL() << "GO_TO " << start

			self.code -=1
			self.code << NL() << end << ":"
			self.code << NL() << "//} WHILE LOOP END"

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
				if node.call:
					if node.call == "this":
						var = Tac_Variable()
						var.ID = self.new_temp()
						var.name = node.IDENTIFIER
						var.member = self.cls
						self.cls.member_variables.append(var)
						self.scope.declareVariable(var)
						self.var = var
						res = self.visit(node.assignment)
						self.code << NL() << var.ID << ": " << res << " // " << node.IDENTIFIER << " = " << res
					else:
						self.visit(node.call)
				elif node.assignment:
					res = self.visit(node.assignment)
				self.code << NL() << self.scope.lookupVariable(node.IDENTIFIER, self.cls).ID << ": " << res << " // " << node.IDENTIFIER << " = " << res
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
				for op, right_node in node.array:
					right = self.visit(right_node)
					res = self.new_temp()
					self.code << NL() << f"OR {res}: {left}, {right} // {left} || {right}"
					left = res
			self.flags["LogicOr"] -= 1
			return res

		elif isinstance(node, ANT_LogicAnd):
			self.flags["LogicAnd"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right_node in node.array:
					right = self.visit(right_node)
					res = self.new_temp()
					self.code << NL() << f"AND {res}: {left}, {right} // {left} && {right}"
					left = res
			self.flags["LogicAnd"] -= 1
			return res

		elif isinstance(node, ANT_Equality):
			self.flags["Equality"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right_node in node.array:
					right = self.visit(right_node)
					res = self.new_temp()
					if op == "==":
						self.code << NL() << f"EQ {res}: {left}, {right} // {left} == {right}"
					elif op == "!=":
						self.code << NL() << f"NEQ {res}: {left}, {right} // {left} != {right}"
					left = res
			self.flags["Equality"] -= 1
			return res

		elif isinstance(node, ANT_Comparison):
			self.flags["Comparison"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right_node in node.array:
					right = self.visit(right_node)
					res = self.new_temp()
					res = self.new_temp()
					if op == "<":
						self.code << NL() << f"LT {res}: {left}, {right} // {left} < {right}"
					elif op == "<=":
						self.code << NL() << f"LEQ {res}: {left}, {right} // {left} <= {right}"
					elif op == ">":
						self.code << NL() << f"GT {res}: {left}, {right} // {left} > {right}"
					elif op == ">=":
						self.code << NL() << f"GEQ {res}: {left}, {right} // {left} >= {right}"
					left = res
			self.flags["Comparison"] -= 1
			return res

		elif isinstance(node, ANT_Term):
			self.flags["Term"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right_node in node.array:
					right = self.visit(right_node)
					res = self.new_temp()
					if op == "+":
						self.code << NL() << f"ADD {res}: {left}, {right} // {left} + {right}"
					elif op == "-":
						self.code << NL() << f"SUB {res}: {left}, {right} // {left} - {right}"
					left = res
			self.flags["Term"] -= 1
			return res

		elif isinstance(node, ANT_Factor):
			self.flags["Factor"] += 1
			if len(node.array) == 0:
				res = self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right_node in node.array:
					right = self.visit(right_node)
					res = self.new_temp()
					if op == "*":
						self.code << NL() << f"MUL {res}: {left}, {right} // {left} * {right}"
					elif op == "/":
						self.code << NL() << f"DIV {res}: {left}, {right} // {left} / {right}"
					elif op == "%":
						self.code << NL() << f"MOD {res}: {left}, {right} // {left} % {right}"
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

			res = self.new_temp()
			cls = self.scope.lookupClass(node.IDENTIFIER)
			arguments: List[str] = self.visit(node.arguments)
			#for argument in arguments:

			self.flags["Instantiation"] -= 1
			return res

		elif isinstance(node, ANT_Unary):
			self.flags["Unary"] += 1
			if node.call:
				res = self.visit(node.call)
			elif node.unary:
				right = self.visit(node.unary)
				res = self.new_temp()
				if node.operator == "-":
					self.code << NL() << f"SUB {res}: 0, {right} // - {right}"
				elif node.operator == "!":
					self.code << NL() << f"NOT {res}: {right} // ! {right}"
			self.flags["Unary"] -= 1
			return res

		elif isinstance(node, ANT_Call):
			self.flags["Call"] += 1
			if node.funAnon:
				res = self.visit(node.funAnon)
			elif node.primary:
				if len(node.calls) == 0 :
					res = self.visit(node.primary) # Calling Variable
					pass
				elif len(node.calls) == 1 :
					call = node.calls[0]
					if call.IDENTIFIER: # Calling Member Variable
						res = call.IDENTIFIER
					elif call.expression: # Calling the index of an array [expression]
						pass
					elif call.arguments: # Calling Function with params
						function: Tac_Function = self.scope.lookupFunction(node.primary.IDENTIFIER, self.cls)
						res = function.ID
						arguments = self.visit(call.arguments)
						for i, param in enumerate(function.parameters):
							self.code << NL() << param.ID << ": " << arguments[i]
						self.code << NL() << "CALL " << res << " // Calling function with params"
					elif call.empty: # Calling Function with no params
						function: Tac_Function = self.scope.lookupFunction(node.primary.IDENTIFIER, self.cls)
						res = function.ID
						self.code << NL() << "CALL " << res << " // Calling function with NO params"
				else:
					for call in node.calls: # Calling Nested eg. cls_instance_var.fun() , cls_instance_var.instance.fun()
						self.visit(call)

			self.flags["Call"] -= 1
			return res
		
		elif isinstance(node, ANT_CallSuffix):
			self.flags["CallSuffix"] += 1

			self.flags["CallSuffix"] -= 1

		elif isinstance(node, ANT_SuperCall):
			self.flags["SuperCall"] += 1

			self.flags["SuperCall"] -= 1

		elif isinstance(node, ANT_Primary): # Can only be called from within a call
			self.flags["Primary"] += 1
			if node.NUMBER:
				res = node.NUMBER
			elif node.STRING :
				res = node.STRING
			elif node.IDENTIFIER:
				res = node.IDENTIFIER
			elif node.operator:
				res = node.operator
			elif node.expression:
				res = self.visit(node.expression)
			elif node.superCall:
				res = self.visit(node.superCall)
			elif node.array:
				res = self.visit(node.array)
			elif node.instantiation:
				res = self.visit(node.instantiation)
			self.flags["Primary"] -= 1
			return res

		elif isinstance(node, ANT_Function):
			self.flags["Function"] += 1

			fun = Tac_Function()
			fun.ID = self.new_label()
			fun.name = node.IDENTIFIER
			if self.cls:
				fun.member = self.cls
				self.cls.member_functions.append(fun)
				if fun.name == "init":
					self.cls.initializer = fun
			else:
				self.scope.declareFunction(fun)
			self.fun = fun

			self.code << NL() << "// FUNCTION START {"
			self.code << NL() << fun.ID << ": // " << node.IDENTIFIER
			self.code += 1
			if node.parameters:
				parameters = self.visit(node.parameters)
				for parameter in parameters:
					param = Tac_Function_Parameter()
					param.ID = self.new_temp()
					param.name = parameter
					fun.parameters.append(param)

			return_val = self.visit(node.block)
			self.code -= 1
			self.code << NL() << "RETURN"
			self.code << NL() << "//} FUNCTION END"

			self.fun = None

			self.flags["Function"] -= 1
			return fun.ID

		elif isinstance(node, ANT_Variable):
			self.flags["Variable"] += 1

			var = Tac_Variable()
			var.ID = self.new_temp()
			var.name = node.IDENTIFIER
			self.scope.declareVariable(var)
			self.var = var

			if node.expression:
				expression = self.visit(node.expression)
				self.code << NL() << var.ID << ": " << expression << " // " << node.IDENTIFIER << " = " << expression
				self.var = None
			else:
				self.code << NL() << "// Declare Empty Var: " << node.IDENTIFIER

			self.flags["Variable"] -= 1
			if node.expression:
				return var.ID

		elif isinstance(node, ANT_Parameters):
			self.flags["Parameters"] += 1
			parameters: List[str] = []
			for identifier in node.identifiers:
				parameters.append(identifier)
			self.flags["Parameters"] -= 1
			return parameters

		elif isinstance(node, ANT_Arguments):
			self.flags["Arguments"] += 1
			arguments: List[str] = []
			for expression in node.expressions:
				expr = self.visit(expression)
				arguments.append(expr)
			self.flags["Arguments"] -= 1
			return arguments