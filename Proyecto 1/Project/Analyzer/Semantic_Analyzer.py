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

		self.table_c = table_c
		self.table_f = table_f
		self.table_v = table_v

	def visitProgram(self, ctx:CompiscriptParser.ProgramContext, **kwargs):
		return self.visitChildren(ctx)

	def visitDeclaration(self, ctx:CompiscriptParser.DeclarationContext, **kwargs):
		return self.visitChildren(ctx)

	def visitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext, **kwargs):
		self.enter("Class Declaration")
		self.scope_tracker.enterScope()

		struct = Class()
		struct.ID = str(ctx.IDENTIFIER(0))

		self.debug << NL() << f"Class [{struct.ID}]"

		members: Container = self.visit(ctx.classBody(), **kwargs, visiting_class = struct, struct = struct)
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
		self.exit("Class Declaration")
		return Container(struct, Type.CLASS)

	def visitClassBody(self, ctx:CompiscriptParser.ClassBodyContext, **kwargs):
		self.enter("Class Body")
		members: List[Container] = []
		for i in range(len(ctx.classMember())):
			member = self.visit(ctx.classMember(i), **kwargs)
			members.append(member)
		self.exit("Class Body")
		return Container(members, Type.ARRAY)

	def visitClassMember(self, ctx:CompiscriptParser.ClassMemberContext, **kwargs):
		self.enter("Member Declaration")
		self.scope_tracker.enterScope()

		if ctx.varDecl() is not None:
			variable: Container = self.visit(ctx.varDecl(), **kwargs)
			self.exit("Member Declaration")
			return variable

		elif ctx.function() is not None:
			function: Container = self.visit(ctx.function(), **kwargs)
			self.exit("Member Declaration")
			return function

	def visitFunDecl(self, ctx:CompiscriptParser.FunDeclContext, **kwargs):
		self.enter("Function Declaration")

		function = self.visit(ctx.function(), **kwargs)

		self.exit("Function Declaration")
		return Container(function, Type.FUNCTION)

	def visitVarDecl(self, ctx:CompiscriptParser.VarDeclContext, **kwargs):
		self.enter("Variable Declaration")
#
		variable = Variable()
		variable.ID = str(ctx.IDENTIFIER())
		variable.code = ctx.getText()
#
		if "struct" in kwargs and isinstance(kwargs["struct"], Class):
			variable.member = kwargs["visiting_class"]
#
		if ctx.expression():
			var: Container = self.visit(ctx.expression(), **kwargs)
			variable.code = var.getCode()
			variable.type = var.type

		self.debug << NL() << f"Variable [{variable.ID}]"
#
		self.scope_tracker.declareVariable(variable, None)
		self.addSymbolToTable(variable)
