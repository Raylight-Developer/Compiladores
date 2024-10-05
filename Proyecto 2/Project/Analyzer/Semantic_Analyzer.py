from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *

from .Symbols import *
from .Scope import *

class Semantic_Analyzer(CompiscriptVisitor):
	def __init__(self, table_c: Symbol_Table, table_f: Symbol_Table, table_v: Symbol_Table, program: CompiscriptParser.ProgramContext):
		super().__init__()

		self.output = Lace()
		self.output.current_tab = 1
		self.scope_tracker = Scope_Tracker(self.output)

		self.current_function = None
		self.current_variable = None
		self.current_class = None
		self.current_call = None

		self.table_c = table_c
		self.table_f = table_f
		self.table_v = table_v

		self.visit(program)

	def visitProgram(self, ctx:CompiscriptParser.ProgramContext):
		return self.visitChildren(ctx)

	def visitDeclaration(self, ctx:CompiscriptParser.DeclarationContext):
		return self.visitChildren(ctx)

	def visitFunDecl(self, ctx:CompiscriptParser.FunDeclContext):
		return self.visitChildren(ctx)

	def visitVarDecl(self, ctx:CompiscriptParser.VarDeclContext):
		return self.visitChildren(ctx)

	def visitStatement(self, ctx:CompiscriptParser.StatementContext):
		return self.visitChildren(ctx)

	def visitExprStmt(self, ctx:CompiscriptParser.ExprStmtContext):
		return self.visitChildren(ctx)

	def visitPrintStmt(self, ctx:CompiscriptParser.PrintStmtContext):
		return self.visitChildren(ctx)

	def visitReturnStmt(self, ctx:CompiscriptParser.ReturnStmtContext):
		if ctx.expression():
			return self.visit(ctx.expression())
		return Container(None, Type.VOID)

	def visitParameters(self, ctx:CompiscriptParser.ParametersContext):
		parameters: List[str] = []
		for identifier in ctx.IDENTIFIER():
			parameters.append(identifier.getText())
		return parameters

	def visitArguments(self, ctx:CompiscriptParser.ArgumentsContext):
		arguments = []
		for expr in ctx.expression():
			arguments.append(self.visit(expr))  # Visit and evaluate each expression
		return arguments

	def visitBlock(self, ctx:CompiscriptParser.BlockContext):
		self.scope_tracker.enterScope()
		self.visitChildren(ctx)
		self.scope_tracker.exitScope()

	def visitExpression(self, ctx: CompiscriptParser.ExpressionContext):
		res: Container = Container()

		if ctx.assignment():
			res = self.visit(ctx.assignment())
		elif ctx.funAnon():
			res = self.visit(ctx.funAnon())

		return res

	def visitFunAnon(self, ctx:CompiscriptParser.FunAnonContext):
		self.scope_tracker.enterScope()

		function = Function()
		function.ctx = ctx
		function.ID = "ANON"
		function.data = ctx.block().getText()
		self.current_function = function

		self.output << NL() << f"Declaring Anon Function [{function.ID}]"

		if ctx.parameters():
			for param in ctx.parameters().IDENTIFIER():
				parameter = Function_Parameter()
				parameter.ID = param.getText()
				parameter.function = function
				function.parameters.append(parameter)

		#self.visitChildren(ctx)
#
		self.scope_tracker.exitScope()
		self.scope_tracker.declareAnonFunction(function)
		self.addSymbolToTable(function)
		self.current_function = None
#
		return Container(function, Type.FUN_ANON)

	def visitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
		self.scope_tracker.enterScope()

		struct = Class()
		struct.ctx = ctx
		struct.ID = ctx.IDENTIFIER(0).getText()
		self.current_class = struct

		self.output << NL() << f"Declaring Class [{struct.ID}]"

		if ctx.IDENTIFIER(1):
			struct.parent = self.scope_tracker.lookupClass(ctx.IDENTIFIER(1).getText())
			for member in struct.parent.member_functions:
				member.member = struct
				member.origin = "Inherited"
				struct.member_functions.append(member)

			for member in struct.parent.member_variables:
				member.member = struct
				struct.member_variables.append(member)
				self.scope_tracker.declareVariable(member)
				self.addSymbolToTable(member)

			struct.initialzer = struct.parent.initializer

		members: List[Container[Function]] = self.visit(ctx.classBody())
