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

		self.struct_scope: Class = None

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
		struct.ID = str(ctx.IDENTIFIER(0))

		self.debug << NL() << f"Class [{struct.ID}]"

		members: Container = self.visit(ctx.classBody())
		for member in members.data:
			if member.type == Type.FUNCTION:
				struct.member_functions.append(member)
			elif member.type == Type.VARIABLE:
				struct.member_variables.append(member)
			else:
				print(member)
#
		self.scope_tracker.exitScope()
		self.scope_tracker.declareClass(struct)
		self.addSymbolToTable(struct)
#
		self.struct_scope = None
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

		if ctx.variable():
			variable: Container = self.visit(ctx.variable(), member = True)
			self.exit("Member Declaration")
			return variable

		elif ctx.function():
			function: Container = self.visit(ctx.function())
			self.exit("Member Declaration")
			return function

	def visitFunDecl(self, ctx:CompiscriptParser.FunDeclContext):
		self.enter("Function Declaration")

		function: Container = self.visit(ctx.function())

		self.exit("Function Declaration")
		return function

	def visitVarDecl(self, ctx:CompiscriptParser.VarDeclContext):
		self.enter("Variable Declaration")

		variable: Container = self.visit(ctx.variable())

		self.exit("Variable Declaration")
		return variable

	def visitStatement(self, ctx:CompiscriptParser.StatementContext):
		return self.visitChildren(ctx)

	def visitExprStmt(self, ctx:CompiscriptParser.ExprStmtContext):
		return self.visitChildren(ctx)

	def visitForStmt(self, ctx:CompiscriptParser.ForStmtContext):
		self.enter("For Statement")

		self.scope_tracker.enterScope()
		children = self.visitChildren(ctx)
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
		return self.visitChildren(ctx)

	def visitWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext):
		self.enter("While Statement")

		self.scope_tracker.enterScope()
		children = self.visitChildren(ctx)
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

	def visitExpression(self, ctx:CompiscriptParser.ExpressionContext):
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
		self.enter("Assignment")

		if ctx.getChildCount() == 1:
			return self.visit(ctx.logic_or())

		if ctx.call():
			if ctx.IDENTIFIER():
				var_name = str(ctx.IDENTIFIER())
				self.debug << NL() << "Assigning Value to Class Member [" << var_name << "]"

				if isinstance(self.struct_scope, Class):
					if self.struct_scope.checkVariable(var_name, self.struct_scope):
						variable: Variable = self.struct_scope.lookupVariable(var_name, self.struct_scope)
						variable.member = self.struct_scope.ID
						variable.code = self.visit(ctx.assignment())
						variable.class_type = self.struct_scope
						return variable.code

					else:
						variable = Variable()
						variable.ID = var_name
						variable.member = self.struct_scope.ID
						variable.code = self.visit(ctx.assignment())
						variable.class_type = self.struct_scope

						self.struct_scope.member_variables.append(variable)
						self.scope_tracker.declareVariable(variable, self.struct_scope)
						return variable.code
		else:
			if ctx.IDENTIFIER():
				var_name = str(ctx.IDENTIFIER())
				self.debug << NL() << "Assigning Value to [" << var_name << "]"

				if ctx.assignment():
					code = self.visit(ctx.assignment())
				elif ctx.logic_or() is not None:
					code = self.visit(ctx.logic_or())
				self.scope_tracker.lookupVariable(var_name, None).code = code
				return code
 
		self.exit("Assignment")

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		self.enterFull("Or")

		left: Container = self.visit(ctx.logic_and(0))
		for i in range(1, len(ctx.logic_and())):
			right: Container = self.visit(ctx.logic_and(i))
			return Container(f"{left.getCode()} or {right.getCode()}", Type.BOOL)

		self.exitFull("Or")
		return self.visitChildren(ctx)

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		self.enterFull("And")

		left: Container = self.visit(ctx.equality(0))
		for i in range(1, len(ctx.equality())):
			right: Container = self.visit(ctx.equality(i))
			return Container(f"{left.getCode()} and {right.getCode()}", Type.BOOL)

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
				error(self.debug, f"Error Comparison. {left} {operator} {right}")
			self.exitFull("Equality")
			return Container(f"{left.getCode()} {operator} {right.getCode()}", Type.BOOL)

	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		self.enterFull("Comparison")

		if ctx.getChildCount() == 1:
			value: Container = self.visit(ctx.term(0))
			self.exitFull("Comparison")
			return value

		left: Container = self.visit(ctx.term(0))
		for i in range(1, len(ctx.term())):
			operator = ctx.getChild(2 * i - 1).getText()
			right: Container = self.visit(ctx.term(i))
			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Comparison. {left} {operator} {right}")
			self.exitFull("Comparison")
			return Container(f"{left.getCode()} {operator} {right.getCode()}", Type.BOOL)

	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		self.enterFull("Term")

		left  : Container = self.visit(ctx.factor(0))
		for i in range(1, len(ctx.factor())):
			right : Container = self.visit(ctx.factor(i))
			operator: str = ctx.getChild(2 * i - 1).getText()

			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Term. Evaluating Expression: None Arguments. [{left}] {operator} [{right}]")

			type = operationType(self.debug, left, operator, right)

			self.exitFull("Term")

			if operator == '+':
				return Container(f"({left.getCode()} + {right.getCode()})", type)
			elif operator == '-':
				return Container(f"({left.getCode()} - {right.getCode()})", type)

		return left

	def visitFactor(self, ctx:CompiscriptParser.FactorContext):
		self.enterFull("Factor")

		left : Container = self.visit(ctx.unary(0))
		for i in range(1, len(ctx.unary())):
			right : Container = self.visit(ctx.unary(i))
			operator: str = ctx.getChild(2 * i - 1).getText()

			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Factor. Evaluating Expression: None Arguments. [{left}] {operator} [{right}]")

			type = operationType(self.debug, left, operator, right)

			self.exitFull("Factor")

			if operator == '*':
				return Container(f"({left.getCode()} * {right.getCode()})", type)
			elif operator == '/':
				return Container(f"({left.getCode()} / {right.getCode()})", type)
			elif operator == '%':
				return Container(f"({left.getCode()} % {right.getCode()})", type)

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
					return Container(f"-{operand.getCode()}", operand.type)
				error(self.debug, f"Error Applying Unary operator {operator} to ⟪{operand.type}⟫({operand.getCode()})")
			elif operator == '!':
				if operand.type == Type.BOOL:
					self.exitFull("Unary")
					return Container(f"!{operand.getCode()}", operand.type)
				error(self.debug, f"Error Applying Unary operator {operator} to ⟪{operand.type}⟫({operand.getCode()})")
		else:
			visited: Container = self.visit(ctx.call())
			self.exitFull("Unary")
			return visited

	def visitCall(self, ctx:CompiscriptParser.CallContext):
		self.enterFull("Call")

		if ctx.getChildCount() > 1 and ctx.getChild(1).getText() == '.':
			instance: Container = self.visit(ctx.getChild(0))  # visit the instance (e.g., myclassinstance)
			member_variable = ctx.getChild(2).getText()   # get the member variable name (e.g., variable_a)
			
			member_name = ctx.IDENTIFIER(0)
			print(f"{member_variable}.{member_name}")

			if self.scope_tracker.checkVariable(instance, self.struct_scope):
				variable: Variable = self.scope_tracker.lookupVariable(instance, self.struct_scope)
				if self.scope_tracker.checkClass(variable.class_type, self.struct_scope):
					struct: Class = self.scope_tracker.lookupClass(variable.class_type, self.struct_scope)
					print(f"Accessing member variable '{member_variable}' of variable '{variable}' whidch instantiates '{struct}'")
		
		self.exitFull("Call")
		return self.visitChildren(ctx)

	def visitSuper(self, ctx: CompiscriptParser.SuperContext):
		return super().visitSuper(ctx)

	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
		self.enterFull("Primary")

		if ctx.NUMBER():
			text = str(ctx.NUMBER())
			self.exitFull("Primary")
			if '.' in text:
				return Container(text, Type.FLOAT)
			else:
				return Container(text, Type.INT)
		if ctx.STRING():
			text = str(ctx.STRING()).strip('"')
			self.exitFull("Primary")
			return Container(text, Type.STRING)
		if ctx.IDENTIFIER():
			var_name = str(ctx.IDENTIFIER())
			if self.scope_tracker.checkVariable(var_name, self.struct_scope):
				self.exitFull("Primary")
				return Container(self.scope_tracker.lookupVariable(var_name, self.struct_scope), Type.VARIABLE)
			else:
				error(self.debug, f"Error Primary. Variable '{var_name}' out of scope.")

		if ctx.array():
			return self.visit(ctx.array())
		if ctx.instantiation():
			return self.visit(ctx.instantiation())
		if ctx.expression():
			return self.visit(ctx.expression())
		if ctx.super_():
			return self.visit(ctx.super_())

		self.exitFull("Primary")
		if ctx.getText() == "true":
			return Container("true", Type.BOOL)
		if ctx.getText() == "false":
			return Container("false", Type.BOOL)
		if ctx.getText() == "nil":
			return Container("nil", Type.NONE)
		if ctx.getText() == "this":
			return Container("this", Type.MEMBER_POINTER)
		
		return self.visitChildren(ctx)

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		"""Assign Function Member to Class or create Function"""
		self.enter("Function")
		self.scope_tracker.enterScope()

		function = Function()
		function.ID = str(ctx.IDENTIFIER())
		if self.struct_scope:
			function.member = self.struct_scope.ID
			#TODO if function.ID == "init"
			#TODO this. variables
			if function.ID == "init":
				self.struct_scope.initializer = function
#
		self.scope_tracker.exitScope()
		self.scope_tracker.declareFunction(function, self.struct_scope)
		self.addSymbolToTable(function)
#
		self.exit("Function")
		return Container(function, Type.FUNCTION)

	def visitVariable(self, ctx:CompiscriptParser.VariableContext):
		"""Assign Variable Member to Class or create Variable"""
		self.enter("Variable")
#
		variable = Variable()
		variable.ID = ctx.IDENTIFIER().getText()
		variable.code = ctx.getText()
#
		if self.struct_scope:
			variable.member = self.struct_scope
#
		if ctx.expression():
			var: Container = self.visit(ctx.expression())
			variable.code = var.getCode()
			variable.type = var.type

		self.debug << NL() << f"Variable [{variable.ID}]"
#
		self.scope_tracker.declareVariable(variable, None)
		self.addSymbolToTable(variable)
#
		self.exit("Variable")
		return Container(variable, Type.VARIABLE)

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