#
		self.exit("Variable Declaration")
		return Container(variable, Type.VARIABLE)

	def visitStatement(self, ctx:CompiscriptParser.StatementContext, **kwargs):
		return self.visitChildren(ctx)

	def visitExprStmt(self, ctx:CompiscriptParser.ExprStmtContext, **kwargs):
		return self.visitChildren(ctx)

	def visitForStmt(self, ctx:CompiscriptParser.ForStmtContext, **kwargs):
		self.enter("For Statement")

		self.scope_tracker.enterScope()
		children = self.visitChildren(ctx)
		self.scope_tracker.exitScope()
		
		self.exit("For Statement")
		return children

	def visitIfStmt(self, ctx:CompiscriptParser.IfStmtContext, **kwargs):
		self.enter("If Statement")

		self.scope_tracker.enterScope()
		children = self.visitChildren(ctx)
		self.scope_tracker.exitScope()

		self.exit("If Statement")
		return children

	def visitPrintStmt(self, ctx:CompiscriptParser.PrintStmtContext, **kwargs):
		return self.visitChildren(ctx)

	def visitReturnStmt(self, ctx:CompiscriptParser.ReturnStmtContext, **kwargs):
		return self.visitChildren(ctx)

	def visitWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext, **kwargs):
		self.enter("While Statement")

		self.scope_tracker.enterScope()
		children = self.visitChildren(ctx)
		self.scope_tracker.exitScope()

		self.exit("While Statement")
		return children

	def visitBlock(self, ctx:CompiscriptParser.BlockContext, **kwargs):
		self.enter("Block")

		self.scope_tracker.enterScope()
		children = self.visitChildren(ctx)
		self.scope_tracker.exitScope()

		self.exit("Block")
		return children

	def visitFunAnon(self, ctx:CompiscriptParser.FunAnonContext, **kwargs):
		return self.visitChildren(ctx)

	def visitExpression(self, ctx:CompiscriptParser.ExpressionContext, **kwargs):
		self.enterFull("Expression")

		if ctx.getChildCount() == 1:
			return self.visit(ctx.getChild(0), **kwargs)

		left = self.visit(ctx.getChild(0), **kwargs)
		operator = ctx.getChild(1).getText()
		right = self.visit(ctx.getChild(2), **kwargs)

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

	def visitAssignment(self, ctx:CompiscriptParser.AssignmentContext, **kwargs):
		"""Assign Code to a Variable"""
		self.enterFull("Assignment")

		if ctx.getChildCount() == 1:
			return self.visit(ctx.logic_or(), **kwargs)

		if ctx.call():
			if ctx.IDENTIFIER():
				var_name = str(ctx.IDENTIFIER())
				self.debug << NL() << "Assign Value to Class Member [" << var_name << "]"

				struct = kwargs["struct"] if "struct" in kwargs else None
				if isinstance(struct, Class):
					if struct.checkVariable(var_name, struct):
						variable: Variable = struct.lookupVariable(var_name, struct)
						variable.member = struct.ID
						variable.code = self.visit(ctx.assignment(), **kwargs)
						return variable.code

					else:
						variable = Variable()
						variable.ID = var_name
						variable.member = struct.ID
						variable.code = self.visit(ctx.assignment(), **kwargs)

						struct.member_variables.append(variable)
						self.scope_tracker.declareVariable(variable, struct)
						return variable.code
		else:
			if ctx.IDENTIFIER():
				var_name = str(ctx.IDENTIFIER())
				self.debug << NL() << "Assign Value to [" << var_name << "]"

				code = self.visit(ctx.assignment(), **kwargs)
				self.scope_tracker.lookupVariable(var_name, None).code = code
				return code
 
		self.exitFull("Assignment")

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext, **kwargs):
		self.enterFull("Or")

		left: Container = self.visit(ctx.logic_and(0), **kwargs)
		for i in range(1, len(ctx.logic_and())):
			right: Container = self.visit(ctx.logic_and(i), **kwargs)
			return Container(f"{left.getCode()} or {right.getCode()}", Type.BOOL)

		self.exitFull("Or")
		return self.visitChildren(ctx)

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext, **kwargs):
		self.enterFull("And")

		left: Container = self.visit(ctx.equality(0), **kwargs)
		for i in range(1, len(ctx.equality())):
			right: Container = self.visit(ctx.equality(i), **kwargs)
			return Container(f"{left.getCode()} and {right.getCode()}", Type.BOOL)

		self.exitFull("And")
		return self.visitChildren(ctx)

	def visitEquality(self, ctx:CompiscriptParser.EqualityContext, **kwargs):
		self.enterFull("Equality")

		if ctx.getChildCount() == 1:
			value: Container = self.visit(ctx.comparison(0), **kwargs)
			self.exitFull("Equality")
			return value

		left: Container = self.visit(ctx.comparison(0), **kwargs)
		for i in range(1, len(ctx.comparison())):
			operator = ctx.getChild(2 * i - 1).getText()
			right: Container = self.visit(ctx.comparison(i), **kwargs)
			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Comparison. {left} {operator} {right}")
			self.exitFull("Equality")
			return Container(f"{left.getCode()} {operator} {right.getCode()}", Type.BOOL)

	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext, **kwargs):
		self.enterFull("Comparison")

		if ctx.getChildCount() == 1:
			value: Container = self.visit(ctx.term(0))
			self.exitFull("Comparison")
			return value

		left: Container = self.visit(ctx.term(0), **kwargs)
		for i in range(1, len(ctx.term())):
			operator = ctx.getChild(2 * i - 1).getText()
			right: Container = self.visit(ctx.term(i), **kwargs)
			if not isinstance(left, Container) or not isinstance(right, Container):
				error(self.debug, f"Error Comparison. {left} {operator} {right}")
			self.exitFull("Comparison")
			return Container(f"{left.getCode()} {operator} {right.getCode()}", Type.BOOL)

	def visitTerm(self, ctx:CompiscriptParser.TermContext, **kwargs):
		self.enterFull("Term")

		if ctx.getChildCount() == 1:
			value: Container = self.visit(ctx.factor(0), **kwargs)
			self.exitFull("Term")
			return value

		left  : Container = self.visit(ctx.factor(0), **kwargs)
		operator: str = ctx.getChild(1).getText()
		right : Container = self.visit(ctx.factor(1), **kwargs)

		if not isinstance(left, Container) or not isinstance(right, Container):
			error(self.debug, f"Error Term. Evaluating Expression: None Arguments. [{left}] {operator} [{right}]")

		type = operationType(self.debug, left, operator, right)

		self.exitFull("Term")

		if operator == '+':
			return Container(f"({left.getCode()} + {right.getCode()})", type)
		elif operator == '-':
			return Container(f"({left.getCode()} - {right.getCode()})", type)

	def visitFactor(self, ctx:CompiscriptParser.FactorContext, **kwargs):
		self.enterFull("Factor")

		if ctx.getChildCount() == 1:
			value: Container = self.visit(ctx.unary(0), **kwargs)
			self.exitFull("Factor")
			return value

		left  : Container = self.visit(ctx.unary(0), **kwargs)
		operator: str = ctx.getChild(1).getText()
		right : Container = self.visit(ctx.unary(1), **kwargs)

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

	def visitArray(self, ctx:CompiscriptParser.ArrayContext, **kwargs):
		elements: List[Container] = []
		if ctx.expression():
			for expr in ctx.expression():
				elements.append(self.visit(expr, **kwargs))
		return Container(elements, Type.ARRAY)

	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext, **kwargs):

		class_name = ctx.IDENTIFIER().getText()

		args = []
		if ctx.arguments():
			args = self.visit(ctx.arguments(), **kwargs)
		
		return Container(self.scope_tracker.lookupClass(class_name), Type.VARIABLE)

	def visitUnary(self, ctx:CompiscriptParser.UnaryContext, **kwargs):
		self.enterFull("Unary")

		if ctx.getChildCount() == 2:
			operator = str(ctx.getChild(0))
			operand: Container = self.visit(ctx.unary(), **kwargs)
			if operator == '-':
				self.exitFull("Unary")
				return Container(f"-{operand.getCode()}", operand.type)
			elif operator == '!':
				self.exitFull("Unary")
				return Container(f"!{operand.getCode()}", operand.type)
		else:
			visited: Container = self.visit(ctx.getChild(0), **kwargs)
			self.exitFull("Unary")
			return visited

	def visitCall(self, ctx:CompiscriptParser.CallContext, **kwargs):
		self.enterFull("Call")
		self.exitFull("Call")
		return self.visitChildren(ctx, **kwargs)

	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext, **kwargs):
		self.enterFull("Primary")

		if ctx.NUMBER():
			text = str(ctx.NUMBER())
			self.exitFull("Primary")
			if '.' in text:
				return Container(text, Type.FLOAT)
			else:
				return Container(text, Type.INT)
		elif ctx.STRING():
			text = str(ctx.STRING()).strip('"')
			self.exitFull("Primary")
			return Container(text, Type.STRING)
		elif ctx.IDENTIFIER():
			var_name = str(ctx.IDENTIFIER())
			scope = kwargs["struct"] if "struct" in kwargs else None
			if self.scope_tracker.checkVariable(var_name, scope):
				self.exitFull("Primary")
				return Container(self.scope_tracker.lookupVariable(var_name, scope), Type.VARIABLE)
			else:
				error(self.debug, f"Error Primary. Variable '{var_name}' out of scope.")

		elif ctx.array():
			return self.visit(ctx.array())
		elif ctx.instantiation():
			return self.visit(ctx.instantiation())
		elif ctx.expression():
			return self.visit(ctx.expression())

		self.exitFull("Primary")
		if ctx.getText() == "true":
			return Container("true", Type.BOOL)
		elif ctx.getText() == "false":
			return Container("false", Type.BOOL)
		elif ctx.getText() == "nil":
			return Container("nil", Type.NONE)
		elif ctx.getText() == "this":
			return Container("this.", Type.MEMBER_POINTER)

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext, **kwargs):
		"""Assign Function Member to Class or create Function"""
		self.enter("Function")
		self.scope_tracker.enterScope()

		function = Function()
		function.ID = str(ctx.IDENTIFIER())
		if "struct" in kwargs and isinstance(kwargs["struct"], Class):
			function.member = kwargs["struct"].ID
			#TODO if function.ID == "init"
			#TODO this. variables
			if function.ID == "init":
				kwargs["struct"].initializer = function
