from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from .Classes import *

class Tree_Generator(CompiscriptVisitor):
	def __init__(self):
		super().__init__()

	def visitProgram(self, ctx:CompiscriptParser.ProgramContext):
		val = ANT_Program()

		for i in range(len(ctx.declaration())):
			val.declarations.append(self.visit(ctx.declaration(i)))

		return val

	def visitDeclaration(self, ctx:CompiscriptParser.DeclarationContext):
		val = ANT_Declaration()

		if ctx.classDecl():
			val.classDecl = self.visit(ctx.classDecl())
		elif ctx.funDecl():
			val.funDecl = self.visit(ctx.funDecl())
		elif ctx.varDecl():
			val.varDecl = self.visit(ctx.varDecl())
		elif ctx.statement():
			val.statement = self.visit(ctx.statement())

		return val

	def visitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
		val = ANT_ClassDecl()

		val.IDENTIFIER = str(ctx.IDENTIFIER(0))
		if ctx.IDENTIFIER(1):
			val.extends = str(ctx.IDENTIFIER(1))
		val.class_body = self.visit(ctx.classBody())

		return val

	def visitClassBody(self, ctx:CompiscriptParser.ClassBodyContext):
		val = ANT_ClassBody()

		for i in range(len(ctx.classMember())):
			val.class_members.append(self.visit(ctx.classMember(i)))

		return val

	def visitClassMember(self, ctx:CompiscriptParser.ClassMemberContext):
		val = ANT_ClassMember()

		val.function = self.visit(ctx.function())

		return val

	def visitFunDecl(self, ctx:CompiscriptParser.FunDeclContext):
		val = ANT_FunDecl()

		val.function = self.visit(ctx.function())

		return val

	def visitVarDecl(self, ctx:CompiscriptParser.VarDeclContext):
		val = ANT_VarDecl()

		val.variable = self.visit(ctx.variable())

		return val

	def visitStatement(self, ctx:CompiscriptParser.StatementContext):
		val = ANT_Statement()

		if ctx.exprStmt():
			val.exprStmt = self.visit(ctx.exprStmt())
		elif ctx.forStmt():
			val.forStmt = self.visit(ctx.forStmt())
		elif ctx.ifStmt():
			val.ifStmt = self.visit(ctx.ifStmt())
		elif ctx.printStmt():
			val.printStmt = self.visit(ctx.printStmt())
		elif ctx.returnStmt():
			val.returnStmt = self.visit(ctx.returnStmt())
		elif ctx.whileStmt():
			val.whileStmt = self.visit(ctx.whileStmt())
		elif ctx.block():
			val.block = self.visit(ctx.block())

		return val

	def visitExprStmt(self, ctx:CompiscriptParser.ExprStmtContext):
		val = ANT_ExprStmt()

		if ctx.expression():
			val.expression = self.visit(ctx.expression())

		return val

	def visitForStmt(self, ctx:CompiscriptParser.ForStmtContext):
		val = ANT_ForStmt()

		if ctx.varDecl():
			val.varDecl = self.visit(ctx.varDecl())
		else:
			val.exprStmt = self.visit(ctx.exprStmt())
		if ctx.expression(0):
			val.compare_expression = self.visit(ctx.expression(0))
		if ctx.expression(1):
			val.increment_expression = self.visit(ctx.expression(1))
		val.statement = self.visit(ctx.statement())

		return val

	def visitIfStmt(self, ctx:CompiscriptParser.IfStmtContext):
		val = ANT_IfStmt()

		val.expression = self.visit(ctx.expression())
		val.if_statement = self.visit(ctx.statement(0))
		if ctx.statement(1):
			val.else_statement = self.visit(ctx.statement(1))

		return val

	def visitPrintStmt(self, ctx:CompiscriptParser.PrintStmtContext):
		val = ANT_PrintStmt()

		if ctx.expression():
			val.expression = self.visit(ctx.expression())

		return val

	def visitReturnStmt(self, ctx:CompiscriptParser.ReturnStmtContext):
		val = ANT_ReturnStmt()

		if ctx.expression():
			val.expression = self.visit(ctx.expression())

		return val

	def visitWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext):
		val = ANT_WhileStmt()

		val.expression = self.visit(ctx.expression())
		val.statement = self.visit(ctx.statement())

		return val

	def visitBlock(self, ctx:CompiscriptParser.BlockContext):
		val = ANT_Block()

		for i in range(len(ctx.declaration())):
			val.declarations.append(self.visit(ctx.declaration(i)))

		return val

	def visitFunAnon(self, ctx:CompiscriptParser.FunAnonContext):
		val = ANT_FunAnon()

		if ctx.parameters():
			val.parameters = self.visit(ctx.parameters())
		val.block = self.visit(ctx.block())

		return val

	def visitExpression(self, ctx:CompiscriptParser.ExpressionContext):
		val = ANT_Expression()

		if ctx.assignment():
			val.assignment = self.visit(ctx.assignment())
		else:
			val.funAnon = self.visit(ctx.funAnon())

		return val

	def visitAssignment(self, ctx:CompiscriptParser.AssignmentContext):
		val = ANT_Assignment()

		if ctx.logic_or():
			val.logic_or = self.visit(ctx.logic_or())
		else:
			if ctx.call():
				val.call = self.visit(ctx.call())
			val.IDENTIFIER = str(ctx.IDENTIFIER())
			val.assignment = self.visit(ctx.assignment())

		return val

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		val = ANT_LogicOr()

		val.left = self.visit(ctx.logic_and(0))
		for i in range(1, len(ctx.logic_and())):
			val.array.append((
				str(ctx.getChild(2 * i - 1)),
				self.visit(ctx.logic_and(i))
			))

		return val

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		val = ANT_LogicAnd()

		val.left = self.visit(ctx.equality(0))
		for i in range(1, len(ctx.equality())):
			val.array.append((
				str(ctx.getChild(2 * i - 1)),
				self.visit(ctx.equality(i))
			))

		return val

	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		val = ANT_Equality()

		val.left = self.visit(ctx.comparison(0))
		for i in range(1, len(ctx.comparison())):
			val.array.append((
				str(ctx.getChild(2 * i - 1)),
				self.visit(ctx.comparison(i))
			))

		return val

	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		val = ANT_Comparison()

		val.left = self.visit(ctx.term(0))
		for i in range(1, len(ctx.term())):
			val.array.append((
				str(ctx.getChild(2 * i - 1)),
				self.visit(ctx.term(i))
			))

		return val

	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		val = ANT_Term()

		val.left = self.visit(ctx.factor(0))
		for i in range(1, len(ctx.factor())):
			val.array.append((
				str(ctx.getChild(2 * i - 1)),
				self.visit(ctx.factor(i))
			))

		return val

	def visitFactor(self, ctx:CompiscriptParser.FactorContext):
		val = ANT_Factor()

		val.left = self.visit(ctx.unary(0))
		for i in range(1, len(ctx.unary())):
			val.array.append((
				str(ctx.getChild(2 * i - 1)),
				self.visit(ctx.unary(i))
			))

		return val

	def visitArray(self, ctx:CompiscriptParser.ArrayContext):
		val = ANT_Array()

		for i in range(len(ctx.expression())):
			val.expressions.append(self.visit(ctx.expression(i)))

		return val

	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
		val = ANT_Instantiation()

		val.IDENTIFIER = str(ctx.IDENTIFIER())
		if ctx.arguments():
			val.arguments = self.visit(ctx.arguments())

		return val

	def visitUnary(self, ctx:CompiscriptParser.UnaryContext):
		val = ANT_Unary()

		if ctx.unary():
			val.operator = str(ctx.getChild(0))
			val.unary = self.visit(ctx.unary())
		else:
			val.call = self.visit(ctx.call())

		return val

	def visitCall(self, ctx:CompiscriptParser.CallContext):
		val = ANT_Call()

		if ctx.funAnon():
			val.funAnon = self.visit(ctx.funAnon())
		else:
			val.primary = self.visit(ctx.primary())
			i = 1  # Start after the primary
			while i < ctx.getChildCount():
				if ctx.getChild(i).getText() == '(':
					if ctx.getChild(i+1).getText() == ")":
						val.calls.append("()")
						i+=1
					else:
						val.calls.append(self.visit(ctx.getChild(i+1)))
						i+=2
				elif ctx.IDENTIFIER(i):
					val.calls.append(str(ctx.IDENTIFIER(i)))
				elif ctx.expression(i):
					val.calls.append(self.visit(ctx.expression(i)))
				i+=1

		return val

	def visitSuperCall(self, ctx:CompiscriptParser.SuperCallContext):
		val = ANT_SuperCall()

		val.IDENTIFIER = str(ctx.IDENTIFIER())

		return val

	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
		val = ANT_Primary()

		if ctx.array() or ctx.instantiation():
			if ctx.array():
				val.array = self.visit(ctx.array())
			else:
				val.instantiation = self.visit(ctx.instantiation())
		elif ctx.superCall():
			val.superCall = self.visit(ctx.superCall())
		elif ctx.NUMBER() or ctx.STRING() or ctx.IDENTIFIER() or ctx.expression():
			if ctx.NUMBER():
				val.NUMBER = str(ctx.NUMBER())
			elif ctx.STRING():
				val.STRING = str(ctx.STRING())
			elif ctx.IDENTIFIER():
				val.IDENTIFIER = str(ctx.IDENTIFIER())
			else:
				val.expression = self.visit(ctx.expression())
		else:
			val.operator = ctx.getText()

		return val

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		val = ANT_Function()

		val.IDENTIFIER = str(ctx.IDENTIFIER())
		if ctx.parameters():
			val.parameters = self.visit(ctx.parameters())
		val.block = self.visit(ctx.block())

		return val

	def visitVariable(self, ctx:CompiscriptParser.VariableContext):
		val = ANT_Variable()

		val.IDENTIFIER = str(ctx.IDENTIFIER())
		if ctx.expression():
			val.expression = self.visit(ctx.expression())

		return val

	def visitParameters(self, ctx:CompiscriptParser.ParametersContext):
		val = ANT_Parameters()

		for i in range(len(ctx.IDENTIFIER())):
			val.identifiers.append(str(ctx.IDENTIFIER(i)))

		return val

	def visitArguments(self, ctx:CompiscriptParser.ArgumentsContext):
		val = ANT_Arguments()

		for i in range(len(ctx.expression())):
			val.expressions.append(self.visit(ctx.expression(i)))

		return val