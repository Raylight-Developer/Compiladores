from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from .Symbols import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *
from .Scope import *

FULL_VIEW = False

class Semantic_Analyzer(CompiscriptVisitor):
	def __init__(self, debug: Lace, table_c: Symbol_Table, table_f: Symbol_Table, table_v: Symbol_Table, parser: CompiscriptParser):
		super().__init__()
		self.parser = parser
		self.compiled = True

		self.debug = debug
		self.count = 0
		self.graph = Digraph()
		self.scope_tracker = Scope_Tracker(debug)

		self.current_call      : str = None

		self.current_class    : Class    = None
		self.current_instance : Variable = None
		self.current_function : Function = None
		self.current_variable : Variable = None

		self.table_c = table_c
		self.table_f = table_f
		self.table_v = table_v

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

	def visitFunAnon(self, ctx:CompiscriptParser.FunAnonContext):
		"""Create Scoped Lambda-ish Function"""
		self.enter("Anon Function")
		self.scope_tracker.enterScope()

		function = Function()
		function.ctx = ctx
		function.ID = "ANON"
		function.data = ctx.block().getText()
		self.current_function = function

		self.debug << NL() << f"Declaring Anon Function [{function.ID}]"

		if ctx.parameters():
			for param in ctx.parameters().IDENTIFIER():
				parameter = Function_Parameter()
				parameter.ID = param.getText()
				parameter.function = function
				function.parameters.append(parameter)

		self.visitChildren(ctx)
#
		self.scope_tracker.exitScope()
		self.scope_tracker.declareAnonFunction(function)
		self.addSymbolToTable(function)
		self.current_function = None
#
		self.exit("Anon Function")
		return Container(function, Type.FUN_ANON)

	def visitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
		self.enter("Class Declaration")
		self.scope_tracker.enterScope()

		struct = Class()
		struct.ctx = ctx
		struct.ID = ctx.IDENTIFIER(0).getText()
		self.current_class = struct

		if ctx.IDENTIFIER(1):
			struct.parent = self.scope_tracker.lookupClass(ctx.IDENTIFIER(1).getText())
			for member in struct.parent.member_functions:
				member.member = struct
				member.origin = "Inherited"
				struct.member_functions.append(member)
				self.scope_tracker.declareFunction(member)
				self.addSymbolToTable(member)

			for member in struct.parent.member_variables:
				member.member = struct
				struct.member_variables.append(member)
				self.scope_tracker.declareVariable(member)
				self.addSymbolToTable(member)

			struct.initialzer = struct.parent.initializer

			struct.parent = self.scope_tracker.lookupClass(ctx.IDENTIFIER(1).getText())

		self.debug << NL() << f"Declaring Class [{struct.ID}]"

		members: List[Container[Function]] = self.visit(ctx.classBody())
		for member in members:
			for function in struct.member_functions:
				if member.data.ID == function.ID:
					struct.member_functions.remove(function)
					self.removeSymbolFromTable(function)
					member.data.origin = "Override"
					self.updateSymbolFromTable(member.data)
			struct.member_functions.append(member.data)
#
		self.scope_tracker.exitScope()
		self.scope_tracker.declareClass(struct)
		self.addSymbolToTable(struct)