#
		scope = kwargs["struct"] if "struct" in kwargs else None
		self.scope_tracker.exitScope()
		self.scope_tracker.declareFunction(function, scope)
		self.addSymbolToTable(function)
#
		self.exit("Function")
		return Container(function, Type.FUNCTION)

	def visitParameters(self, ctx:CompiscriptParser.ParametersContext, **kwargs):
		parameters: List[str] = []
		for identifier in ctx.IDENTIFIER():
			parameters.append(identifier.getText())
		return parameters

	def visitArguments(self, ctx:CompiscriptParser.ArgumentsContext, **kwargs):
		arguments = []
		for expr in ctx.expression():
			arguments.append(self.visit(expr, **kwargs))  # Visit and evaluate each expression
		return arguments

	def visitChildren(self, node: ParserRuleContext, **kwargs):
		result = self.defaultResult()
		for i in range(node.getChildCount()):
			if not self.shouldVisitNextChild(node, result):
				return result

			child = node.getChild(i)
			if isinstance(child, TerminalNodeImpl):
				continue
			childResult = self.visit(child, **kwargs)
			result = self.aggregateResult(result, childResult)

		return result

	def visit_default(self, node: ParserRuleContext, **kwargs):
		for child in node.getChildren():
			self.visit(child, **kwargs)

	def visit(self, node: ParserRuleContext, **kwargs):
		method_name = 'visit' + node.__class__.__name__.replace('Context', '')
		visitor_method = getattr(self, method_name, self.visit_default)
		return visitor_method(node, **kwargs)

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