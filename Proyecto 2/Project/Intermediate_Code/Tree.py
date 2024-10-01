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
			val.comapare_expression = self.visit(ctx.expression(0))
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
			val.declarations.append(ctx.declaration(i))

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

		return val

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		val = ANT_LogicOr()

		return val

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		val = ANT_LogicAnd()

		return val

	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		val = ANT_Equality()

		return val

	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		val = ANT_Comparison()

		return val

	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		val = ANT_Term()

		return val

	def visitFactor(self, ctx:CompiscriptParser.FactorContext):
		val = ANT_Factor()

		return val

	def visitArray(self, ctx:CompiscriptParser.ArrayContext):
		val = ANT_Array()

		return val

	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
		val = ANT_Instantiation()

		return val

	def visitUnary(self, ctx:CompiscriptParser.UnaryContext):
		val = ANT_Unary()

		return val

	def visitCall(self, ctx:CompiscriptParser.CallContext):
		val = ANT_Call()

		return val

	def visitSuperCall(self, ctx:CompiscriptParser.SuperCallContext):
		val = ANT_SuperCall()

		return val

	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
		val = ANT_Primary()

		return val

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		val = ANT_Function()

		return val

	def visitVariable(self, ctx:CompiscriptParser.VariableContext):
		val = ANT_Variable()

		return val

	def visitParameters(self, ctx:CompiscriptParser.ParametersContext):
		val = ANT_Parameters()

		return val

	def visitArguments(self, ctx:CompiscriptParser.ArgumentsContext):
		val = ANT_Arguments()

		return val