#
		self.current_class = None
		self.exit("Class Declaration")
		return Container(struct, Type.CLASS)

	def visitClassBody(self, ctx:CompiscriptParser.ClassBodyContext):
		self.enter("Class Body")
		members: List[Container] = []
		for i in range(len(ctx.classMember())):
			member = self.visit(ctx.classMember(i))
			members.append(member)
		self.exit("Class Body")
		return members

	def visitClassMember(self, ctx:CompiscriptParser.ClassMemberContext):
		self.enter("Member Declaration")
		self.scope_tracker.enterScope()

		if ctx.function():
			function: Container = self.visit(ctx.function())
			self.exit("Member Declaration")
			self.scope_tracker.exitScope()
			return function

	def visitForStmt(self, ctx:CompiscriptParser.ForStmtContext):
		self.enter("For Statement")
		self.scope_tracker.enterScope()

		if ctx.varDecl():
			self.visit(ctx.varDecl())
		elif ctx.exprStmt():
			self.visit(ctx.exprStmt())

		expression = ctx.expression(0)
		if expression:
			expression: Container = self.visit(expression)
			if not isinstance(expression, Container) or not expression.type == Type.BOOL:
				error(self.debug, f"Error For. Condition is not boolean. {expression.data}")

		if ctx.expression(1):
			self.visit(ctx.expression(1))

		children: Container = self.visit(ctx.statement())

		self.scope_tracker.exitScope()
		self.exit("For Statement")
		return children

	def visitIfStmt(self, ctx:CompiscriptParser.IfStmtContext):
		self.enter("If Statement")

		expression: Container = self.visit(ctx.expression())
		
		if not isinstance(expression, Container) or not expression.type == Type.BOOL:
			error(self.debug, f"Error If. IF Condition is not boolean. {expression.data}")
		self.visit(ctx.statement(0))

		if ctx.statement(1):
			return self.visit(ctx.statement(1))

		self.exit("If Statement")
		return None

	def visitReturnStmt(self, ctx:CompiscriptParser.ReturnStmtContext):
		if ctx.expression():
			return self.visit(ctx.expression())
		return Container(None, Type.VOID)

	def visitWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext):
		self.enter("While Statement")
		self.scope_tracker.enterScope()

		expression = self.visit(ctx.expression())
		if not isinstance(expression, Container) or not expression.type == Type.BOOL:
			error(self.debug, f"Error While. Condition is not boolean. {expression.data}")
		children = self.visit(ctx.statement())

		self.scope_tracker.exitScope()
		self.exit("While Statement")
		return children

	def visitBlock(self, ctx:CompiscriptParser.BlockContext):
		self.enter("Block")

		self.scope_tracker.enterScope()
		children = self.visitChildren(ctx)
		self.scope_tracker.exitScope()

		self.exit("Block")
		return children

	def visitExpression(self, ctx: CompiscriptParser.ExpressionContext):
		self.enterFull("Expression")

		if ctx.getChildCount() == 1:
			return self.visit(ctx.getChild(0))

		left: Container = self.visit(ctx.getChild(0))
		operator = ctx.getChild(1).getText()
		right: Container = self.visit(ctx.getChild(2))

		if left is None or right is None:
			error(self.debug, f"Error Expression. Evaluating Expression: None Arguments. [{left}] {operator} [{right}]")

		operation_type = operationType(self.debug, left, operator, right)

		self.exitFull("Expression")

		return Container(f"({left.innermostCode()} {operator} {right.innermostCode()})", operation_type)

	def visitAssignment(self, ctx:CompiscriptParser.AssignmentContext):
		"""Assign Code to a Variable"""
		self.enterFull("Assignment")

		if ctx.logic_or():
			self.visit(ctx.logic_or())

		if ctx.call():
			if ctx.call().getText() == "this":
				if self.current_class:
					memeber_var_name = ctx.IDENTIFIER().getText()
					if self.current_class:
						self.debug << NL() << f"Declaring Member Variable  [{memeber_var_name}]"
						variable = Variable()
						variable.ctx = ctx
						variable.ID = memeber_var_name
						variable.member = self.current_class

						assignment: Container = self.visit(ctx.assignment())
						if assignment.type == Type.PARAMETER:
							variable.data = assignment.data.ID
							variable.type = assignment.type
						else:
							variable.data = assignment.data
							variable.type = assignment.type

						for member in self.current_class.member_variables:
							if member.ID == variable.ID:
								self.current_class.member_variables.remove(member)
								self.removeSymbolFromTable(member)
								variable.origin = "Override"

						self.current_class.member_variables.append(variable)
						self.scope_tracker.declareVariable(variable)
						self.addSymbolToTable(variable)
					else:
						error(self.debug, "NOT IMPLEMENTED")
				else:
					error(self.debug, "Error Assignment. There is no parent to define a variable member to.")
			else:
				instance: Container[Variable] = self.visit(ctx.call())
				if instance.type == Type.INSTANCE:
					if instance.data.data.checkVariable(ctx.IDENTIFIER().getText()):
						code = self.visit(ctx.assignment()) # TODO
						var = instance.data.data.lookupVariable(ctx.IDENTIFIER().getText())
						var.data = code
						self.updateSymbolFromTable(var)
					else:
						error(self.debug, f"Error Assignment. {instance.data.data.ID}.{ctx.IDENTIFIER().getText()} is not defined")

		if ctx.call() is None and ctx.IDENTIFIER():
			var_name = str(ctx.IDENTIFIER())
			self.debug << NL() << "Assigning Value to [" << var_name << "]"

			if ctx.assignment():
				code = self.visit(ctx.assignment())
			elif ctx.logic_or():
				code = self.visit(ctx.logic_or())

			if self.scope_tracker.checkVariable(var_name, None):
				var = self.scope_tracker.lookupVariable(var_name, None)
				var.data = code
				self.updateSymbolFromTable(var)
			else:
				error(self.debug, f"Error Assignment. Cannot assign value to an undeclared variable {var_name}")
 
		self.exitFull("Assignment")
		return self.visitChildren(ctx)

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		self.enterFull("Or")

		left: Container = self.visit(ctx.logic_and(0))
		for i in range(1, len(ctx.logic_and())):
			right: Container = self.visit(ctx.logic_and(i))
			return Container(f"({left.data} or {right.data})", Type.BOOL)

		self.exitFull("Or")
		return self.visitChildren(ctx)

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		self.enterFull("And")

		left: Container = self.visit(ctx.equality(0))
		for i in range(1, len(ctx.equality())):
			right: Container = self.visit(ctx.equality(i))
			return Container(f"({left.data} and {right.data})", Type.BOOL)

		self.exitFull("And")
		return self.visitChildren(ctx)

	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		self.enterFull("Equality")

		if ctx.getChildCount() == 1:
			value: Container = self.visit(ctx.comparison(0))
			self.exitFull("Equality")
			return value

		left: Container = self.visit(ctx.comparison(0))
		for i in range(1, len(ctx.comparison())):
			operator = ctx.getChild(2 * i - 1).getText()
			right: Container = self.visit(ctx.comparison(i))
			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Equality. {type(left)}({left}) {operator} {type(right)}({right})")
			comparisonCheck(self.debug, left, operator, right)
			self.exitFull("Equality")
			return Container(f"({left.data} {operator} {right.data})", Type.BOOL)

	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		self.enterFull("Comparison")

		if ctx.getChildCount() == 1:
			value: Container = self.visit(ctx.term(0))
			self.exitFull("Comparison")
			return value

		left: Container = self.visit(ctx.term(0))
		for i in range(1, len(ctx.term())):
			operator: str = ctx.getChild(2 * i - 1).getText()
			right: Container = self.visit(ctx.term(i))
			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Comparison. {type(left)}({left}) {operator.replace('<', 'less').replace('>', 'greater')} {type(right)}({right})")
			comparisonCheck(self.debug, left, operator, right)
			self.exitFull("Comparison")
			return Container(f"({left.innermostCode()} {operator} {right.innermostCode()})", Type.BOOL)

	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		self.enterFull("Term")

		left : Container = self.visit(ctx.factor(0))
		for i in range(1, len(ctx.factor())):
			right : Container = self.visit(ctx.factor(i))
			operator: str = ctx.getChild(2 * i - 1).getText()

			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Term. Evaluating Expression: Unkwown Arguments. {type(left)}[{left}] {operator} {type(right)}[{right}]")

			operation_type = operationType(self.debug, left, operator, right)

			self.exitFull("Term")

			return Container(f"({left.innermostCode()} {operator} {right.innermostCode()})", operation_type)

		return left

	def visitFactor(self, ctx:CompiscriptParser.FactorContext):
		self.enterFull("Factor")

		left : Container = self.visit(ctx.unary(0))
		for i in range(1, len(ctx.unary())):
			right : Container = self.visit(ctx.unary(i))
			operator: str = ctx.getChild(2 * i - 1).getText()

			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Factor. Evaluating Expression: Unkwown Arguments. {type(left)}[{left}] {operator} {type(right)}[{right}]")

			operation_type = operationType(self.debug, left, operator, right)

			self.exitFull("Factor")

			return Container(f"({left.innermostCode()} {operator} {right.innermostCode()})", operation_type)

		return left

	def visitArray(self, ctx:CompiscriptParser.ArrayContext):
		self.enterFull("Array")
		elements: List[Container] = []
		if ctx.expression():
			for expr in ctx.expression():
				elements.append(self.visit(expr))
		self.exitFull("Array")
		return Container(elements, Type.ARRAY)

	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
		self.enterFull("Instantiation")

		class_name = ctx.IDENTIFIER().getText()
		struct = self.scope_tracker.lookupClass(class_name)

		args = []
		if ctx.arguments():
			args = self.visit(ctx.arguments())

		if struct.initializer:
			if len(args) != len(struct.initializer.parameters):
				error(self.debug, f"Error Intantiation. Tried to Instantiate '{class_name}' with {len(args)} parameters. Expected {len(struct.initializer.parameters)}")
		elif len(args) != 0:
			error(self.debug, f"Error Intantiation. Tried to Instantiate '{class_name}' with {len(args)} parameters. Expected NONE")

		self.exitFull("Instantiation")
		return Container(self.scope_tracker.lookupClass(class_name), Type.CLASS)

	def visitUnary(self, ctx:CompiscriptParser.UnaryContext):
		self.enterFull("Unary")

		if ctx.getChildCount() == 2:
			operator = ctx.getChild(0).getText()
			operand: Container = self.visit(ctx.unary())
			if operator == '-':
				if operand.type == Type.INT or operand.type == Type.FLOAT:
					self.exitFull("Unary")
					return Container(f"-{operand.data}", operand.type)
				error(self.debug, f"Error Unary. Applying operator {operator} to <{operand.type}>({operand.data})")
			elif operator == '!':
				if operand.type == Type.BOOL:
					self.exitFull("Unary")
					return Container(f"!{operand.data}", operand.type)
				error(self.debug, f"Error Unary. Applying {operator} to <{operand.type}>({operand.data})")
		else:
			visited: Container = self.visit(ctx.call())
			self.exitFull("Unary")
			return visited

	def visitCall(self, ctx:CompiscriptParser.CallContext):
		self.enterFull("Call")

		if ctx.getChildCount() == 1:
			if ctx.primary():
				visited = self.visit(ctx.primary())
				return visited

		elif ctx.primary():
			primary: Container = self.visit(ctx.primary())
			if primary.type == Type.FUNCTION:
				if (self.current_function and self.current_function.ID != primary.data.ID )or (self.current_call and self.current_call != primary.data.ID):
					self.current_call = primary.data.ID
					call_params = []
					if ctx.arguments() and len(ctx.arguments()) > 0:
						arguments: CompiscriptParser.ArgumentsContext = ctx.arguments(0)
						for i in range(0, arguments.getChildCount(), 2):
							call_params.append(self.visit(arguments.getChild(i)))
					elif len(self.current_function.parameters) != len(call_params):
						error(self.debug, f"Error Call. Tried to call Function '{self.current_function.ID}' with {len(call_params)} parameters. Expected {len(self.current_function.parameters)}")
					if self.current_function.parameters:
						self.current_call = None
				elif (self.current_function and self.current_function.ID == primary.data.ID) or (self.current_call and self.current_call == primary.data.ID):
					if self.current_function:
						self.current_function.recursive = True
						self.updateSymbolFromTable(self.current_function)
				else:
					call_params = []
					if ctx.arguments() and len(ctx.arguments()) > 0:
						arguments: CompiscriptParser.ArgumentsContext = ctx.arguments(0)
						for i in range(0, arguments.getChildCount(), 2):
							call_params.append(self.visit(arguments.getChild(i)))
					elif len(primary.data.parameters) != len(call_params):
						error(self.debug, f"Error Call. Tried to call Function '{primary.data.ID}' with {len(call_params)} parameters. Expected {len(primary.data.parameters)}")

			elif primary.type == Type.THIS: # Accesing a variable from self
				if self.current_class is None:
					error(self.debug, "Error Call. Calling this outside of class")
				elif self.current_class:
					var_name = ctx.IDENTIFIER(0).getText()
					if self.current_class.lookupVariable(var_name):
						return Container(self.current_class.lookupVariable(var_name), Type.VARIABLE)
					error(self.debug, f"Error Call. Trying to acces undefined variable {self.current_class.ID}.{var_name}")
			elif primary.type == Type.INSTANCE:
				child_count = ctx.getChildCount()
				# Verify if there is a nested call or variable
				if child_count > 3:  # Checks if there are more elements indicating a chain
					current_instance: Class | Variable | Function = primary.data.data  # Start with the first instance
					for i in range(2, child_count, 2):  # Iterate over each chained element (assuming format: instance '.' member)
						member_name = ctx.getChild(i).getText()  # Extract member name
						if isinstance(current_instance, Variable):
							return Container(current_instance, Type.VARIABLE)
						
						if i + 1 < child_count and ctx.getChild(i + 1).getText() == '(':  # It's a function call
							function = self.scope_tracker.lookupFunction(member_name, current_instance)
							call_params = []
							if ctx.arguments() and len(ctx.arguments()) > 0:
								arguments: CompiscriptParser.ArgumentsContext = ctx.arguments(0)
								for j in range(0, arguments.getChildCount(), 2):
									call_params.append(self.visit(arguments.getChild(j)))
							
							# Check if the parameters match the function definition
							if len(function.parameters) != len(call_params):
								error(self.debug, f"Error Call. Tried to call Function '{function.ID}' with {len(call_params)} parameters. Expected {len(function.parameters)}")
							
							# Move to the next instance for further chained calls, if any
							if function.return_type == Type.VOID:
								break
							current_instance = function.return_type  # Update the current instance to function's return type
						else:  # It's a variable access
							variable = self.scope_tracker.lookupVariable(member_name, current_instance)
							current_instance = variable  # Update current instance to variable's type

					return Container(current_instance, Type.INSTANCE)
				
				else:  # Single function call or variable access
					member_name = ctx.IDENTIFIER(0).getText()
					if ctx.getChild(2).getText() == '(':  # Function call
						function = self.scope_tracker.lookupFunction(member_name, primary.data.data)
						call_params = []
						if ctx.arguments() and len(ctx.arguments()) > 0:
							arguments: CompiscriptParser.ArgumentsContext = ctx.arguments(0)
							for i in range(0, arguments.getChildCount(), 2):
								call_params.append(self.visit(arguments.getChild(i)))
						if len(function.parameters) != len(call_params):
							error(self.debug, f"Error Call. Tried to call Function '{function.ID}' with {len(call_params)} parameters. Expected {len(function.parameters)}")
						self.current_call = None
						return function  # Return the called function
					else:  # Variable access
						return Container(self.scope_tracker.lookupVariable(member_name, primary.data.data), Type.VARIABLE)
			
			elif primary.type == Type.SUPER:
				if not self.current_class:
					error(self.debug, "Calling super outside of Class")
				if not self.current_class.parent.initializer:
					error(self.debug, f"Calling super in a Class {self.current_class} whose parent class {self.current_class.parent} does not have a init() method.")
				call_params = []
				if ctx.arguments() and len(ctx.arguments()) > 0:
					arguments: CompiscriptParser.ArgumentsContext = ctx.arguments(0)
					for i in range(0, arguments.getChildCount(), 2):
						call_params.append(self.visit(arguments.getChild(i)))
				if len(self.current_class.parent.initializer.parameters) != len(call_params):
					error(self.debug, f"Error Call. Tried to call Super Function '{self.current_function.ID}' with {len(call_params)} parameters. Expected {len(self.current_class.parent.initializer.parameters)}")

		self.exitFull("Call")

		visited: Container = self.visitChildren(ctx)
		return visited

	def visitSuperCall(self, ctx: CompiscriptParser.SuperCallContext):
		self.enterFull("Super")

		if not ctx.IDENTIFIER():
			error(self.debug, "Error Super. Empy super call")
		if not self.current_class:
			error(self.debug, "Error Super. Calling super outside of class")
		if not self.current_class.parent:
			error(self.debug, "Error Super. Calling super in a class with no parent")

		member_name: str = ctx.IDENTIFIER().getText()
		if self.current_class.parent.checkFunction(member_name):
			self.exitFull("Super")
			return Container(self.current_class.lookupFunction(member_name), Type.SUPER)
		else:
			error(self.debug, f"Error Super. No function in hierarchy named '{member_name}'")


	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
		#self.enterFull("Primary")

		if ctx.NUMBER():
			text = str(ctx.NUMBER())
			if '.' in text:
				return Container(text, Type.FLOAT)
			else:
				return Container(text, Type.INT)
		elif ctx.STRING():
			text = str(ctx.STRING()).strip('"')
			return Container(text, Type.STRING)
		elif ctx.IDENTIFIER():
			ID = ctx.IDENTIFIER().getText()
			if self.scope_tracker.checkVariable(ID, self.current_class):
				variable = self.scope_tracker.lookupVariable(ID, self.current_class)
				type = Type.INSTANCE if variable.type == Type.CLASS else Type.VARIABLE
				return Container(variable, type)
			if self.scope_tracker.checkFunction(ID, self.current_class):
				function = self.scope_tracker.lookupFunction(ID, self.current_class)
				return Container(function, Type.FUNCTION)
			if self.current_function:
				return Container(self.current_function.lookupParameter(ID), Type.PARAMETER)

			error(self.debug, f"Error Primary. Variable '{ID}' not defined")

		elif ctx.array():
			return self.visit(ctx.array())
		elif ctx.instantiation():
			return self.visit(ctx.instantiation())
		elif ctx.expression():
			return self.visit(ctx.expression())
		elif ctx.superCall():
			return self.visit(ctx.superCall())

		elif ctx.getText() == "true":
			return Container("true", Type.BOOL)
		elif ctx.getText() == "false":
			return Container("false", Type.BOOL)
		elif ctx.getText() == "nil":
			return Container("nil", Type.NONE)
		elif ctx.getText() == "this":
			return Container("this", Type.THIS)
		elif ctx.superCall():
			return Container(ctx.superCall().getChild(2).getText(), Type.SUPER)
		
		visited = self.visitChildren(ctx)
		return visited

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		"""Assign Function Member to Class or create Function"""
		self.enter("Function")
		self.scope_tracker.enterScope()

		function = Function()
		function.ctx = ctx
		function.ID = ctx.IDENTIFIER().getText()
		function.data = ctx.block().getText()
		self.current_function = function

		self.debug << NL() << f"Declaring Function [{function.ID}]"

		if ctx.parameters():
			for param in ctx.parameters().IDENTIFIER():
				parameter = Function_Parameter()
				parameter.ID = param.getText()
				parameter.function = function
				function.parameters.append(parameter)

		if self.current_class:
			function.member = self.current_class
			#TODO if function.ID == "init"
			#TODO this. variables
			if function.ID == "init":
				self.current_class.initializer = function

		self.visitChildren(ctx)
