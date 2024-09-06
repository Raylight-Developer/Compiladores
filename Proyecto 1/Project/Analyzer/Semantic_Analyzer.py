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

	def visitProgram(self, ctx:CompiscriptParser.ProgramContext):
		return self.visitChildren(ctx)

	def visitDeclaration(self, ctx:CompiscriptParser.DeclarationContext):
		return self.visitChildren(ctx)

	def visitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
		self.scope_tracker.enterScope()

		struct = Class()
		struct.ID = str(ctx.IDENTIFIER(0))
		self.addSymbolToTable(struct)

		children = self.visitChildren(ctx)
		self.scope_tracker.exitScope()
		return children

	def visitFunDecl(self, ctx:CompiscriptParser.FunDeclContext):
		self.scope_tracker.enterScope()

		function = Function()
		function.ID = str(ctx.IDENTIFIER())
		self.addSymbolToTable(function)

		children = self.visitChildren(ctx)
		self.scope_tracker.exitScope()
		return children


	def visitVarDecl(self, ctx:CompiscriptParser.VarDeclContext):
		self.enter("VarDecl")
#
		variable = Variable()
		variable.ID = str(ctx.IDENTIFIER())
		variable.code = ctx.getText()
#
		if ctx.expression():
			var = self.visit(ctx.expression())
			if isinstance(var, Container):
				variable.code = var.code
				variable.type = var.type
			else:
				variable.code = var
				variable.type = inferVariableType(var)

		self.debug << NL() << f"Variable [{variable.ID}]"
#
		self.scope_tracker.declareVariable(variable)
		self.addSymbolToTable(variable)
#
		self.exit("VarDecl")

		return self.visitChildren(ctx)

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
			error(self.debug, f"Evaluating Expression: None Arguments. [{left}] {operator} [{right}]")

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
			error(self.debug, f"Evaluating Expression: Unknown Operator. [{left}] {operator} [{right}]")

		self.exitFull("Expression")

	def visitAssignment(self, ctx:CompiscriptParser.AssignmentContext):
		"""Assign Code to a Variable"""
		self.enterFull("Assignment")

		if ctx.IDENTIFIER() is not None:
			var_name = str(ctx.IDENTIFIER())
			self.debug << NL() << "Assign Value to [" << var_name << "]"

			if ctx.assignment() is not None:
				value = self.visit(ctx.assignment())
			elif ctx.logic_or() is not None:
				value = self.visit(ctx.logic_or())

			self.scope_tracker.lookupVariable(var_name).code = value

		visited = self.visitChildren(ctx)
		self.exitFull("Assignment")
		return visited

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		self.enterFull("Or")
		
		for i in range(ctx.getChildCount()):
			operator = self.visit(ctx.getChild(i))

			if operator == None:
				left  : Container = self.visit(ctx.getChild(i-1))
				right : Container = self.visit(ctx.getChild(i+1))
				operator = "or"
				return Container(f"{left.code} {operator} {right.code}", Type.BOOL)

		self.exitFull("Or")
		return self.visitChildren(ctx)

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		self.enterFull("And")
		
		for i in range(ctx.getChildCount()):
			operator = self.visit(ctx.getChild(i))

			if operator == None:
				left  : Container = self.visit(ctx.getChild(i-1))
				right : Container = self.visit(ctx.getChild(i+1))
				operator = "and"
				return Container(f"{left.code} {operator} {right.code}", Type.BOOL)

		self.exitFull("And")
		return self.visitChildren(ctx)

	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		self.enterFull("Equality")

		text = ctx.getText()

		visited = self.visitChildren(ctx)
		self.exitFull("Equality")

		if any(item in ["!=", "=="] for item in text):
			return Container(ctx.getText(), Type.BOOL)
		return visited

	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		self.enterFull("Comparison")

		text = ctx.getText()

		visited = self.visitChildren(ctx)
		self.exitFull("Comparison")

		if any(item in ["<=", ">=", "<", ">", "!=", "==", "!"] for item in text):
			return Container(ctx.getText(), Type.BOOL)
		return visited

	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		self.enterFull("Term")

		if ctx.getChildCount() == 1:
			self.exitFull("Term")
			return self.visit(ctx.factor(0))

		left  : Container = self.visit(ctx.factor(0))
		operator: str = ctx.getChild(1).getText()
		right : Container = self.visit(ctx.factor(1))

		if left is None or right is None:
			error(self.debug, f"Evaluating Expression: None Arguments. [{left}] {operator} [{right}]")

		type = operationType(self.debug, left.type, operator, right.type)

		self.exitFull("Term")

		if operator == '+':
			return Container(f"({left.code} + {right.code})", type)
		elif operator == '-':
			return Container(f"({left.code} - {right.code})", type)

	def visitFactor(self, ctx:CompiscriptParser.FactorContext):
		self.enterFull("Factor")

		if ctx.getChildCount() == 1:
			self.exitFull("Factor")
			return self.visit(ctx.unary(0))

		left  : Container = self.visit(ctx.unary(0))
		operator: str = ctx.getChild(1).getText()
		right : Container = self.visit(ctx.unary(1))

		if left is None or right is None:
			error(self.debug, f"Evaluating Expression: None Arguments. [{left}] {operator} [{right}]")

		type = operationType(self.debug, left.type, operator, right.type)

		self.exitFull("Factor")

		if operator == '*':
			return Container(f"({left.code} * {right.code})", type)
		elif operator == '/':
			return Container(f"({left.code} / {right.code})", type)
		elif operator == '%':
			return Container(f"({left.code} % {right.code})", type)

	def visitArray(self, ctx:CompiscriptParser.ArrayContext):
		return self.visitChildren(ctx)

	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
		return self.visitChildren(ctx)

	def visitUnary(self, ctx:CompiscriptParser.UnaryContext):
		self.enterFull("Unary")

		if ctx.getChildCount() == 2:
			operator = str(ctx.getChild(0))
			operand = self.visit(ctx.getChild(1))
			if operator == '-':
				self.exitFull("Unary")
				return -operand
			elif operator == '!':
				self.exitFull("Unary")
				return not operand
		else:
			visited = self.visit(ctx.getChild(0))
			self.exitFull("Unary")
			return visited

	def visitCall(self, ctx:CompiscriptParser.CallContext):
		return self.visitChildren(ctx)

	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
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
				return self.scope_tracker.lookupVariable(var_name)
			else:
				error(self.debug, f"Variable '{var_name}' out of scope.")
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

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		return self.visitChildren(ctx)

	def visitParameters(self, ctx:CompiscriptParser.ParametersContext):
		return self.visitChildren(ctx)

	def visitArguments(self, ctx:CompiscriptParser.ArgumentsContext):
		return self.visitChildren(ctx)

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