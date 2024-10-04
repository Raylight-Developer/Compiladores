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
			if node.classDecl:
				self.visit(node.classDecl)
			elif node.funDecl:
				self.visit(node.funDecl)
			elif node.varDecl:
				self.visit(node.varDecl)
			elif node.statement:
				self.visit(node.statement)

		elif isinstance(node, ANT_ClassDecl):
			cls = Tac_Class()
			cls.name = node.IDENTIFIER
			self.scope.declareClass(cls)
			self.cls = cls

			self.scope.enter()
			self.visit(node.class_body)
			self.scope.exit()

			self.cls = None

		elif isinstance(node, ANT_ClassBody):
			for member in node.class_members:
				self.visit(member)

		elif isinstance(node, ANT_ClassMember):
			self.visit(node.function)

		elif isinstance(node, ANT_FunDecl):
			return self.visit(node.function)

		elif isinstance(node, ANT_VarDecl):
			return self.visit(node.variable)

		elif isinstance(node, ANT_Statement):
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

		elif isinstance(node, ANT_ExprStmt):
			self.visit(node.expression)

		elif isinstance(node, ANT_ForStmt):
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

		elif isinstance(node, ANT_IfStmt):
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

		elif isinstance(node, ANT_PrintStmt):
			self.code << NL() << "// PRINT START {"
			self.code << NL() << "SYSCALL"
			self.code += 1
			expr = self.visit(node.expression)
			self.code -= 1
			self.code << NL() << "PRINT " << expr
			self.code << NL() << "SYSCALL"
			self.code << NL() << "//} PRINT END"

		elif isinstance(node, ANT_ReturnStmt):
			pass

		elif isinstance(node, ANT_WhileStmt):
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

		elif isinstance(node, ANT_Block):
			for declaration in node.declarations:
				self.visit(declaration)

		elif isinstance(node, ANT_FunAnon):
			pass

		elif isinstance(node, ANT_Expression):
			if node.assignment:
				return self.visit(node.assignment)
			elif node.funAnon:
				return self.visit(node.funAnon)

		elif isinstance(node, ANT_Assignment):
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
			return res

		elif isinstance(node, ANT_LogicOr):
			if len(node.array) == 0:
				return self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right_node in node.array:
					right = self.visit(right_node)
					res = self.new_temp()
					self.code << NL() << f"OR {res}: {left}, {right} // {left} || {right}"
					left = res
			return res

		elif isinstance(node, ANT_LogicAnd):
			if len(node.array) == 0:
				return self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right_node in node.array:
					right = self.visit(right_node)
					res = self.new_temp()
					self.code << NL() << f"AND {res}: {left}, {right} // {left} && {right}"
					left = res
			return res

		elif isinstance(node, ANT_Equality):
			if len(node.array) == 0:
				return self.visit(node.left)
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
			return res

		elif isinstance(node, ANT_Comparison):
			if len(node.array) == 0:
				return self.visit(node.left)
			else:
				left = self.visit(node.left)
				for op, right_node in node.array:
					right = self.visit(right_node)
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
			return res

		elif isinstance(node, ANT_Term):
			if len(node.array) == 0:
				return self.visit(node.left)
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
			return res

		elif isinstance(node, ANT_Factor):
			if len(node.array) == 0:
				return self.visit(node.left)
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
			return res

		elif isinstance(node, ANT_Array):
			for expression in node.expressions:
				self.visit(expression)

		elif isinstance(node, ANT_Instantiation):

			res = self.new_temp()
			cls = self.scope.lookupClass(node.IDENTIFIER)
			arguments: List[str] = self.visit(node.arguments)
			#for argument in arguments:

			return res

		elif isinstance(node, ANT_Unary):
			if node.call:
				return self.visit(node.call)
			elif node.unary:
				right = self.visit(node.unary)
				res = self.new_temp()
				if node.operator == "-":
					self.code << NL() << f"SUB {res}: 0, {right} // - {right}"
				elif node.operator == "!":
					self.code << NL() << f"NOT {res}: {right} // ! {right}"
				return res

		elif isinstance(node, ANT_Call):
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
						res = "TODO"
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
						res = self.visit(call)
			return res

		elif isinstance(node, ANT_CallSuffix):
			pass

		elif isinstance(node, ANT_SuperCall):
			pass

		elif isinstance(node, ANT_Primary): # Can only be called from within a call
			if node.NUMBER:
				return node.NUMBER
			elif node.STRING :
				return node.STRING
			elif node.IDENTIFIER:
				return node.IDENTIFIER
			elif node.operator:
				return node.operator
			elif node.expression:
				return self.visit(node.expression)
			elif node.superCall:
				return self.visit(node.superCall)
			elif node.array:
				return self.visit(node.array)
			elif node.instantiation:
				return self.visit(node.instantiation)

		elif isinstance(node, ANT_Function):
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

			return fun.ID

		elif isinstance(node, ANT_Variable):
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

			if node.expression:
				return var.ID

		elif isinstance(node, ANT_Parameters):
			parameters: List[str] = []
			for identifier in node.identifiers:
				parameters.append(identifier)
			return parameters

		elif isinstance(node, ANT_Arguments):
			arguments: List[str] = []
			for expression in node.expressions:
				expr = self.visit(expression)
				arguments.append(expr)
			return arguments