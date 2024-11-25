from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.QT import *

from .Symbols import *
from .Scope import *
from .TAC_Data import *
from .Classes import *
from .Tree import *

class TAC_Generator():
	def __init__(self, table_c: Symbol_Table, table_f: Symbol_Table, table_v: Symbol_Table, program: CompiscriptParser.ProgramContext, info: bool = True):
		super().__init__()
		self.label_count = -1
		self.temp_count = -1

		self.tree = Tree_Generator()
		self.scope = Tac_Scope_Tracker()
		self.program: ANT_Program = self.tree.visitProgram(program)

		self.parent_depth = 0
		self.cls: Tac_Class = None
		self.fun: Tac_Function = None
		self.var: Tac_Variable = None

		self.info = info
		self.debug = Lace()
		self.output = Lace()
		self.fallback = Lace()

		self.table_c = table_c
		self.table_f = table_f
		self.table_v = table_v

		self.visit(self.program)
		self.addSymbols()

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
				return self.visit(node.classDecl)
			elif node.funDecl:
				return self.visit(node.funDecl)
			elif node.varDecl:
				return self.visit(node.varDecl)
			elif node.statement:
				return self.visit(node.statement)

		elif isinstance(node, ANT_ClassDecl):
			cls = Tac_Class()
			cls.name = node.IDENTIFIER
			self.scope.declareClass(cls)
			cls.code = node.class_body
			if node.extends:
				cls.extends = self.scope.lookupClass(node.extends)

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
				return self.visit(node.returnStmt)
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
				self.com() << NL() << "// FOR LOOP START {"
				self.add() << NL() << start << ":"
				self.cominc()
				end = self.new_label()

				if node.compare_expression:
					self.com() << NL() << "// COMPARE"
					compare = self.visit(node.compare_expression)
					self.add() << NL() << "IF " << compare << " GO_TO " << end
					if node.increment_expression:
						self.com() << NL() << "// INCREMENT"
						increment = self.visit(node.increment_expression)
						self.add() << NL() << fun << ": " << increment
				self.com() << NL() << "// FOR LOOP BODY START {"
				self.cominc()
				self.visit(node.statement)
				self.comdec()
				self.com() << NL() << "//} FOR LOOP BODY END"
				self.add() << NL() << "GO_TO " << start

				self.comdec()
				self.add() << NL() << end << ":"
				self.com() << NL() << "//} FOR LOOP END"
			elif node.exprStmt:
				self.visit(node.exprStmt)

		elif isinstance(node, ANT_IfStmt):
			true = self.new_label()

			self.com() << NL() << "// IF START {"
			end = self.new_label()

			if node.expression:
				self.com() << NL() << "// COMPARE"
				compare = self.visit(node.expression)
				self.add() << NL() << "IF " << compare << " GO_TO " << true

			if node.else_statement:
				self.com() << NL() << "// FALSE"
				self.inc()
				self.visit(node.else_statement)
				self.add() << NL() << "GO_TO " << end
				self.dec()
	
			self.com() << NL() << "// TRUE"
			self.add() << NL() << true << ":"
			self.inc()
			self.visit(node.if_statement)
			self.add() << NL() << "GO_TO " << end
			self.dec()

			self.add() << NL() << end << ":"
			self.com() << NL() << "//} IF END"

		elif isinstance(node, ANT_PrintStmt):
			self.com() << NL() << "// PRINT START {"
			self.add() << NL() << "SYSCALL"
			self.inc()
			expr = self.visit(node.expression)
			self.dec()
			self.add() << NL() << "PRINT " << expr
			self.add() << NL() << "SYSCALL"
			self.com() << NL() << "//} PRINT END"

		elif isinstance(node, ANT_ReturnStmt):
			expr = self.visit(node.expression)
			self.add() << NL() << self.fun.return_ID << ": " << expr
			self.com() << " // return val"
			#self.add() << NL() << "RETURN"

		elif isinstance(node, ANT_WhileStmt):
			start = self.new_label()
			self.com() << NL() << "// WHILE LOOP START {"
			self.add() << NL() << start << ":"
			self.inc()
			end = self.new_label()

			if node.expression:
				self.com() << NL() << "// COMPARE"
				compare = self.visit(node.expression)
				not_temp = self.new_temp()
				self.add() << NL() << "NOT " << not_temp << ": " << compare
				self.add() << NL() << "IF " << not_temp << " GO_TO " << end
			
			self.com() << NL() << "// WHILE LOOP BODY START {"
			self.inc()
			self.visit(node.statement)
			self.dec()
			self.com() << NL() << "//} WHILE LOOP BODY END"
			self.add() << NL() << "GO_TO " << start

			self.dec()
			self.add() << NL() << end << ":"
			self.com() << NL() << "//} WHILE LOOP END"

		elif isinstance(node, ANT_Block):
			self.scope.enter()
			res = None
			for declaration in node.declarations:
				decl = self.visit(declaration)
				if decl: res = decl

			self.scope.exit()
			return res

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

						if self.cls:
							parent = self.cls
							if self.parent_depth > 0:
								for i in range(self.parent_depth):
									parent = parent.extends
									var.member = parent
									parent.member_variables[var.name] = var
							else:
								var.member = self.cls
								self.cls.member_variables[var.name] = var
						else:
							self.scope.declareVariable(var)
						self.var = var
						res = self.visit(node.assignment)
						self.add() << NL() << var.ID << ": " << res
						self.com() << " // " << node.IDENTIFIER << " = " << res
					else:
						self.visit(node.call)
				elif node.assignment: # Late Init
					res = self.visit(node.assignment)
					if isinstance(res, Tac_Class):
						print("INSTANCE LATE INIT")
					self.add() << NL() << self.scope.lookupVariable(node.IDENTIFIER, self.cls).ID << ": " << res
					self.com() << " // " << node.IDENTIFIER << " = " << res
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
					self.add() << NL() << f"OR {res}: {left}, {right}"
					self.com() << f" // {left} || {right}"
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
					self.add() << NL() << f"AND {res}: {left}, {right}"
					self.com() << f" // {left} && {right}"
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
						self.add() << NL() << f"EQ {res}: {left}, {right}"
						self.com() << f" // {left} == {right}"
					elif op == "!=":
						self.add() << NL() << f"NEQ {res}: {left}, {right}"
						self.com() << f" // {left} != {right}"
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
						self.add() << NL() << f"LT {res}: {left}, {right}"
						self.com() << f" // {left} < {right}"
					elif op == "<=":
						self.add() << NL() << f"LEQ {res}: {left}, {right}"
						self.com() << f" // {left} <= {right}"
					elif op == ">":
						self.add() << NL() << f"GT {res}: {left}, {right}"
						self.com() << f" // {left} > {right}"
					elif op == ">=":
						self.add() << NL() << f"GEQ {res}: {left}, {right}"
						self.com() << f" // {left} >= {right}"
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
						self.add() << NL() << f"ADD {res}: {left}, {right}"
						self.com() << f" // {left} + {right}"
					elif op == "-":
						self.add() << NL() << f"SUB {res}: {left}, {right}"
						self.com() << f" // {left} - {right}"
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
						self.add() << NL() << f"MUL {res}: {left}, {right}"
						self.com() << f" // {left} * {right}"
					elif op == "/":
						self.add() << NL() << f"DIV {res}: {left}, {right}"
						self.com() << f" // {left} / {right}"
					elif op == "%":
						self.add() << NL() << f"MOD {res}: {left}, {right}"
						self.com() << f" // {left} % {right}"
					left = res
			return res

		elif isinstance(node, ANT_Array):
			array = []
			ID = self.new_temp()
			length = self.new_temp()
			for expression in node.expressions:
				array.append(self.visit(expression))
			self.com() << NL() << "// ARRAY START {"
			self.cominc()
			self.add() << NL() << length << ": " << len(array)
			self.add() << NL() << "ALLOCATE " << ID << ", " << length
			self.com() << NL() << "// ELEMENT START {"
			self.cominc()
			for i, element in enumerate(array):
				self.add() << NL() << f"MOV [IT_ARRAY_PTR + {i}], " << element
			self.comdec()
			self.com() << NL() << "//} ELEMENT END"
			self.comdec()
			self.com() << NL() << "//} ARRAY END"
			self.var.array = array
			self.var.length = length
			return ID

		elif isinstance(node, ANT_Instantiation):
			cls = self.scope.lookupClass(node.IDENTIFIER)

			self.var.instance = cls
			self.com() << NL() << "// INSTANTIATE CLASS " << cls.name << " {"
			self.cls = cls
			parent = cls
			while parent.extends != None:
				parent = parent.extends
				self.parent_depth += 1
				self.inc()
				self.visit(parent.code)
				self.dec()
			self.parent_depth = 0
			self.inc()
			self.visit(cls.code)
			self.dec()
			self.com() << NL() << "//} INSTANTIATE CLASS"

			self.com() << NL() << "// INIT CLASS {"
			params = []
			if node.arguments:
				arguments: List[str] = self.visit(node.arguments)
				for i, argument in enumerate(arguments):
					self.add() << NL() << "PUSH " << cls.initializer.ID << "[" << cls.initializer.parameters[i].ID << "]: " << argument
					self.com() << " // Param " << cls.name << "::init::[" << cls.initializer.parameters[i].name << "] = " << argument
					params.append((cls.initializer.parameters[i].name, cls.initializer.parameters[i].ID))

				self.add() << NL() << "CALL " << cls.initializer.ID
				self.com() << " // Calling " << cls.name << ".init function with params " << str(params)
			else:
				self.add() << NL() << "CALL " << cls.initializer.ID
				self.com() << " // Calling " << cls.name << ".init function with NO params"

			self.com() << NL() << "//} INIT CLASS"

			self.cls = None
			return cls

		elif isinstance(node, ANT_Unary):
			if node.call:
				return self.visit(node.call)
			elif node.unary:
				right = self.visit(node.unary)
				res = self.new_temp()
				if node.operator == "-":
					self.add() << NL() << f"SUB {res}: 0, {right}"
					self.com() << f" // - {right}"
				elif node.operator == "!":
					self.add() << NL() << f"NOT {res}: {right}"
					self.com() << f" // ! {right}"
				return res

		elif isinstance(node, ANT_Call):
			if node.funAnon:
				res = self.visit(node.funAnon)
			elif node.primary:
				primary = self.visit(node.primary)
				if len(node.calls) == 0 :
					res = primary # Calling Variable
					pass
				elif len(node.calls) == 1:
					call = node.calls[0]
					if call.IDENTIFIER: # Calling Member Variable
						if primary == 'this':
							res = self.scope.lookupVariable(call.IDENTIFIER, self.cls).ID
						else:
							var = self.scope.lookupVariable(node.primary.IDENTIFIER, self.cls)
							if call.IDENTIFIER == "length":
								if var.length:
									res = var.length
								else:
									res = var.instance.lookupVariable(call.IDENTIFIER).ID
							else:
								res = var.instance.lookupVariable(call.IDENTIFIER).ID
					elif call.expression: # Calling the index of an array [expression]
						expression = self.visit(call.expression)
						self.add() << NL() << "IT_ARRAY_PTR: " << primary << ", [" << expression << "]"
						res = "IT_ARRAY_PTR"
					elif call.arguments: # Calling Function with params
						if node.primary.superCall:
							function: Tac_Function = self.cls.extends.initializer
							res = function.return_ID
							arguments = self.visit(call.arguments)
							params = []
							for i, param in enumerate(function.parameters):
								self.add() << NL() << "PUSH " << function.ID << "[" <<  param.ID << "]: " << arguments[i]
								self.com() << " // Param " << function.name << "::[" << param.name << "] = " << arguments[i]
								params.append((param.name, param.ID))
							self.add() << NL() << "CALL " << function.ID
							self.com() << " // Calling super." << function.name << " function with params " << str(params)
						else:
							function: Tac_Function = self.scope.lookupFunction(node.primary.IDENTIFIER, self.cls)
							res = function.return_ID
							arguments = self.visit(call.arguments)
							params = []
							for i, param in enumerate(function.parameters):
								self.add() << NL() << "PUSH " << function.ID << "[" << param.ID << "]: " << arguments[i]
								self.com() << " // Param " << function.name << "::[" << param.name << "] = " << arguments[i]
								params.append((param.name, param.ID))
							self.add() << NL() << "CALL " << function.ID
							self.com() << " // Calling function " << function.name << " with params " << str(params)
					elif call.empty: # Calling Function with no params
						if node.primary.superCall:
							function: Tac_Function = self.cls.extends.initializer
							res = function.return_ID
							self.add() << NL() << "CALL " << function.ID
							self.com() << " // Calling super." << function.name << " function with NO params"
						else:
							function: Tac_Function = self.scope.lookupFunction(node.primary.IDENTIFIER, self.cls)
							res = function.return_ID
							self.add() << NL() << "CALL " << function.ID
							self.com() << " // Calling function " << function.name << " with NO params"
				elif len(node.calls) == 2: # Calling Instance
					call_a = node.calls[0]
					call_b = node.calls[1]
					if call_a.IDENTIFIER:
						if call_b.arguments:
							if primary == 'this':
								function = self.cls.lookupFunction(call_a.IDENTIFIER)
							else:
								function = self.scope.lookupVariable(node.primary.IDENTIFIER).instance.lookupFunction(call_a.IDENTIFIER)
							res = function.return_ID
							arguments = self.visit(call_b.arguments)
							params = []
							for i, param in enumerate(function.parameters):
								self.add() << NL() << "PUSH " << function.ID << "[" << param.ID << "]: " << arguments[i]
								self.com() << " // Param " << function.name << "::[" << param.name << "] = " << arguments[i]
								params.append((param.name, param.ID))
							self.add() << NL() << "CALL " << function.ID
							self.com() << " // Calling function with params " << str(params)
						elif call_b.empty:
							primary = self.visit(node.primary)
							if primary == 'this':
								function = self.cls.lookupFunction(call_a.IDENTIFIER)
							else:
								function = self.scope.lookupVariable(node.primary.IDENTIFIER, self.cls).instance.lookupFunction(call_a.IDENTIFIER)
							res = function.return_ID
							self.add() << NL() << "CALL " << function.ID
							self.com() << " // Calling function with NO params"
						#res = call_a.IDENTIFIER
					elif call_a.expression: # Calling the index of an array [expression]
						res = "TODO"
					elif call_a.arguments: # Calling Function with params
						function: Tac_Function = self.scope.lookupFunction(node.primary.IDENTIFIER, self.cls)
						res = function.return_ID
						arguments = self.visit(call_a.arguments)
						params = []
						for i, param in enumerate(function.parameters):
							self.add() << NL() << "PUSH " << function.ID << "[" << param.ID << "]: " << arguments[i]
							self.com() << " // Param " << function.name << "::[" << param.name << "] = " << arguments[i]
							params.append((param.name, param.ID))
						self.add() << NL() << "CALL " << res
						self.com() << " // Calling function with params"  << str(params)
					elif call_a.empty: # Calling Function with no params
						function: Tac_Function = self.scope.lookupFunction(node.primary.IDENTIFIER, self.cls)
						res = function.return_ID
						self.add() << NL() << "CALL " << res
						self.com() << " // Calling function with NO params"
				else:
					# Calling Nested eg. cls_instance_var.fun() , cls_instance_var.instance.fun()
					i = 1
					while i < len(node.calls):
						call = node.calls[i]
						if i == len(node.calls) - 1: # Last Element
							res = None
						else:
							if call.IDENTIFIER:
								if i < len(node.calls):
									if node.calls[i+1].empty:
										nested = self.scope.lookupFunction(call.IDENTIFIER)
										i += 1
									elif node.calls[i+1].arguments:
										pass
										i += 1
									else:
										nested = self.scope.lookupVariable(call.IDENTIFIER)
								else:
									nested = self.scope.lookupVariable(call.IDENTIFIER)
							elif call.expression:
								nested = None
							elif call.arguments:
								nested = None
							elif call.empty:
								nested = None
						i += 1
			return res

		elif isinstance(node, ANT_CallSuffix):
			pass

		elif isinstance(node, ANT_SuperCall):
			return node

		elif isinstance(node, ANT_Primary): # Can only be called from within a call
			if node.NUMBER:
				return node.NUMBER
			elif node.STRING :
				return node.STRING
			elif node.IDENTIFIER:
				if self.fun and self.fun.lookupParameter(node.IDENTIFIER):
					return self.fun.lookupParameter(node.IDENTIFIER).ID
				elif self.scope.lookupVariable(node.IDENTIFIER, self.cls):
					return self.scope.lookupVariable(node.IDENTIFIER, self.cls).ID
				else:
					return self.scope.lookupFunction(node.IDENTIFIER, self.cls).return_ID # Recursive Function Call
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
			fun.return_ID = self.new_temp()
			fun.name = node.IDENTIFIER
			if self.cls:
				parent = self.cls
				if self.parent_depth > 0:
					for i in range(self.parent_depth):
						parent = parent.extends

						fun.member = parent
						parent.member_functions[fun.name] = fun
						if fun.name == "init":
							parent.initializer = fun
				else:
					fun.member = self.cls
					self.cls.member_functions[fun.name] = fun
					if fun.name == "init":
						self.cls.initializer = fun
			else:
				self.scope.declareFunction(fun)

			self.fun = fun

			self.com() << NL() << "// FUNCTION START {"
			self.add() << NL() << fun.ID << ":"
			self.com() << "// " << node.IDENTIFIER
			self.inc()
			if node.parameters:
				parameters = self.visit(node.parameters)
				for parameter in parameters:
					param = Tac_Function_Parameter()
					param.ID = self.new_temp()
					param.name = parameter
					fun.parameters.append(param)
					self.com() << NL() << "// Fun: " << fun.name << " Has Param: " << param.ID

			self.scope.enter()
			self.visit(node.block)
			self.scope.exit()
			self.dec()
			self.add() << NL() << "RETURN"
			self.com() << NL() << "//} FUNCTION END"

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
				if not isinstance(expression, Tac_Class):
					self.add() << NL() << var.ID << ": " << expression
					self.com() << " // " << node.IDENTIFIER << " = " << str(expression)

				self.var = None
				return var.ID

			self.com() << NL() << "// Declare Empty Var: " << node.IDENTIFIER
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

	def deb(self):
		return self.debug

	def com(self):
		if self.info:
			return self.output
		return self.fallback

	def add(self):
		return self.output

	def cominc(self):
		if self.info:
			self.output += 1

	def comdec(self):
		if self.info:
			self.output -= 1

	def inc(self):
		self.output += 1

	def dec(self):
		self.output -= 1

	def addSymbols(self):
		offset = 0
		for scope in reversed(self.scope.persistent_stack):
			for key, value in scope.items():
				if isinstance(value, Tac_Class):
					value.offset = offset
					offset += 8
					for i, var in enumerate(value.member_variables.values()):
						offset += 8
						var.offset = i*8 + 8
						self.table_v.addSymbol(var)
					for fun in value.member_functions.values():
						self.table_f.addSymbol(fun)
					self.table_c.addSymbol(value)
				elif isinstance(value, Tac_Function):
					self.table_f.addSymbol(value)
				elif isinstance(value, Tac_Variable):
					if not value.member:
						value.offset = offset
						offset += 8
					self.table_v.addSymbol(value)