from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from .Symbols import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *
from .Scope import *

class Semantic_Analyzer(CompiscriptVisitor):
	def __init__(self, debug: Lace, table_c: Symbol_Table, table_f: Symbol_Table, table_v: Symbol_Table, parser: CompiscriptParser):
		super().__init__()
		self.parser = parser

		self.debug = debug
		self.count = 0
		self.graph = Digraph()
		self.scope_tracker = Scope_Tracker()

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
		struct.ID = ctx.IDENTIFIER(0).getText()
		self.addSymbolToTable(struct)

		self.scope_tracker.exitScope()
		return self.visitChildren(ctx)

	def visitFunDecl(self, ctx:CompiscriptParser.FunDeclContext):
		self.scope_tracker.enterScope()

		function = Function()
		function.ID = ctx.IDENTIFIER().getText()
		self.addSymbolToTable(function)

		self.scope_tracker.exitScope()
		return self.visitChildren(ctx)

	def visitVarDecl(self, ctx:CompiscriptParser.VarDeclContext):
		self.debug << NL() << "ENTER VarDecl"
		self.debug += 1
#
		variable = Variable()
#
		variable.ID = ctx.IDENTIFIER().getText()
		variable.code = ctx.getText()
		if ctx.expression():
			var = self.visit(ctx.expression())
			if isinstance(var, Container):
				variable.code = var.code
				variable.type = var.type
			else:
				variable.code = var
				variable.type = inferVariableType(var)

		self.debug << NL() << f"Variable [{variable.ID}]"
		self.debug << NL() << f"Declaration [{variable.code}]"
#
		self.scope_tracker.declareVariable(variable)
		self.addSymbolToTable(variable)