#
		for member in members:
			if member.data.ID in [function.ID for function in struct.member_functions]:
				inherited = next((inherited for inherited in struct.member_functions if inherited.ID == member.data.ID), None)
				struct.member_functions.remove(inherited)
				self.removeSymbolFromTable(inherited)
				member.data.origin = "Override"
			self.scope_tracker.declareFunction(member.data)
			struct.member_functions.append(member.data)
			self.addSymbolToTable(member.data)

		self.scope_tracker.exitScope()
		self.scope_tracker.declareClass(struct)
		self.addSymbolToTable(struct)
#
		self.current_class = None
		return Container(struct, Type.CLASS)

	def visitClassBody(self, ctx:CompiscriptParser.ClassBodyContext):
		members: List[Container] = []
		for i in range(len(ctx.classMember())):
			member = self.visit(ctx.classMember(i))
			members.append(member)
		return members

	def visitClassMember(self, ctx:CompiscriptParser.ClassMemberContext):
		self.scope_tracker.enterScope()

		if ctx.function():
			function: Container = self.visit(ctx.function())
			self.scope_tracker.exitScope()
			return function

	def visitForStmt(self, ctx:CompiscriptParser.ForStmtContext):
		self.scope_tracker.enterScope()

		if ctx.varDecl():
			self.visit(ctx.varDecl())
		elif ctx.exprStmt():
			self.visit(ctx.exprStmt())

		if ctx.expression(0):
			expression: Container = self.visit(ctx.expression(0))
			if not isinstance(expression, Container) or not expression.type == Type.BOOL:
				error(self.output, f"Error For. Condition is not boolean. {expression.data}")

		if ctx.expression(1):
			self.visit(ctx.expression(1))

		self.scope_tracker.exitScope()


	def visitIfStmt(self, ctx:CompiscriptParser.IfStmtContext):
		if ctx.expression():
			expression: Container = self.visit(ctx.expression())
			
			if not isinstance(expression, Container) or not expression.type == Type.BOOL:
				error(self.output, f"Error If. IF Condition is not boolean. {expression.data}")

		if ctx.statement(0):
			return self.visit(ctx.statement(0))

		if ctx.statement(1):
			return self.visit(ctx.statement(1))

	def visitWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext):
		self.scope_tracker.enterScope()

		expression = self.visit(ctx.expression())
		if not isinstance(expression, Container) or not expression.type == Type.BOOL:
			error(self.output, f"Error While. Condition is not boolean. {expression.data}")

		self.scope_tracker.exitScope()

	def visitAssignment(self, ctx:CompiscriptParser.AssignmentContext):
		res: Container = Container()

		if ctx.logic_or():
			res = self.visit(ctx.logic_or())

		elif ctx.call():
			if ctx.call().getText() == "this":
				if self.current_class:
					memeber_var_name = ctx.IDENTIFIER().getText()
					if self.current_class:
						self.output << NL() << f"Declaring Member Variable [{memeber_var_name}]"
						variable = Variable()
						variable.ctx = ctx
						variable.ID = memeber_var_name
						variable.member = self.current_class

						assignment: Container[Function_Parameter] = self.visit(ctx.assignment())
						if assignment.type == Type.PARAMETER:
							variable.data = assignment.data.ID
							variable.type = assignment.type
						else:
							variable.data = assignment.data
							variable.type = assignment.type

						for member in self.current_class.member_variables:
							if member.ID == variable.ID:
								self.current_class.member_variables.remove(member)
								#self.removeSymbolFromTable(member)
								variable.origin = "Override"

						self.current_class.member_variables.append(variable)
						self.scope_tracker.declareVariable(variable)
						self.addSymbolToTable(variable)

						res = Container(variable, Type.VARIABLE)
					else:
						error(self.output, "NOT IMPLEMENTED")
				else:
					error(self.output, "Error Assignment. There is no parent to define a variable member to.")
			else:
				instance: Container[Variable] = self.visit(ctx.call())
				if instance.type == Type.INSTANCE:
					if instance.data.data.checkVariable(ctx.IDENTIFIER().getText()):
						code = self.visit(ctx.assignment()) # TODO
						var = instance.data.data.lookupVariable(ctx.IDENTIFIER().getText())
						var.data = code
						self.updateSymbolFromTable(var)

						res = Container(var, Type.INSTANCE)
					else:
						error(self.output, f"Error Assignment. {instance.data.data.ID}.{ctx.IDENTIFIER().getText()} is not defined")

		elif ctx.IDENTIFIER():
			var_name = str(ctx.IDENTIFIER())
			self.output << NL() << "Assigning Value to [" << var_name << "]"

			if self.scope_tracker.checkVariable(var_name, None):
				var = self.scope_tracker.lookupVariable(var_name, None)
				var.data = self.visit(ctx.assignment())
				self.updateSymbolFromTable(var)

				res = Container(var, Type.VARIABLE)
			else:
				error(self.output, f"Error Assignment. Cannot assign value to an undeclared variable {var_name}")

		return res

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		res: Container = Container()

		left: Container = self.visit(ctx.logic_and(0))
		res = left
		for i in range(1, len(ctx.logic_and())):
			right: Container = self.visit(ctx.logic_and(i))
			res = Container(f"({left.data} or {right.data})", Type.BOOL)

		return res

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		res: Container = Container()

		left: Container = self.visit(ctx.equality(0))
		res = left
		for i in range(1, len(ctx.equality())):
			right: Container = self.visit(ctx.equality(i))
			res = Container(f"({left.data} and {right.data})", Type.BOOL)

		return res

	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		res: Container = Container()

		left: Container = self.visit(ctx.comparison(0))
		res = left
		for i in range(1, len(ctx.comparison())):
			operator = ctx.getChild(2 * i - 1).getText()
			right: Container = self.visit(ctx.comparison(i))
			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.output, f"Error Equality. {type(left)}({left}) {operator} {type(right)}({right})")
			comparisonCheck(self.output, left, operator, right)
			res = Container(f"({left.data} {operator} {right.data})", Type.BOOL)

		return res

	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		res: Container = Container()

		left: Container = self.visit(ctx.term(0))
		res = left
		for i in range(1, len(ctx.term())):
			operator: str = ctx.getChild(2 * i - 1).getText()
			right: Container = self.visit(ctx.term(i))
			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.output, f"Error Comparison. {type(left)}({left}) {operator.replace('<', 'less').replace('>', 'greater')} {type(right)}({right})")
			comparisonCheck(self.output, left, operator, right)
			res = Container(f"({left.innermostCode()} {operator} {right.innermostCode()})", Type.BOOL)

		return res

	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		res: Container = Container()

		left : Container = self.visit(ctx.factor(0))
		res = left
		for i in range(1, len(ctx.factor())):
			right : Container = self.visit(ctx.factor(i))
			operator: str = ctx.getChild(2 * i - 1).getText()

			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.output, f"Error Term. Evaluating Expression: Unkwown Arguments. {type(left)}[{left}] {operator} {type(right)}[{right}]")

			operation_type = operationType(self.output, left, operator, right)

			res = Container(f"({left.innermostCode()} {operator} {right.innermostCode()})", operation_type)

		return res

	def visitFactor(self, ctx:CompiscriptParser.FactorContext):
		res: Container = Container()

		left : Container = self.visit(ctx.unary(0))
		res = left

		for i in range(1, len(ctx.unary())):
			right : Container = self.visit(ctx.unary(i))
			operator: str = ctx.getChild(2 * i - 1).getText()

			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.output, f"Error Factor. Evaluating Expression: Unkwown Arguments. {type(left)}[{left}] {operator} {type(right)}[{right}]")

			operation_type = operationType(self.output, left, operator, right)

			res = Container(f"({left.innermostCode()} {operator} {right.innermostCode()})", operation_type)

		return res

	def visitArray(self, ctx:CompiscriptParser.ArrayContext):
		res: Container = Container()

		elements: List[Container] = []
		if ctx.expression():
			for expr in ctx.expression():
				elements.append(self.visit(expr))

		return Container(elements, Type.ARRAY)

	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
		class_name = ctx.IDENTIFIER().getText()
		struct = self.scope_tracker.lookupClass(class_name)

		args = []
		if ctx.arguments():
			args = self.visit(ctx.arguments())

		if struct.initializer:
			if len(args) != len(struct.initializer.parameters):
				error(self.output, f"Error Intantiation. Tried to Instantiate '{class_name}' with {len(args)} parameters. Expected {len(struct.initializer.parameters)}")
		elif len(args) != 0:
			error(self.output, f"Error Intantiation. Tried to Instantiate '{class_name}' with {len(args)} parameters. Expected NONE")

		return Container(self.scope_tracker.lookupClass(class_name), Type.CLASS)

	def visitUnary(self, ctx:CompiscriptParser.UnaryContext):
		res: Container = Container()

		if ctx.getChildCount() == 2:
			operator = ctx.getChild(0).getText()
			operand: Container = self.visit(ctx.unary())
			if operator == '-':
				if operand.type == Type.INT or operand.type == Type.FLOAT:
					res = Container(f"-{operand.data}", operand.type)
				else:
					error(self.output, f"Error Unary. Applying operator {operator} to <{operand.type}>({operand.data})")
			elif operator == '!':
				if operand.type == Type.BOOL:
					res = Container(f"!{operand.data}", operand.type)
				else:
					error(self.output, f"Error Unary. Applying {operator} to <{operand.type}>({operand.data})")
		else:
			res = self.visit(ctx.call())

		return res

	def visitCall(self, ctx:CompiscriptParser.CallContext):
		res: Container = Container()

		if ctx.getChildCount() == 1:
			if ctx.primary():
				res = self.visit(ctx.primary())
			elif ctx.funAnon():
				res = self.visit(ctx.funAnon())
		elif ctx.primary():
			primary: Container = self.visit(ctx.primary())
			if primary.type == Type.FUNCTION:
				if (self.current_function and self.current_function.ID != primary.data.ID )or (self.current_call and self.current_call != primary.data.ID):
					self.current_call = primary.data.ID
					call_params = []
					if ctx.callSuffix() and len(ctx.callSuffix()) > 0:
						arguments: CompiscriptParser.ArgumentsContext = ctx.callSuffix(0).arguments()
						for i in range(0, arguments.getChildCount(), 2):
							call_params.append(self.visit(arguments.getChild(i)))
					elif self.current_function.parameters:
						self.current_call = None
					if len(self.current_function.parameters) != len(call_params):
						error(self.output, f"Error Call. Tried to call Function '{self.current_function.ID}' with {len(call_params)} parameters. Expected {len(self.current_function.parameters)}")
				elif (self.current_function and self.current_function.ID == primary.data.ID) or (self.current_call and self.current_call == primary.data.ID):
					if self.current_function:
						self.current_function.recursive = True
						self.updateSymbolFromTable(self.current_function)
				else:
					call_params = []
					if ctx.callSuffix() and len(ctx.callSuffix()) > 0:
						if ctx.callSuffix(0).arguments():
							arguments: CompiscriptParser.ArgumentsContext = ctx.callSuffix(0).arguments()
							for i in range(0, arguments.getChildCount(), 2):
								call_params.append(self.visit(arguments.getChild(i)))
					if len(primary.data.parameters) != len(call_params):
						error(self.output, f"Error Call. Tried to call Function '{primary.data.ID}' with {len(call_params)} parameters. Expected {len(primary.data.parameters)}")
				res = primary
			elif primary.type == Type.THIS: # Accesing a variable from self
				if self.current_class is None:
					error(self.output, "Error Call. Calling this outside of class")
				elif self.current_class:
					var_name = ctx.callSuffix(0).IDENTIFIER().getText()
					if self.current_class.lookupVariable(var_name):
						return Container(self.current_class.lookupVariable(var_name), Type.VARIABLE)
					error(self.output, f"Error Call. Trying to acces undefined variable {self.current_class.ID}.{var_name}")
			elif primary.type == Type.INSTANCE:
				child_count = ctx.getChildCount()
				# Verify if there is a nested call or variable
				if child_count > 3:  # Checks if there are more elements indicating a chain
					current_instance: Class | Variable | Function = primary.data.data  # Start with the first instance
					for i in range(2, child_count, 2):  # Iterate over each chained element (assuming format: instance '.' member)
						member_name = ctx.getChild(i).getText()
						if isinstance(current_instance, Variable):
							return Container(current_instance, Type.VARIABLE)
						# It's a function call
						if i + 1 < child_count and ctx.getChild(i + 1).getText() == '(':
							function = self.scope_tracker.lookupFunction(member_name, current_instance)
							call_params = []
							if ctx.callSuffix() and len(ctx.callSuffix()) > 0:
								arguments: CompiscriptParser.ArgumentsContext = ctx.callSuffix(0).arguments()
								for j in range(0, arguments.getChildCount(), 2):
									call_params.append(self.visit(arguments.getChild(j)))
							# Check if the parameters match the function definition
							if len(function.parameters) != len(call_params):
								error(self.output, f"Error Call. Tried to call Function '{function.ID}' with {len(call_params)} parameters. Expected {len(function.parameters)}")
							# Move to the next instance for further chained calls, if any
							if function.return_type == Type.VOID:
								break
							current_instance = function.return_type  # Update the current instance to function's return type
						# It's a variable access
						else:
							variable = self.scope_tracker.lookupVariable(member_name, current_instance)
							current_instance = variable  # Update current instance to variable's type
					return Container(current_instance, Type.INSTANCE)
				# Single function call or variable access
				else:
					member_name = ctx.callSuffix(0).IDENTIFIER().getText()
					# Function call
					if ctx.getChild(2) and (ctx.getChild(2).getText() == "()" or ctx.getChild(2).arguments()):
						function = self.scope_tracker.lookupFunction(member_name, primary.data.data)
						call_params = []
						if ctx.callSuffix() and len(ctx.callSuffix()) > 0:
							arguments: CompiscriptParser.ArgumentsContext = ctx.callSuffix(0).arguments()
							if arguments:
								for i in range(0, arguments.getChildCount(), 2):
									call_params.append(self.visit(arguments.getChild(i)))
						if len(function.parameters) != len(call_params):
							error(self.output, f"Error Call. Tried to call Function '{function.ID}' with {len(call_params)} parameters. Expected {len(function.parameters)}")
						self.current_call = None
						# Return the called function
						return function
					# Variable access
					else:
						return Container(self.scope_tracker.lookupVariable(member_name, primary.data.data), Type.VARIABLE)
			
			elif primary.type == Type.SUPER:
				if not self.current_class:
					error(self.output, "Calling super outside of Class")
				if not self.current_class.parent.initializer:
					error(self.output, f"Calling super in a Class {self.current_class} whose parent class {self.current_class.parent} does not have a init() method.")
				call_params = []
				if ctx.callSuffix() and len(ctx.callSuffix()) > 0:
					arguments: CompiscriptParser.ArgumentsContext = ctx.callSuffix(0).arguments()
					for i in range(0, arguments.getChildCount(), 2):
						call_params.append(self.visit(arguments.getChild(i)))
				if len(self.current_class.parent.initializer.parameters) != len(call_params):
					error(self.output, f"Error Call. Tried to call Super Function '{self.current_function.ID}' with {len(call_params)} parameters. Expected {len(self.current_class.parent.initializer.parameters)}")

		return res

	def visitSuperCall(self, ctx: CompiscriptParser.SuperCallContext):
		res = None

		if not ctx.IDENTIFIER():
			error(self.output, "Error Super. Empy super call")
		if not self.current_class:
			error(self.output, "Error Super. Calling super outside of class")
		if not self.current_class.parent:
			error(self.output, "Error Super. Calling super in a class with no parent")

		member_name: str = ctx.IDENTIFIER().getText()
		if self.current_class.parent.checkFunction(member_name):
			function = self.current_class.lookupFunction(member_name)
			res = Container(function, Type.SUPER)
		else:
			error(self.output, f"Error Super. No function in hierarchy named '{member_name}'")

		return res

	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
		res: Container = Container()

		if ctx.NUMBER():
			text = str(ctx.NUMBER())
			if '.' in text:
				res = Container(text, Type.FLOAT)
			else:
				res = Container(text, Type.INT)
		elif ctx.STRING():
			text = str(ctx.STRING()).strip('"')
			res = Container(text, Type.STRING)
		elif ctx.IDENTIFIER():
			ID = ctx.IDENTIFIER().getText()
			if self.scope_tracker.checkVariable(ID, self.current_class):
				variable = self.scope_tracker.lookupVariable(ID, self.current_class)
				type = Type.INSTANCE if variable.type == Type.CLASS else Type.VARIABLE
				res = Container(variable, type)
			elif self.scope_tracker.checkFunction(ID, self.current_class):
				res = Container(self.scope_tracker.lookupFunction(ID, self.current_class), Type.FUNCTION)
			elif self.current_function:
				res = Container(self.current_function.lookupParameter(ID), Type.PARAMETER)
			else:
				error(self.output, f"Error Primary. Variable '{ID}' not defined")

		elif ctx.array():
			res = self.visit(ctx.array())
		elif ctx.instantiation():
			res = self.visit(ctx.instantiation())
		elif ctx.expression():
			res = self.visit(ctx.expression())
		elif ctx.superCall():
			res = self.visit(ctx.superCall())

		elif ctx.getText() == "true":
			res = Container("true", Type.BOOL)
		elif ctx.getText() == "false":
			res = Container("false", Type.BOOL)
		elif ctx.getText() == "nil":
			res = Container("nil", Type.NONE)
		elif ctx.getText() == "this":
			res = Container("this", Type.THIS)
		elif ctx.superCall():
			res = Container(ctx.superCall().getChild(2).getText(), Type.SUPER)

		return res

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		self.scope_tracker.enterScope()

		function = Function()
		function.ctx = ctx
		function.ID = ctx.IDENTIFIER().getText()
		function.data = ctx.block().getText()
		self.current_function = function

		self.output << NL() << f"Declaring Function [{function.ID}]"

		if ctx.parameters():
			for param in ctx.parameters().IDENTIFIER():
				parameter = Function_Parameter()
				parameter.ID = param.getText()
				parameter.function = function
				function.parameters.append(parameter)

		if self.current_class:
			function.member = self.current_class
			if function.ID == "init":
				self.current_class.initializer = function

		self.visitChildren(ctx)
