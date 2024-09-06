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

		members: List[Union[Function, Variable]] = self.visit(ctx.classBody(), **kwargs, visiting_class = struct, visitor = struct)
		for member in members:
			if isinstance(member, Function):
				struct.member_functions.append(member)
			elif isinstance(member, Variable):
				struct.member_variables.append(member)
			else:
				print(member)
#
		self.scope_tracker.declareClass(struct)
		self.addSymbolToTable(struct)
		self.scope_tracker.exitScope()
#
		self.exit("Class Declaration")
		return Container(struct, Type.FUNCTION)

	def visitClassBody(self, ctx:CompiscriptParser.ClassBodyContext, **kwargs):
		self.enter("Class Body")
		members: List[Union[Function, Variable]] = []
		for i in range(len(ctx.classMember())):
			member = self.visit(ctx.classMember(i), **kwargs)
			members.append(member)
		self.exit("Class Body")
		return members

	def visitClassMember(self, ctx:CompiscriptParser.ClassMemberContext, **kwargs):
		self.enter("Member Declaration")
		self.scope_tracker.enterScope()

		if ctx.varDecl() is not None:
			variable: Variable = self.visit(ctx.varDecl(), **kwargs)
			self.exit("Member Declaration")
			return variable

		elif ctx.function() is not None:
			function: Function = self.visit(ctx.function(), **kwargs)
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
		if "visitor" in kwargs and isinstance(kwargs["visitor"], Class):
			variable.member = kwargs["visiting_class"]
#
		if ctx.expression():
			var = self.visit(ctx.expression(), **kwargs)
			if isinstance(var, Container):
				variable.code = var.getCode()
				variable.type = var.type
			else:
				variable.code = var
				variable.type = inferVariableType(var)

		self.debug << NL() << f"Variable [{variable.ID}]"
#
		self.scope_tracker.declareVariable(variable)
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

		if ctx.IDENTIFIER() is not None:
			var_name = str(ctx.IDENTIFIER())
			self.debug << NL() << "Assign Value to [" << var_name << "]"

			if ctx.assignment() is not None:
				value = self.visit(ctx.assignment(), **kwargs)
			elif ctx.logic_or() is not None:
				value = self.visit(ctx.logic_or(), **kwargs)

			self.scope_tracker.lookupVariable(var_name).code = value

		visited = self.visitChildren(ctx)
		self.exitFull("Assignment")
		return visited

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
			if not isinstance(left, Container):
				error(self.debug, f"Error Equality. {left} {operator} {right}")
			if not isinstance(right, Container):
				error(self.debug, f"Error Equality. {left} {operator} {right}")
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
			if not isinstance(left, Container):
				error(self.debug, f"Error Comparison. {left} {operator} {right}")
			if not isinstance(right, Container):
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

		if left is None or right is None:
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

		if left is None or right is None:
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
		return self.visitChildren(ctx, **kwargs)

	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext, **kwargs):
		return self.visitChildren(ctx, **kwargs)

	def visitUnary(self, ctx:CompiscriptParser.UnaryContext, **kwargs):
		self.enterFull("Unary")

		if ctx.getChildCount() == 2:
			operator = str(ctx.getChild(0))
			operand: Container = self.visit(ctx.getChild(1), **kwargs)
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
			if self.scope_tracker.checkVariable(var_name):
				self.exitFull("Primary")
				return Container(self.scope_tracker.lookupVariable(var_name), Type.VARIABLE)
			else:
				error(self.debug, f"Error Primary. Variable '{var_name}' out of scope.")
		if ctx.expression():
			visited = self.visit(ctx.expression())

		self.exitFull("Primary")
		if ctx.getText() == "true":
			return Container("true", Type.BOOL)
		elif ctx.getText() == "false":
			return Container("false", Type.BOOL)
		elif ctx.getText() == "nil":
			return Container("nil", Type.NONE)
		elif ctx.expression():
			return visited  # Delegate to expression handling

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext, **kwargs):
		"""Assign Function Member to Class or create Function"""
		self.enter("Function")
		self.scope_tracker.enterScope()

		function = Function()
		function.ID = str(ctx.IDENTIFIER())
		if "visitor" in kwargs and isinstance(kwargs["visitor"], Class):
			function.member = kwargs["visiting_class"]
			#TODO if function.ID == "init"
			#TODO this. variables
			if function.ID == "init":
				kwargs["visitor"].initializer = function	
#
		self.scope_tracker.declareFunction(function)
		self.addSymbolToTable(function)
		self.scope_tracker.exitScope()
#
		self.exit("Function")
		return function

	def visitParameters(self, ctx:CompiscriptParser.ParametersContext, **kwargs):
		return self.visitChildren(ctx)

	def visitArguments(self, ctx:CompiscriptParser.ArgumentsContext, **kwargs):
		return self.visitChildren(ctx)

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