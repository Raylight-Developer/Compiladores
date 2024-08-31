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
		self.declared_functions: Set[str] = set()
	
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
		var_value = None
		if ctx.expression():
			var_value = self.visit(ctx.expression())
			if isinstance(var_value, bool):
				var_type = "boolean"
			elif isinstance(var_value, str):
				if len(var_value) == 1:
					var_type = "char"
				else:
					var_type = "string"
			elif isinstance(var_value, int):
				var_type = "int"
			elif isinstance(var_value, float):
				var_type = "float"

		# Verificar si la variable ya está declarada en el ámbito global
		if var_name in self.global_variables:
			raise Exception(f"Error: Variable '{var_name}' ya declarada en el ámbito global.")
		else:
			self.global_variables[var_name] = None

		# Almacenar la información en la tabla de símbolos
		property = Symbol_Property()
		property.id = var_name
		property.scope = "global"
		property.value = var_value
		property.type = var_type

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


	def visitPrintStmt(self, ctx: CompiscriptParser.PrintStmtContext):
		# Obtener la info del nodo
		text = ctx.getText()
		# En caso de tener un print, procesarlo
		if "print" in text:
			# Verificar si la función 'print' ya ha sido declarada
			if "print" not in self.declared_functions:
				# Si 'print' no está declarada, agregarla a la tabla de funciones
				print_function = Symbol_Property()
				print_function.id = "print"
				print_function.parameters = "any"  # 'any', ya que acepta cualquier cosa
				print_function.return_type = "void"
				
				# Agregar a la tabla de funciones
				self.table_functions.add(print_function)

				# Marcar 'print' como declarada
				self.declared_functions.add("print")

			# Obtener y visitar la expresión dentro de la instrucción print
			expression_value = self.visit(ctx.expression())

			# Imprimir la expresión (esto es solo un ejemplo de cómo podrías manejarlo)
			print(f'Print statement: {expression_value}')

			return None
		else:
			# Delegar al siguiente metodo
			return self.visitChildren(ctx)


	def visitReturnStmt(self, ctx:CompiscriptParser.ReturnStmtContext):
		return self.visitChildren(ctx)


	def visitWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext):
		return self.visitChildren(ctx)


	def visitBlock(self, ctx:CompiscriptParser.BlockContext):
		return self.visitChildren(ctx)


	def visitFunAnon(self, ctx:CompiscriptParser.FunAnonContext):
		return self.visitChildren(ctx)


	def visitExpression(self, ctx: CompiscriptParser.ExpressionContext):
		# Verificamos si la expresión tiene múltiples términos (por ejemplo, con operadores lógicos o aritméticos)
		if ctx.getChildCount() == 1:
			return self.visit(ctx.getChild(0))

		left = self.visit(ctx.getChild(0))
		operator = ctx.getChild(1).getText()
		right = self.visit(ctx.getChild(2))

		# Si alguno de los operandos es None, algo salió mal en el procesamiento anterior
		if left is None or right is None:
			raise Exception("Error en la evaluación de la expresión: uno de los operandos es None.")

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
			raise Exception(f"Operador desconocido: {operator}")


	def visitAssignment(self, ctx:CompiscriptParser.AssignmentContext):
		return self.visitChildren(ctx)


	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		text = ctx.getText()
		if "or" in text:
			result = self.visit(ctx.getChild(0))

			# Recorremos los otros términos en la expresión
			for i in range(1, ctx.getChildCount(), 2):
				operator = ctx.getChild(i).getText()
				right = self.visit(ctx.getChild(i + 1))

				# Evaluamos el operador `or`
				if operator == 'or':
					result = result or right

			return result
		else:
			return self.visitChildren(ctx)


	def visitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
		text = ctx.getText()
		if 'and' in text:
			# Empezamos evaluando el primer término
			result = self.visit(ctx.getChild(0))

			# Recorremos los otros términos en la expresión
			for i in range(2, ctx.getChildCount(), 2):  # Saltamos el operador 'and' para obtener el siguiente término
				right = self.visit(ctx.getChild(i))

				# Evaluamos la expresión utilizando el operador `and`
				result = result and right

				# Si result es False, podemos devolverlo inmediatamente
				if not result:
					return False

			return result
		else:
			return self.visitChildren(ctx)
	
	
	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		text = ctx.getText()
		if "==" in text:
			data = text.split("==")
			left = data[0]
			right = data[1]
			return left == right
		elif "!=" in text:
			data = text.split("!=")
			left = data[0]
			right = data[1]
			return left != right
		else:
			return self.visitChildren(ctx)


	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		text = ctx.getText()
		data = []
		left, right = "", ""
		if "<" in text:
			data = text.split("<")
			left = data[0]
			right = data[1]
			return left < right
		elif "<=" in text:
			data = text.split("<=")
			left = data[0]
			right = data[1]
			return left <= right
		elif ">" in text:
			data = text.split(">")
			left = data[0]
			right = data[1]
			return left > right
		elif ">=" in text:
			data = text.split(">=")
			left = data[0]
			right = data[1]
			return left >= right
		else:
			return self.visitChildren(ctx)
		

	def visitTerm(self, ctx: CompiscriptParser.TermContext):
		if ctx.getChildCount() == 1:
			return self.visit(ctx.factor(0))  # Retorna el único factor si no hay operación

		left = self.visit(ctx.factor(0))
		right = self.visit(ctx.factor(1))

		# Si alguno de los operandos es None, algo salió mal en el procesamiento anterior
		if left is None or right is None:
			raise Exception("Error en la evaluación de la expresión: uno de los operandos es None.")

		if ctx.getChild(1).getText() == '+':
			return left + right
		elif ctx.getChild(1).getText() == '-':
			return left - right


	def visitFactor(self, ctx: CompiscriptParser.FactorContext):
		if ctx.getChildCount() == 1:
			return self.visit(ctx.unary(0))  # Retorna el único unary si no hay operación

		left = self.visit(ctx.unary(0))
		right = self.visit(ctx.unary(1))

		# Si alguno de los operandos es None, algo salió mal en el procesamiento anterior
		if left is None or right is None:
			raise Exception("Error en la evaluación de la expresión: uno de los operandos es None.")

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


	def visitUnary(self, ctx: CompiscriptParser.UnaryContext):
		if ctx.getChildCount() == 2:
			# Caso donde tenemos un operador unario (como '-' o '!')
			operator = ctx.getChild(0).getText()
			operand = self.visit(ctx.getChild(1))  # El operando es el siguiente hijo
			if operator == '-':
				return -operand
			elif operator == '!':
				return not operand
			# Puedes manejar otros operadores unarios aquí si existen en tu lenguaje
		else:
			# Caso donde no hay operador unario, simplemente se delega al siguiente nodo
			return self.visit(ctx.getChild(0))  # El primer hijo debe ser el siguiente nivel de expresión (por ejemplo, `primary`)


	def visitCall(self, ctx:CompiscriptParser.CallContext):
		name = str(ctx.IDENTIFIER())
		return self.visitChildren(ctx)

	def visitPrimary(self, ctx: CompiscriptParser.PrimaryContext):
		if ctx.NUMBER():
			text = ctx.NUMBER().getText()
			if '.' in text:
				return float(text) # Inferred as float
			else:
				return int(text)  # Inferred as int
		elif ctx.STRING():
			str_value = ctx.STRING().getText().strip('"')
			return str_value
		elif ctx.IDENTIFIER():
			var_name = ctx.IDENTIFIER().getText()
			if var_name in self.local_variables:
				return self.local_variables[var_name], "unknown"  # Unknown until evaluated
			elif var_name in self.global_variables:
				return self.global_variables[var_name], "unknown"
			else:
				raise Exception(f"Error: Variable '{var_name}' not declared.")
		elif ctx.getText() == "true":
			return True
		elif ctx.getText() == "false":
			return False
		elif ctx.getText() == "nil":
			return None
		elif ctx.expression():
			return self.visit(ctx.expression())  # Delegate to expression handling


	def visitFunction(self, ctx:CompiscriptParser.FunctionContext):
		return self.visitChildren(ctx)


	def visitParameters(self, ctx:CompiscriptParser.ParametersContext):
		return self.visitChildren(ctx)


	def visitArguments(self, ctx:CompiscriptParser.ArgumentsContext):
		return self.visitChildren(ctx)


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