#
		self.debug -= 1
		self.debug << NL() << "EXIT  VarDecl"

		return self.visitChildren(ctx)

	def visitStatement(self, ctx:CompiscriptParser.StatementContext):
		return self.visitChildren(ctx)

	def visitExprStmt(self, ctx:CompiscriptParser.ExprStmtContext):
		return self.visitChildren(ctx)

	def visitForStmt(self, ctx:CompiscriptParser.ForStmtContext):
		return self.visitChildren(ctx)

	def visitIfStmt(self, ctx:CompiscriptParser.IfStmtContext):
		return self.visitChildren(ctx)

	def visitPrintStmt(self, ctx:CompiscriptParser.PrintStmtContext):
		return self.visitChildren(ctx)

	def visitReturnStmt(self, ctx:CompiscriptParser.ReturnStmtContext):
		return self.visitChildren(ctx)

	def visitWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext):
		return self.visitChildren(ctx)

	def visitBlock(self, ctx:CompiscriptParser.BlockContext):
		return self.visitChildren(ctx)

	def visitFunAnon(self, ctx:CompiscriptParser.FunAnonContext):
		return self.visitChildren(ctx)

	def visitExpression(self, ctx:CompiscriptParser.ExpressionContext):
		if ctx.getChildCount() == 1:
			return self.visit(ctx.getChild(0))

		left = self.visit(ctx.getChild(0))
		operator = ctx.getChild(1).getText()
		right = self.visit(ctx.getChild(2))

		# Si alguno de los operandos es None, algo salió mal en el procesamiento anterior
		if left is None or right is None:
			raise Exception("Error en la evaluación de la expresión: uno de los operandos es None.")
		self.log(left, operator, right)
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
			self.debug << NL() << f"Error Evaluating Expression: Unknown Operator. [{left}] {operator} [{right}]"
			raise Exception(f"Error Evaluating Expression: Unknown Operator. [{left}] {operator} [{right}]")

	def visitAssignment(self, ctx:CompiscriptParser.AssignmentContext):
		"""Assign Code to a Variable"""

		if ctx.IDENTIFIER() is not None:
			var_name = ctx.IDENTIFIER().getText()
			self.debug << NL() << "Assign Value to [" << var_name << "]"

			if ctx.assignment() is not None:
				# Visita la expresión a la derecha del '='
				value = self.visit(ctx.assignment())
			elif ctx.logic_or() is not None:
				# Visita la lógica "or" si está presente
				value = self.visit(ctx.logic_or())

			self.scope_tracker.lookupVariable(var_name).code = value

		return self.visitChildren(ctx)

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		return self.visitChildren(ctx)

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		return self.visitChildren(ctx)

	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		text = ctx.getText()
		if any(item in ["!=", "=="] for item in text):
			return Container(ctx.getText(), Type.BOOL)
		return self.visitChildren(ctx)

	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		text = ctx.getText()
		if any(item in ["<=", ">=", "<", ">", "!=", "==", "!"] for item in text):
			return Container(ctx.getText(), Type.BOOL)
		return self.visitChildren(ctx)

	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		if ctx.getChildCount() == 1:
			return self.visit(ctx.factor(0))

		left  : Container = self.visit(ctx.factor(0))
		right : Container = self.visit(ctx.factor(1))

		#self.debug << NL() << f"{left} " << f"[{type(left)}]" << f" - {right} " << f"[{type(right)}]"

		if left is None or right is None:
			self.debug << NL() << f"Error Evaluating Expression: None Operator. [{left}] - [{right}]"
			raise Exception(f"Error Evaluating Expression: None Operator. [{left}] - [{right}]")

		type = Type.FLOAT
		if left.type == Type.INT and right.type == Type.INT:
			type = Type.INT
		elif left.type == Type.FLOAT and right.type == Type.INT:
			type = Type.FLOAT
		elif left.type == Type.INT and right.type == Type.FLOAT:
			type = Type.FLOAT
		elif left.type == Type.FLOAT and right.type == Type.FLOAT:
			type = Type.FLOAT

		if ctx.getChild(1).getText() == '+':
			return Container(f"({left.code} + {right.code})", type)
		elif ctx.getChild(1).getText() == '-':
			return Container(f"({left.code} - {right.code})", type)
		else:
			self.debug << NL() << f"Error Cannot operate different Types [{left.type}]({left.code}) - [{right.type}]({right.code})"
			raise Exception(f"Error Cannot operate different Types [{left.type}]({left.code}) - [{right.type}]({right.code})")

	def visitFactor(self, ctx:CompiscriptParser.FactorContext):
		if ctx.getChildCount() == 1:
			return self.visit(ctx.unary(0))

		left  : Container = self.visit(ctx.unary(0))
		right : Container = self.visit(ctx.unary(1))

		#self.debug << NL() << f"{left} " << f"[{type(left)}]" << f" - {right} " << f"[{type(right)}]"

		if left is None or right is None:
			self.debug << NL() << f"Error Evaluating Expression: None Operator. [{left}] - [{right}]"
			raise Exception(f"Error Evaluating Expression: None Operator. [{left}] - [{right}]")

		type = Type.FLOAT
		if left.type == Type.INT and right.type == Type.INT:
			type = Type.INT
		elif left.type == Type.FLOAT and right.type == Type.INT:
			type = Type.FLOAT
		elif left.type == Type.INT and right.type == Type.FLOAT:
			type = Type.FLOAT
		elif left.type == Type.FLOAT and right.type == Type.FLOAT:
			type = Type.FLOAT
		else:
			self.debug << NL() << f"Error Cannot operate different Types [{left.type}]({left.code}) - [{right.type}]({right.code})"
			raise Exception(f"Error Cannot operate different Types [{left.type}]({left.code}) - [{right.type}]({right.code})")

		if ctx.getChild(1).getText() == '*':
			return Container(f"({left.code} * {right.code})", type)
		elif ctx.getChild(1).getText() == '/':
			return Container(f"({left.code} / {right.code})", type)
		elif ctx.getChild(1).getText() == '%':
			return Container(f"({left.code} % {right.code})", type)

	def visitArray(self, ctx:CompiscriptParser.ArrayContext):
		return self.visitChildren(ctx)

	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
		return self.visitChildren(ctx)

	def visitUnary(self, ctx:CompiscriptParser.UnaryContext):
		if ctx.getChildCount() == 2:
			operator = ctx.getChild(0).getText()
			operand = self.visit(ctx.getChild(1))
			if operator == '-':
				return -operand
			elif operator == '!':
				return not operand
		else:
			return self.visit(ctx.getChild(0))

	def visitCall(self, ctx:CompiscriptParser.CallContext):
		return self.visitChildren(ctx)

	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
		if ctx.NUMBER():
			text = ctx.NUMBER().getText()
			if '.' in text:
				return Container(text, Type.FLOAT)
			else:
				return Container(text, Type.INT)
		elif ctx.STRING():
			text = ctx.STRING().getText().strip('"')
			return Container(text, Type.STRING)
		elif ctx.IDENTIFIER():
			var_name = ctx.IDENTIFIER().getText()
			if self.scope_tracker.checkVariable(var_name):
				return self.scope_tracker.lookupVariable(var_name)
			else:
				self.debug << NL() << f"Variable '{var_name}' out of scope."
				self.debug << NL() << f"Variables declaradas in the current scope:"
				self.debug += 1
				for variable in self.scope_tracker.global_variables.forward_map:
					self.debug << NL() << f"{variable}"
				raise Exception(f"Variable '{var_name}' out of scope.")
		elif ctx.getText() == "true":
			return Container("true", Type.BOOL)
		elif ctx.getText() == "false":
			return Container("false", Type.BOOL)
		elif ctx.getText() == "nil":
			return Container("nil", Type.NONE)
		elif ctx.expression():
			return self.visit(ctx.expression())  # Delegate to expression handling

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