#
		self.scope_tracker.exitScope()
		self.scope_tracker.declareFunction(function)
		self.addSymbolToTable(function)
		self.current_function = None
#
		self.exit("Function")
		return Container(function, Type.FUNCTION)

	def visitVariable(self, ctx:CompiscriptParser.VariableContext):
		"""Assign Variable Member to Class or create Variable"""
		self.enter("Variable")
#
		variable = Variable()
		variable.ctx = ctx
		variable.ID = ctx.IDENTIFIER().getText()
		variable.data = ctx.getText()
#
		if self.current_class:
			variable.member = self.current_class
#
		if ctx.expression():
			var: Container = self.visit(ctx.expression())
			variable.data = var.data
			variable.type = var.type

		self.debug << NL() << f"Declaring Variable [{variable.ID}]"
#
		self.scope_tracker.declareVariable(variable)
		self.addSymbolToTable(variable)
#
		self.exit("Variable")

		return Container(variable, Type.INSTANCE if variable.type == Type.CLASS else Type.VARIABLE)

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

	def enterFull(self, type: str):
		if FULL_VIEW:
			self.debug << NL() << "ENTER " + type
			self.debug += 1

	def exitFull(self, type: str):
		if FULL_VIEW:
			self.debug -= 1
			self.debug << NL() << "EXIT  " + type

	def enter(self, type: str):
		self.debug << NL() << "ENTER " + type
		self.debug += 1

	def exit(self, type: str):
		self.debug -= 1
		self.debug << NL() << "EXIT  " + type

	def nodeTree(self, ctx: ParserRuleContext):
		node_id = f"node{self.count}"
		self.count += 1

		if isinstance(ctx, ParserRuleContext):
			rule_name = self.parser.ruleNames[ctx.getRuleIndex()]
			label = f"{rule_name}: {ctx.getText()}"
		else:
			label = f"Terminal: {ctx.getText()}"

		self.graph.node(node_id, label)

		for i in range(ctx.getChildCount()):
			child = ctx.getChild(i)
			child_id = self.nodeTree(child)
			self.graph.edge(node_id, child_id)

		return node_id