#
		self.scope_tracker.exitScope()
		if not self.current_class:
			self.scope_tracker.declareFunction(function)
			self.addSymbolToTable(function)
		self.current_function = None
#
		return Container(function, Type.FUNCTION)

	def visitVariable(self, ctx:CompiscriptParser.VariableContext):
#
		variable = Variable()
		variable.ctx = ctx
		variable.ID = ctx.IDENTIFIER().getText()
		variable.data = ctx.getText()
#
		if self.current_class:
			variable.member = self.current_class
#
		self.output << NL() << f"Declaring Variable [{variable.ID}]"
#
		self.scope_tracker.declareVariable(variable)
		if ctx.expression():
			var: Container = self.visit(ctx.expression())
			variable.data = var.data
			variable.type = var.type

		self.addSymbolToTable(variable)
#
		return Container(variable, Type.INSTANCE if variable.type == Type.CLASS else Type.VARIABLE)

	def addSymbolToTable(self, value: Class | Function | Variable):
		if isinstance(value, Class):
			self.table_c.addSymbol(value)
		elif isinstance(value, Function):
			self.table_f.addSymbol(value)
		elif isinstance(value, Variable):
			self.table_v.addSymbol(value)

	def removeSymbolFromTable(self, value: Class | Function | Variable):
		if isinstance(value, Class):
			self.table_c.removeSymbol(value)
		elif isinstance(value, Function):
			self.table_f.removeSymbol(value)
		elif isinstance(value, Variable):
			self.table_v.removeSymbol(value)

	def updateSymbolFromTable(self, value: Class | Function | Variable):
		if isinstance(value, Class):
			self.table_c.updateSymbol(value)
		elif isinstance(value, Function):
			self.table_f.updateSymbol(value)
		elif isinstance(value, Variable):
			self.table_v.updateSymbol(value)