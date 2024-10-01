from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *

from Analyzer.Symbols import *
from Analyzer.Scope import *

from .Classes import *

class Tac_Info:
	def __init__(self, ID: str = "", data: Dict[str, Any] = {}):
		self.ID = ID
		self.data = data

class TAC_Generator(CompiscriptVisitor):
	def __init__(self, scope_tracker: Scope_Tracker = None):
		super().__init__()
		self.scope_tracker = scope_tracker
		self.label_count = -1
		self.temp_count = -1
		self.code = Lace()
		self.tac_info: Dict[Union[Function, Variable, Class, Function_Parameter], Tac_Info] = {}
		
		self.flags = {
			"visit_instantiation": 0,
			"visit_assignment": 0,
			"visit_comparison": 0,
			"visit_expression": 0,
			"visit_parameters": 0,
			"visit_arguments": 0,
			"visit_equality" : 0,
			"visit_function": 0,
			"visit_variable": 0,
			"visit_primary": 0,
			"visit_factor": 0,
			"visit_array": 0,
			"visit_super": 0,
			"visit_unary": 0,
			"visit_call": 0,
			"visit_term": 0,
			"visit_and": 0,
			"visit_or": 0,
		}

	def new_temp(self):
		self.temp_count += 1
		return f"T_{self.temp_count}"
	
	def new_label(self):
		self.label_count += 1
		return f"L_{self.label_count}"

	def declareClass(self, struct: Class):
		temp_id = self.new_temp()
		self.code << NL() << f"// Class:     [{temp_id}] {struct.ID}"
		self.tac_info[struct] = Tac_Info(temp_id, {})

	def declareFunction(self, function: Function):
		#temp_id = self.new_temp()
		block_id = self.new_label()
		self.code << NL() << "// Declare Function ["
		if function.member:
			self.code << function.member.ID << "."
		self.code << function.ID << "] {"
		self.code += 1
		self.code << NL() << block_id << ":"
		self.code -= 1
		self.code << NL() << "// }" << NL()
		self.tac_info[function] =  Tac_Info(block_id, { "Block ID" : block_id, "Block" : f"{function.data} // FUNCTION CODE" })

	def declareVariable(self, variable: Variable):
		temp_id = self.new_temp()
		#self.code << NL()
		#self.code << f"// Variable:  [{temp_id}] "
		#if variable.member:
		#	self.code << variable.member.ID << "."
		#self.code << variable.ID
		self.tac_info[variable] =  Tac_Info(temp_id)

	def declareParameter(self, parameter: Function_Parameter):
		temp_id = self.new_temp()
		#self.code << NL()
		#self.code << f"// Parameter:  [{temp_id}] "
		#self.code << parameter.function.ID << "." << parameter.ID
		self.tac_info[parameter] = Tac_Info(temp_id)

	def declareAnonFunction(self, function: Function):
		#temp_id = self.new_temp()
		block_id = self.new_label()
		#self.code << NL()
		#self.code << f"// Anon Function:  [{block_id}] [{block_id}] {function.ID}"
		self.tac_info[function] = Tac_Info(block_id, { "Block" : block_id })

	def assignVariable(self, variable: Variable):
		self.code << NL() << "// Assign Variable [" << variable.ID << "] {"
		self.code += 1
		self.code << NL()
		expression = self.visit(variable.ctx.expression())
		self.code << self.tac_info[variable].ID << ": " << expression
		self.code -= 1
		self.code << NL() << "// }" << NL()

	def callFunction(self, function: Function, call_params: List[Container]):
		self.code << NL() << "// Call Function ["
		if function.member:
			if function.member.parent:
				self.code << "Super<" << function.member.parent.ID << ">."
			else:
				self.code << function.member.ID << "."
		self.code << function.ID << "] {"
		self.code += 1
		self.code << NL()
		for i, param in enumerate(call_params):
			self.code << self.tac_info[function.parameters[i]].ID << ": "
			if param.type == Type.STRING:
				self.code << '"' << param.data << '"' << NL()
			elif param.type in [Type.FLOAT, Type.INT]:
				self.code << param.data << NL()
			else:
				self.code << param.data << NL()
		self.code << self.tac_info[self.scope_tracker.lookupFunction(function.ID, function.member)].data["Block"]
		self.code -= 1
		self.code << NL() << "// }" << NL()

	def generate_if(self, if_expr: List[str] = [], if_condition: str = "", if_body: List[str] = [], else_body: List[str] = []):
		if_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(if_expr)
		self.code << NL()
		self.code << NL() << f"IF ({if_condition}) GO_TO {if_label}"
		self.code += 1
		self.code << NL() << "\n".join(else_body)
		self.code -= 1
		self.code << NL() << f"GO_TO {end_label}"
		self.code << NL()
		self.code << NL() << f"{if_label}:"
		self.code += 1
		self.code << NL() << "\n".join(if_body)
		self.code -= 1
		self.code << NL()
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"

	def generate_while(self, while_expr: List[str] = [], while_condition: str = "", while_update: str = "", while_body: List[str] = []):
		loop_start_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(while_expr)
		self.code << NL()
		self.code << NL() << f"{loop_start_label}:"
		self.code += 1
		self.code << NL() << f"IF ({while_condition}) GO_TO {end_label}"
		self.code += 1
		self.code << NL() << "\n".join(while_body)
		self.code << NL() << while_update << " // Update While Condition"
		self.code -= 1
		self.code << NL() << f"GO_TO {loop_start_label}"
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"

	def generate_for(self, for_expr: List[str] = [], for_condition: str = "", for_update: str = "", for_body: List[str] = []):
		loop_start_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(for_expr)
		self.code << NL()
		self.code << NL() << f"{loop_start_label}:"
		self.code += 1
		self.code << NL() << f"IF ({for_condition}) GO_TO {end_label}"
		self.code << NL()
		self.code << NL() << "\n".join(for_body)
		self.code << NL() << for_update << " // Update For Condition"
		self.code << NL()
		self.code << NL() << f"GO_TO {loop_start_label}"
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"


	def visitProgram(self, ctx:CompiscriptParser.ProgramContext):
		val = ANT_Program()

		for i in range(len(ctx.declaration())):
			val.declarations.append(self.visit(ctx.declaration(i)))

		return val

	def visitDeclaration(self, ctx:CompiscriptParser.DeclarationContext):
		val = None
		return val

	def visitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
		return self.visitChildren(ctx)

	def visitClassBody(self, ctx:CompiscriptParser.ClassBodyContext):
		return self.visitChildren(ctx)

	def visitClassMember(self, ctx:CompiscriptParser.ClassMemberContext):
		return self.visitChildren(ctx)

	def visitFunDecl(self, ctx:CompiscriptParser.FunDeclContext):
		val = ANT_FunDecl()

		if ctx.function():
			val.function = self.visit(ctx.function())

		return val

	def visitVarDecl(self, ctx:CompiscriptParser.VarDeclContext):
		val = ANT_VarDecl()

		if ctx.variable():
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
		return self.visitChildren(ctx)


	def visitIfStmt(self, ctx:CompiscriptParser.IfStmtContext):
		return self.visitChildren(ctx)


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
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#block.
	def visitBlock(self, ctx:CompiscriptParser.BlockContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#funAnon.
	def visitFunAnon(self, ctx:CompiscriptParser.FunAnonContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#expression.
	def visitExpression(self, ctx:CompiscriptParser.ExpressionContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#assignment.
	def visitAssignment(self, ctx:CompiscriptParser.AssignmentContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#logic_or.
	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#logic_and.
	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#equality.
	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#comparison.
	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#term.
	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#factor.
	def visitFactor(self, ctx:CompiscriptParser.FactorContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#array.
	def visitArray(self, ctx:CompiscriptParser.ArrayContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#instantiation.
	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#unary.
	def visitUnary(self, ctx:CompiscriptParser.UnaryContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#call.
	def visitCall(self, ctx:CompiscriptParser.CallContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#superCall.
	def visitSuperCall(self, ctx:CompiscriptParser.SuperCallContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#primary.
	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#function.
	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#variable.
	def visitVariable(self, ctx:CompiscriptParser.VariableContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#parameters.
	def visitParameters(self, ctx:CompiscriptParser.ParametersContext):
		return self.visitChildren(ctx)


	# Visit a parse tree produced by CompiscriptParser#arguments.
	def visitArguments(self, ctx:CompiscriptParser.ArgumentsContext):
		return self.visitChildren(ctx)