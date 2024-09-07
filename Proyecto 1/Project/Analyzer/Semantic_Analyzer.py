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

		self.anonymous_counter : int = 0
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

	def visitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
		self.enter("Class Declaration")
		self.scope_tracker.enterScope()

		struct = Class()
		struct.ctx = ctx
		struct.ID = str(ctx.IDENTIFIER(0))
		self.current_class = struct

		self.debug << NL() << f"Declaring Class [{struct.ID}]"

		members: Container[List[Container]] = self.visit(ctx.classBody())
		for member in members.data:
			struct.member_functions.append(member)
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
		return Container(members, Type.ARRAY)

	def visitClassMember(self, ctx:CompiscriptParser.ClassMemberContext):
		self.enter("Member Declaration")
		self.scope_tracker.enterScope()

		if ctx.function():
			function: Container = self.visit(ctx.function())
			self.exit("Member Declaration")
			self.scope_tracker.exitScope()
			return function

	def visitFunDecl(self, ctx:CompiscriptParser.FunDeclContext):
		return self.visitChildren(ctx)

	def visitVarDecl(self, ctx:CompiscriptParser.VarDeclContext):
		return self.visitChildren(ctx)

	def visitStatement(self, ctx:CompiscriptParser.StatementContext):
		return self.visitChildren(ctx)

	def visitExprStmt(self, ctx:CompiscriptParser.ExprStmtContext):
		return self.visitChildren(ctx)

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

		self.scope_tracker.enterScope()
		children = self.visitChildren(ctx)
		self.scope_tracker.exitScope()

		self.exit("If Statement")
		return children

	def visitPrintStmt(self, ctx:CompiscriptParser.PrintStmtContext):
		return self.visitChildren(ctx)

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

	def visitFunAnon(self, ctx:CompiscriptParser.FunAnonContext):
		return self.visitChildren(ctx)

	def visitExpression(self, ctx: CompiscriptParser.ExpressionContext):
		self.enterFull("Expression")

		if ctx.getChildCount() == 1:
			return self.visit(ctx.getChild(0))

		left = self.visit(ctx.getChild(0))
		operator = ctx.getChild(1).getText()
		right = self.visit(ctx.getChild(2))

		# Si alguno de los operandos es None, algo salió mal en el procesamiento anterior
		if left is None or right is None:
			error(self.debug, f"Error Expression. Evaluating Expression: None Arguments. [{left}] {operator} [{right}]")

		if operator == '+':
			return left + right
		elif operator == '-':
			return left - right
		elif operator == '*':
			return left * right
		elif operator == '/':
			return left / right
		elif operator == '%':
			return left % right
		# Si el operador no es reconocido, lanza una excepción
		
		else:
			error(self.debug, f"Error Expression. Evaluating Expression: Unknown Operator. [{left}] {operator} [{right}]")

		self.exitFull("Expression")

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

						self.current_class.member_variables.append(variable)
						self.scope_tracker.declareVariable(variable, self.current_variable)
						self.addSymbolToTable(variable)
					else:
						self.debug << NL() << f"Assigning to Member Variable  [{memeber_var_name}]"
						print(f"ASSIGN THIS  {self.current_class}")
						error(self.debug, "ASSIGN THIS NOT IMPLEMENTED")
						#variable = Variable()
						#variable.ctx = ctx
						#variable.ID = memeber_var_name
						#variable.member = self.current_class
						#variable.data = self.visit(ctx.assignment())
