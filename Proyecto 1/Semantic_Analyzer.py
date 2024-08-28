from CompiscriptVisitor import CompiscriptVisitor
from CompiscriptParser import CompiscriptParser
from CompiscriptLexer import CompiscriptLexer
from Symbol_Table import Symbol_Table, Symbol_Property

from Include import *

class Semantic_Analyzer(CompiscriptVisitor):
	def __init__(self, log: QTextBrowser, table_functions: Symbol_Table, table_variables: Symbol_Table, table_classes: Symbol_Table, parser: CompiscriptParser):
		super().__init__()
		self.counter = 1
		self.parser = parser
		self.graph = Digraph()
		self.log = log
		self.table_functions = table_functions
		self.table_variables = table_variables
		self.table_classes = table_classes

		self.global_variables: Dict[str, ParserRuleContext] = {}
		self.local_variables: Dict[str, ParserRuleContext] = {}

	def visitProgram(self, ctx:CompiscriptParser.ProgramContext):
		return self.visitChildren(ctx)

	def visitDeclaration(self, ctx:CompiscriptParser.DeclarationContext):
		return self.visitChildren(ctx)

	def visitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
		return self.visitChildren(ctx)

	def visitFunDecl(self, ctx: CompiscriptParser.FunDeclContext):
		fun_name = ctx.function().IDENTIFIER().getText()

		# Verifica si la función ya está declarada
		if fun_name in self.functions:
			raise Exception(f"Error: Función '{fun_name}' ya declarada.")

		# Registra la función en la tabla de símbolos
		self.functions[fun_name] = ctx

		# Construir los datos del símbolo
		symbol_data = Symbol_Property()
		symbol_data.id = fun_name                    # ID
		symbol_data.type = "function"                  # Data_Type
		symbol_data.size = "-"                         # Size (no aplica a funciones)
		symbol_data.offset = "-"                         # Offset (no aplica a funciones)
		symbol_data.scope = "global"                    # Scope (asumiendo que las funciones son globales)
		#symbol_data. = "function"                   # Structure ????????????????????????????????????????????????????????????????????????????????????????????

		# Agregar el símbolo a la tabla
		# self.table_functions.add(symbol_data)???????????????????????????????????????????????????????????????????????????????????????????????????????

		# Construir el AST
		node_id = self.nodeTree(ctx)

		# Visita el cuerpo de la función
		self.visit(ctx.function().block())

		return node_id

	# Visit a parse tree produced by CompiscriptParser#varDecl.
	def visitVarDecl(self, ctx: CompiscriptParser.VarDeclContext):
		var_name = ctx.IDENTIFIER().getText()

		# Intentar obtener el tipo de la variable desde el contexto
		var_type = "unknown"
		if ctx.getChild(0):  # Suponiendo que el tipo es el primer hijo
			var_type = ctx.getChild(0).getText()

		# Verificar si la variable ya está declarada en el ámbito global
		if var_name in self.global_variables:
			raise Exception(f"Error: Variable '{var_name}' ya declarada en el ámbito global.")
		else:
			self.global_variables[var_name] = None

		# Almacenar la información en la tabla de símbolos
		property = Symbol_Property()
		property.id = var_name
		property.scope = "global"
		property.value = None

		if ctx.expression():
			expression_value = self.visit(ctx.expression())
			property.value = expression_value

		# Añadir el símbolo a la tabla de variables
		self.table_variables.add(property)

		# Construir el AST
		node_id = self.nodeTree(ctx)

		# Visitar la expresión asociada si existe
		if ctx.expression():
			expression_value = self.visit(ctx.expression())
			print(expression_value)

		return node_id

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
		return self.visitChildren(ctx)

	def visitAssignment(self, ctx:CompiscriptParser.AssignmentContext):
		return self.visitChildren(ctx)

	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		return self.visitChildren(ctx)

	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		return self.visitChildren(ctx)

	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		return self.visitChildren(ctx)

	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		return self.visitChildren(ctx)

	def visitTerm(self, ctx:CompiscriptParser.TermContext):
		if ctx.getChildCount() == 1:
			return self.visit(ctx.factor(0))  # Retorna el único factor si no hay operación

		left = self.visit(ctx.factor(0))
		right = self.visit(ctx.factor(1))

		if ctx.getChild(1).getText() == '+':
			return left + right
		elif ctx.getChild(1).getText() == '-':
			return left - right

	def visitFactor(self, ctx:CompiscriptParser.FactorContext):
		if ctx.getChildCount() == 1:
			return self.visit(ctx.unary(0))  # Retorna el único unary si no hay operación

		left = self.visit(ctx.unary(0))
		right = self.visit(ctx.unary(1))

		if ctx.getChild(1).getText() == '*':
			return left * right
		elif ctx.getChild(1).getText() == '/':
			return left / right
		elif ctx.getChild(1).getText() == '%':
			return left % right

	def visitArray(self, ctx:CompiscriptParser.ArrayContext):
		return self.visitChildren(ctx)

	def visitInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
		return self.visitChildren(ctx)

	def visitUnary(self, ctx:CompiscriptParser.UnaryContext):
		return self.visitChildren(ctx)

	def visitCall(self, ctx:CompiscriptParser.CallContext):
		name = str(ctx.IDENTIFIER())
		return self.visitChildren(ctx)

	def visitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
		if ctx.NUMBER():
			# Retorna el valor numérico
			return int(ctx.NUMBER().getText())
		elif ctx.IDENTIFIER():
			# Retorna el valor de la variable si existe
			var_name = ctx.IDENTIFIER().getText()
			if self.local_variables and var_name in self.local_variables:
				return self.local_variables[var_name]
			elif var_name in self.global_variables:
				return self.global_variables[var_name]
			else:
				raise Exception(f"Error: Variable '{var_name}' no declarada.")
		elif ctx.STRING():
			return ctx.STRING().getText().strip('"')
		elif ctx.getText() == "true":
			return True
		elif ctx.getText() == "false":
			return False
		elif ctx.getText() == "nil":
			return None

	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		return self.visitChildren(ctx)

	def visitParameters(self, ctx:CompiscriptParser.ParametersContext):
		return self.visitChildren(ctx)

	def visitArguments(self, ctx:CompiscriptParser.ArgumentsContext):
		return self.visitChildren(ctx)

	def __init__(self, log: QTextBrowser, table_functions: Symbol_Table, table_variables: Symbol_Table, table_classes: Symbol_Table, parser: CompiscriptParser):
		super().__init__()
		self.counter = 1
		self.parser = parser
		self.graph = Digraph()
		self.log = log
		self.table_functions = table_functions
		self.table_variables = table_variables
		self.table_classes = table_classes

		self.table_functions: Dict[str, ParserRuleContext] = {}
		self.global_variables: Dict[str, ParserRuleContext] = {}
		self.local_variables: Dict[str, ParserRuleContext] = {}

	def nodeTree(self, ctx: Union[ParserRuleContext]):
		node_id = f"node{self.counter}"
		self.counter += 1

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