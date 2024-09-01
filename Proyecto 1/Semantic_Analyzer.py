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
		self.variables_control = {}
		self.global_variables = {}
		self.current_scope = ""
		self.variables_scope = {}

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

	
	def visitVarDecl(self, ctx: CompiscriptParser.VarDeclContext):
		var_name = ctx.IDENTIFIER().getText()

		# Try to get the variable's type from the context
		var_type = "unknown"
		var_value = None
		if ctx.expression():
			var_value = self.visit(ctx.expression())
			if isinstance(var_value, bool):
				var_type = "boolean"
			elif isinstance(var_value, str):
				var_type = "char" if len(var_value) == 1 else "string"
			elif isinstance(var_value, int):
				var_type = "int"
			elif isinstance(var_value, float):
				var_type = "float"

		# Determine if we are in a local or global scope
		is_local_scope = len(self.table_variables.scopes) > 1
		current_scope_id = self.current_scope if is_local_scope else "global_0"

		# Initialize the scope in variables_scope if it doesn't exist
		if current_scope_id not in self.variables_scope:
			self.variables_scope[current_scope_id] = {}

		# Check if the variable is already declared in the current scope
		if var_name in self.variables_scope[current_scope_id]:
			raise Exception(f"Error: Variable '{var_name}' already declared in scope '{current_scope_id}'.")

		# Store the variable in the current scope's dictionary in variables_scope
		self.variables_scope[current_scope_id][var_name] = {"type": var_type, "value": var_value}

		print(f"variables_scope: {self.variables_scope}")

		# Create the variable's property and add it to the scope and symbol table
		property = Symbol_Property()
		property.id = var_name
		property.scope = "local" if is_local_scope else "global"
		property.value = var_value
		property.type = var_type

		# Add the variable to the table of variables in the current scope
		self.table_variables.add_and_scope(property)

		# If it's a global variable, also add it to the global dictionary
		if not is_local_scope:
			self.global_variables[var_name] = var_value

		# Construct the AST node
		node_id = self.nodeTree(ctx)

		# Visit the associated expression if it exists
		if ctx.expression():
			expression_value = self.visit(ctx.expression())
			print(f"Value of the expression assigned to {var_name}: {expression_value}")

		return node_id

	# Example of visiting a new scope (like a block or function)
	def enterNewScope(self, scope_id: str):
		# When entering a new scope, set the current scope
		self.current_scope = scope_id
		if scope_id not in self.variables_scope:
			self.variables_scope[scope_id] = {}
		print(f"Entered new scope: {scope_id}")

	def exitScope(self):
		# When exiting the scope, pop the scope stack and return to the parent scope
		print(f"Exiting scope: {self.current_scope}")
		self.current_scope = "global_0" if len(self.table_variables.scopes) == 1 else self.table_variables.scopes[-1].id
		print(f"Returned to scope: {self.current_scope}")


	def visitStatement(self, ctx:CompiscriptParser.StatementContext):
		return self.visitChildren(ctx)


	def visitExprStmt(self, ctx:CompiscriptParser.ExprStmtContext):
		return self.visitChildren(ctx)


	def visitForStmt(self, ctx: CompiscriptParser.ForStmtContext):
		# Crear un nuevo scope para el ciclo 'for'
		self.table_variables.enter_scope()
		self.current_scope = self.table_variables.scopes[-1].id
		print(f"Entering 'for' scope: {self.current_scope}")

		# 1. Inicialización: Ejecutar la inicialización del ciclo, si existe
		if ctx.varDecl():
			self.visit(ctx.varDecl())
		elif ctx.exprStmt():
			self.visit(ctx.exprStmt())
		
		# 2. Condición: Evaluar la condición del 'for' si existe
		condition_value = True
		if ctx.expression(0):
			condition_value = self.visit(ctx.expression(0))
			
			# Verificar que la condición sea de tipo booleano
			if not isinstance(condition_value, bool):
				raise TypeError(f"Error: La condición en la sentencia 'for' debe ser booleana, pero se obtuvo {type(condition_value).__name__}.")

		# 3. Ciclo 'for': Continuar mientras la condición sea verdadera
		while condition_value:
			# 4. Ejecutar el cuerpo del ciclo
			self.visit(ctx.statement())

			# 5. Actualización: Ejecutar la actualización del ciclo, si existe
			if ctx.expression(1):
				self.visit(ctx.expression(1))

			# Re-evaluar la condición después de cada iteración si existe
			if ctx.expression(0):
				condition_value = self.visit(ctx.expression(0))

		# Salir del scope del bloque 'for'
		print(f"Exiting 'for' scope: {self.current_scope}")
		self.table_variables.exit_scope()
		self.current_scope = self.table_variables.scopes[-1].id if self.table_variables.scopes else "global_0"

		return None


	def visitIfStmt(self, ctx: CompiscriptParser.IfStmtContext):
		# Evaluar la condición del 'if'
		condition_value = self.visit(ctx.expression())
		text = ctx.getText()
		print(f"condicion valor: {condition_value}")
		
		# Verificar que la condición sea de tipo booleano
		if not isinstance(condition_value, bool):
			raise TypeError(f"Error: La condición en la sentencia 'if' debe ser booleana, pero se obtuvo {type(condition_value).__name__}.")
				# Obtener la info del nodo
		# En caso de tener un print, procesarlo
		if "if" in text:
			# Verificar si la función 'print' ya ha sido declarada
			if "if" not in self.declared_functions:
				# Si 'print' no está declarada, agregarla a la tabla de funciones
				print_function = Symbol_Property()
				print_function.id = "if"
				print_function.parameters = "boolean"  # 'any', ya que acepta cualquier cosa
				print_function.return_type = "void"
				
				# Agregar a la tabla de funciones
				self.table_functions.add(print_function)

				# Marcar 'print' como declarada
				self.declared_functions.add("if")

		
		# Crear un nuevo scope para el bloque 'if'
		self.table_variables.enter_scope()
		self.current_scope = self.table_variables.scopes[-1].id
		print(f"Entering 'if' scope: {self.current_scope}")
		
		# Si la condición es True, ejecutar el bloque 'if'
		if condition_value:
			self.visit(ctx.statement(0))
		
		# Salir del scope del bloque 'if'
		print(f"Exiting 'if' scope: {self.current_scope}")
		self.table_variables.exit_scope()
		self.current_scope = self.table_variables.scopes[-1].id if self.table_variables.scopes else "global_0"
		

		if ctx.getChildCount() > 5:  # 'if' '(' expression ')' statement 'else' statement
			# Crear un nuevo scope para el bloque 'else'
			self.table_variables.enter_scope()
			# Crear un nuevo scope para el bloque 'else'
			self.current_scope = self.table_variables.scopes[-1].id
			print(f"Entering 'else' scope: {self.current_scope}")
			
			# Evaluar el bloque 'else'
			else_block = ctx.statement(1)
			else_block_result = self.visit(else_block)
			
			# Salir del scope del bloque 'else'
			print(f"Exiting 'else' scope: {self.current_scope}")
			# Salir del scope del bloque 'else'
			self.table_variables.exit_scope()

			# Si la condición es False, ejecutar el bloque 'else'
			if not condition_value:
				self.visit(ctx.statement(1))
			
			self.current_scope = self.table_variables.scopes[-1].id if self.table_variables.scopes else "global_0"
		
				# Verificar si existe un bloque 'else'
		
		return None  # No hay un resultado específico para la evaluación de 'if' o 'else'

		# return self.visitChildren(ctx)


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
		# Evaluar la condición del 'while'
		condition_value = self.visit(ctx.expression())
		text = ctx.getText()
		print(f"condición valor: {condition_value}")
		
		# Verificar que la condición sea de tipo booleano
		if not isinstance(condition_value, bool):
			raise TypeError(f"Error: La condición en la sentencia 'while' debe ser booleana, pero se obtuvo {type(condition_value).__name__}.")
		
		# Verificar si la función 'while' ya ha sido declarada (este bloque parece innecesario pero lo dejo por si lo necesitas)
		if "while" in text:
			if "while" not in self.declared_functions:
				while_function = Symbol_Property()
				while_function.id = "while"
				while_function.parameters = "boolean"  # 'boolean', ya que la condición debe ser booleana
				while_function.return_type = "void"
				
				# Agregar a la tabla de funciones
				self.table_functions.add(while_function)

				# Marcar 'while' como declarada
				self.declared_functions.add("while")
		
		# Crear un nuevo scope para el bloque 'while'
		self.table_variables.enter_scope()
		self.current_scope = self.table_variables.scopes[-1].id
		print(f"Entering 'while' scope: {self.current_scope}")
		
		# Mientras la condición sea True, ejecutar el bloque 'while'
		# while condition_value:
		# 	# Iterar sobre todas las declaraciones dentro del bloque 'while'
		# 	for stmt in ctx.statement():
		# 		self.visit(stmt)
			
			# Re-evaluar la condición después de cada iteración
			# condition_value = self.visit(ctx.expression())
		
		# Salir del scope del bloque 'while'
		print(f"Exiting 'while' scope: {self.current_scope}")
		self.table_variables.exit_scope()
		self.current_scope = self.table_variables.scopes[-1].id if self.table_variables.scopes else "global_0"
		
		return None


	def visitBlock(self, ctx: CompiscriptParser.BlockContext):
		# Entrar en un nuevo scope, lo que automáticamente incrementa el contador de scopes
		self.table_variables.enter_scope()
		# Imprimir el identificador del nuevo scope para debugging
		print(f"Entering scope: {self.table_variables.scopes[-1].id}")
		self.current_scope = self.table_variables.scopes[-1].id
		# Evaluar todas las declaraciones dentro del bloque
		result = None
		for declaration in ctx.declaration():
			result = self.visit(declaration)

		# Salir del scope al final del bloque, lo que también elimina el scope del stack
		print(f"Exiting scope: {self.table_variables.scopes[-1].id}")
		self.table_variables.exit_scope()
		self.current_scope = "global_0"
		return result


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
			print(f"Valor inicial para or: {result}")

			for i in range(1, ctx.getChildCount(), 2):
				operator = ctx.getChild(i).getText()
				right = self.visit(ctx.getChild(i + 1))
				print(f"Evaluando: {result} or {right}")
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
			print(f"Valor inicial para and: {result}")
			
			# Recorremos los otros términos en la expresión
			for i in range(2, ctx.getChildCount(), 2):  # Saltamos el operador 'and' para obtener el siguiente término
				right = self.visit(ctx.getChild(i))
				print(f"Evaluando: {result} and {right}")
				result = result and right

				# Si result es False, podemos devolverlo inmediatamente
				if not result:
					return False

			return result
		else:
			return self.visitChildren(ctx)

	
	def visitEquality(self, ctx:CompiscriptParser.EqualityContext):
		text = ctx.getText()
		data = []
		left, right = "", ""
		if "==" in text:
			data = text.split("==")
			print(f"Datos después del split por '==': {data}")
			data = self.depuracion_elemntos_con_detalles_extra(data)
			if data[0].lower() == "true" or data[0].lower() == "false":  # Verifica correctamente los booleanos
				left = data[0].lower() == "true"
				right = data[1].lower() == "true"
			else:
				left = data[0]
				right = data[1]
				self.validacion_numeros_mediante_casteo([left, right])
			return left == right
		elif "!=" in text:
			data = text.split("!=")
			print(f"Datos después del split por '!=': {data}")
			data = self.depuracion_elemntos_con_detalles_extra(data)
			if data[0].lower() == "true" or data[0].lower() == "false":
				left = data[0].lower() == "true"
				right = data[1].lower() == "true"
			else:
				left = data[0]
				right = data[1]
				self.validacion_numeros_mediante_casteo([left, right])
			return left != right
		else:
			return self.visitChildren(ctx)


	def visitComparison(self, ctx:CompiscriptParser.ComparisonContext):
		text = ctx.getText()
		data = []
		left, right = "", ""

		if "<=" in text:
			data = text.split("<=")
			# print(f"Datos después de split por '<': {data}")
			data = self.depuracion_elemntos_con_detalles_extra(data)
			self.validacion_numeros_mediante_casteo(data)
			left = data[0]
			right = data[1]
			return left < right
		
		elif ">=" in text:
			data = text.split(">=")
			# print(f"Datos después de split por '<=': {data}")
			data = self.depuracion_elemntos_con_detalles_extra(data)
			self.validacion_numeros_mediante_casteo(data)
			left = data[0]
			right = data[1]
			return left[0] <= right[0]
		
		elif ">" in text:
			data = text.split(">")
			# print(f"Datos después de split por '>': {data}")
			data = self.depuracion_elemntos_con_detalles_extra(data)
			self.validacion_numeros_mediante_casteo(data)
			left = data[0]
			right = data[1]
			return left > right
		
		elif "<" in text:
			# print(f"Datos después de split por '>=': {data}")
			data = text.split("<")
			data = self.depuracion_elemntos_con_detalles_extra(data)
			self.validacion_numeros_mediante_casteo(data)
			left = data[0]
			right = data[1]
			return left >= right
		else:
			return self.visitChildren(ctx)
		

	def validacion_numeros_mediante_casteo(self, data):
		# print(f"Datos antes de depurar: {data}")
		try:
			int(data[0].strip())
			int(data[1].strip())
		except TypeError:
			raise TypeError(f"No se pueden comparar valores de tipos diferente: {type(data[0]).__name__} y {type(data[1]).__name__}")
		# print(f"Datos después de depurar: {data}")


	def depuracion_elemntos_con_detalles_extra(self, data):
		data[0] = data[0].strip('()')
		data[1] = data[1].strip('()')
		print(f"Datos después de eliminar paréntesis: {data}")
		return data
	

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