#
						#self.scope_tracker.declareVariable(variable, self.current_class)

				else:
					error(self.debug, "Error Assignment. There is no parent to define a variable member to.")
			else:
				instance: Container[Variable] = self.visit(ctx.call())
				if instance.type == Type.INSTANCE:
					if self.scope_tracker.checkVariable(ctx.IDENTIFIER().getText(), instance.data.data):
						code = self.visit(ctx.assignment())
						self.scope_tracker.lookupVariable(ctx.IDENTIFIER().getText(), instance.data.data).data = code
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
				self.scope_tracker.lookupVariable(var_name, None).data = code
			else:
				error(self.debug, f"Error Assignment. Cannot assign value to an undeclared variable {var_name}")
 
		self.exitFull("Assignment")
		return self.visitChildren(ctx)

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		self.enterFull("Or")

		left: Container = self.visit(ctx.logic_and(0))
		for i in range(1, len(ctx.logic_and())):
			right: Container = self.visit(ctx.logic_and(i))
			return Container(f"{left.data} or {right.data}", Type.BOOL)

		self.exitFull("Or")
		return self.visitChildren(ctx)

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		self.enterFull("And")

		left: Container = self.visit(ctx.equality(0))
		for i in range(1, len(ctx.equality())):
			right: Container = self.visit(ctx.equality(i))
			return Container(f"{left.data} and {right.data}", Type.BOOL)

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
			self.exitFull("Equality")
			return Container(f"{left.data} {operator} {right.data}", Type.BOOL)

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
			self.exitFull("Comparison")
			return Container(f"{left.data} {operator} {right.data}", Type.BOOL)

	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		self.enterFull("Term")

		left  : Container = self.visit(ctx.factor(0))
		for i in range(1, len(ctx.factor())):
			right : Container = self.visit(ctx.factor(i))
			operator: str = ctx.getChild(2 * i - 1).getText()

			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Term. Evaluating Expression: Unkwown Arguments. {type(left)}[{left}] {operator} {type(right)}[{right}]")

			operation_type = operationType(self.debug, left, operator, right)

			self.exitFull("Term")

			if operator == '+':
				return Container(f"({left.data} + {right.data})", operation_type)
			elif operator == '-':
				return Container(f"({left.data} - {right.data})", operation_type)

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

			return Container(f"({left.data} {operator} {right.data})", operation_type)

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

		args = []
		if ctx.arguments():
			args = self.visit(ctx.arguments())
		
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
				error(self.debug, f"Error Applying Unary operator {operator} to <{operand.type}>({operand.data})")
			elif operator == '!':
				if operand.type == Type.BOOL:
					self.exitFull("Unary")
					return Container(f"!{operand.data}", operand.type)
				error(self.debug, f"Error Applying Unary operator {operator} to <{operand.type}>({operand.data})")
		else:
			visited: Container = self.visit(ctx.call())
			self.exitFull("Unary")
			return visited

	def visitCall(self, ctx:CompiscriptParser.CallContext):
		self.enterFull("Call")

		if ctx.getChildCount() == 1:
			if ctx.primary():
				return self.visit(ctx.primary())

		elif ctx.primary():
			primary: Container = self.visit(ctx.primary())
			if primary.type == Type.FUNCTION:
				if self.current_function.ID != primary.data.ID or self.current_call != primary.data.ID:
					self.current_call = primary.data.ID
					call_params = []
					if ctx.arguments() and len(ctx.arguments()) > 0:
						arguments: CompiscriptParser.ArgumentsContext = ctx.arguments(0)
						for i in range(0, arguments.getChildCount(), 2):
							call_params.append(self.visit(arguments.getChild(i)))
					if self.current_function.parameters and len(self.current_function.parameters) != len(call_params):
						error(self.debug, f"Error Call. Tried to call Function '{self.current_function.ID}' with {len(call_params)} parameters. Expected {len(self.current_function.parameters)}")
					if self.current_function.parameters:
						self.current_call = None

				elif self.current_function.ID == primary.ID or self.current_call == primary.ID:
					if self.current_function:
						self.current_function.recursive = True
					return Container(None, Type.PARAMETER)
			elif primary.type == Type.THIS: # Accesing a variable from self
				if self.current_class is None:
					error(self.debug, "Error Call. Calling this outside of class")
				elif self.current_class:
					var_name = ctx.IDENTIFIER(0).getText()
					if self.current_class.lookupVariable(var_name):
						return Container(self.current_class.lookupVariable(var_name), Type.VARIABLE)
					error(self.debug, f"Error Call. Trying to acces undefined variable {self.current_class.ID}.{var_name}")
			elif primary.type == Type.INSTANCE:
				if ctx.getChildCount() > 3: # is calling a function of an instance
					return primary
				else: # is calling a variable of an instance
					return primary



		self.exitFull("Call")
		return self.visitChildren(ctx)

	def visitSuperCall(self, ctx: CompiscriptParser.SuperCallContext):
		self.enterFull("Super")

		if not ctx.IDENTIFIER():
			error(self.debug, "Error Super. Empy super call")
		elif not self.current_class:
			error(self.debug, "Error Super. calling super outside of class")
		else:
			ctx.IDENTIFIER().getText()

		self.exitFull("Super")
		return self.visitChildren(ctx)

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
			var_name = ctx.IDENTIFIER().getText()
			if self.current_function:
				if self.current_function.checkParameter(var_name):
					return Container(self.current_function.lookupParameter(var_name), Type.PARAMETER)
				error(self.debug, f"Error Primary. Parameter '{var_name}' not defined.")
			else:
				if self.scope_tracker.checkVariable(var_name, self.current_class):
					variable = self.scope_tracker.lookupVariable(var_name, self.current_class)
					type = Type.INSTANCE if variable.type == Type.CLASS else Type.VARIABLE
					return Container(variable, type)
				else:
					error(self.debug, f"Error Primary. Variable '{var_name}' out of scope.")

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
		
		return self.visitChildren(ctx)

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		"""Assign Function Member to Class or create Function"""
		self.enter("Function")
		self.scope_tracker.enterScope()

		function = Function()
		function.ctx = ctx
		function.ID = ctx.IDENTIFIER().getText()
		self.current_function = function

		self.debug << NL() << f"Declaring Function [{function.ID}]"

		if ctx.parameters():
			for param in ctx.parameters().IDENTIFIER():
				parameter = Function_Parameter()
				parameter.ID = param.getText()
				parameter.function = function
				function.parameters.append(parameter)

		if self.current_class:
			function.member = self.current_class.ID
			#TODO if function.ID == "init"
			#TODO this. variables
			if function.ID == "init":
				self.current_class.initializer = function

		self.visitChildren(ctx)
#
		self.scope_tracker.exitScope()
		self.scope_tracker.declareFunction(function, self.current_class)
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
		self.scope_tracker.declareVariable(variable, None)
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

	def addSymbolToTable(self, value: Union[Class | Function | Variable]):
		if isinstance(value, Class):
			self.table_c.addSymbol(value)
		elif isinstance(value, Function):
			self.table_f.addSymbol(value)
		elif isinstance(value, Variable):
			self.table_v.addSymbol(value)

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

	def nodeTree(self, ctx: Union[ParserRuleContext]):
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