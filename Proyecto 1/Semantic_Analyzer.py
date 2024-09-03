from CompiscriptVisitor import CompiscriptVisitor
from CompiscriptParser import CompiscriptParser
from CompiscriptLexer import CompiscriptLexer
from Symbol_Table import Symbol_Table, Symbol_Property
from Logger import *
import re

from Include import *

class Semantic_Analyzer(CompiscriptVisitor):
	def __init__(self, log: Logger, table_functions: Symbol_Table, table_variables: Symbol_Table, table_classes: Symbol_Table, parser: CompiscriptParser):
		super().__init__()
		self.counter = 1
		self.inside_loop = False
		self.inside_block_fun_if = False
		self.parser = parser
		self.graph = Digraph()
		self.log = log
		self.table_functions = table_functions
		self.table_variables = table_variables
		self.table_classes = table_classes

		self.current_scope = "global_0"
		self.variables_scope = {}

		self.global_variables: Dict[str, ParserRuleContext] = {}
		self.local_variables: Dict[str, ParserRuleContext] = {}
		self.declared_functions: Set[str] = set()
		# self.functions_parameters = Set[str] = set()

	def visitProgram(self, ctx:CompiscriptParser.ProgramContext):
		return self.visitChildren(ctx)


	def visitDeclaration(self, ctx:CompiscriptParser.DeclarationContext):
		return self.visitChildren(ctx)


	def visitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
		return self.visitChildren(ctx)


	def declare_variable(self, name: str, ctx: ParserRuleContext):
		"""Declare a variable in the current scope."""
		if name in self.local_variables:
			self.log.debug(f"Variable '{name}' is already declared in the current scope.")
		self.local_variables[name] = ctx

	def validacion_numeros_mediante_casteo(self, data):
		# self.log.debug(f"Datos antes de depurar: {data}")
		try:
			int(data[0].strip())
			int(data[1].strip())
		except TypeError:
			raise TypeError(f"No se pueden comparar valores de tipos diferente: {type(data[0]).__name__} y {type(data[1]).__name__}")
		# self.log.debug(f"Datos después de depurar: {data}")


	def visitFunDecl(self, ctx: CompiscriptParser.FunDeclContext):
		fun_name = ctx.function().IDENTIFIER().getText()
		#self.log.debug(f"TEXTO: {ctx.getText()} -- {fun_name}")
		# fun_declard = ctx.function().call()
		# Verifica si la función ya está declarada
		if fun_name in self.declared_functions:
			raise Exception(f"Error: Función '{fun_name}' ya declarada.")
		# Obtencion de los parametros
		
		try:
			parametros = [param.getText() for param in ctx.function().parameters().IDENTIFIER()]
		except: # No tiene Parametros
			parametros = []
		# self.log.debug(f"PARAMETAIOSJDF {parametros}")
		print(f"PAMAREOSIAF: {parametros}")
		params = ctx.function().parameters()
		
		print(f"PARAMETROS: {params}")
		if params:
			for param in params.IDENTIFIER():
				self.declare_variable(param.getText(), param)
		# Registrar la función
		self.declared_functions.add(fun_name)


		# Crear los datos del símbolo de la función
		symbol_data = Symbol_Property()
		symbol_data.id = fun_name                      # ID
		symbol_data.type = "function"                  # Tipo
		symbol_data.parameters = ", ".join(parametros)
		symbol_data.return_type = "void"
		# Agregar a la tabla de funciones
		self.table_functions.add(symbol_data)


		# Delegar al siguiente método (por si hay más cosas que procesar dentro de la función)
		return self.visitChildren(ctx)

		
	def visitVarDecl(self, ctx: CompiscriptParser.VarDeclContext):
		var_name = ctx.IDENTIFIER().getText()
		var_declartion = ctx.getText()
		arreglo = []
		var_type = "unknown"
		var_value = None

		# para capturar el contenido del arreglo
		patron_array = r'\[([^\]]+)\]'
		# Buscar la coincidencia en la cadena
		coincidencia_array = re.search(patron_array, var_declartion)
		if coincidencia_array:
			# Extraer el contenido del arreglo y dividirlo en elementos
			elementos = coincidencia_array.group(1).split(',')
			# Convertir los elementos a enteros
			arreglo = [elemento for elemento in elementos]
			var_type = "array"
	
		# Determina si estamos en un scope local o global
		is_local_scope = len(self.table_variables.scopes) > 1
		current_scope_id = self.current_scope if is_local_scope else "global_0"
		
		# self.log.debug(f"ATENTO: {current_scope_id, self.current_scope, is_local_scope}")
		if current_scope_id == '':
			current_scope_id = "global_0"

		# Inicializa el scope en variables_scope si no existe
		if current_scope_id not in self.variables_scope:
			self.variables_scope[current_scope_id] = {}

		# Verifica si la variable ya está declarada en el scope actual
		if var_name in self.variables_scope[current_scope_id] :
			raise Exception(f"Error: Variable '{var_name}' ya declarada en el scope '{current_scope_id}'.")

		# Try to get the variable's type from the context
		
		if ctx.expression():
			if var_type == "unknown":
				var_value = self.visit(ctx.expression())
				var_type = self.determine_type(var_value)
			elif var_type == "array":
				pass

		if var_type == "array":
			# Guarda la variable en el diccionario del scope actual en variables_scope
			self.variables_scope[current_scope_id][var_name] = {"type": var_type, "value": arreglo}
		else:
			# Guarda la variable en el diccionario del scope actual en variables_scope
			self.variables_scope[current_scope_id][var_name] = {"type": var_type, "value": var_value}


		self.log.debug(f"variables_scope: {self.variables_scope}")

		property = Symbol_Property()
		# Enviarlo en tipo array
		if var_type == "array":
			
			property.id = var_name
			property.scope = "local" if is_local_scope else "global"
			property.value = arreglo
			property.type = var_type
			# self.log.debug(f"DEBERIA ENVIARSE {property.value}")
		else:
		# Crea la propiedad de la variable y la agrega a la tabla de símbolos
			property.id = var_name
			property.scope = "local" if is_local_scope else "global"
			property.value = var_value
			property.type = var_type

		# Agrega la variable a la tabla de variables en el scope actual
		self.table_variables.add_and_scope(property)

		# Si es una variable global, también se agrega al diccionario global
		if not is_local_scope:
			self.global_variables[var_name] = var_value

		# Construye el nodo del AST
		node_id = self.nodeTree(ctx)

		# Visita la expresión asociada si existe
		# if ctx.expression():
		# 	expression_value = self.visit(ctx.expression())
		# 	self.log.debug(f"Value of the expression assigned to {var_name}: {expression_value}")

		return node_id


	def determine_type(self, value):
		if isinstance(value, bool):
			return "boolean"
		elif isinstance(value, str):
			return "char" if len(value) == 1 else "string"
		elif isinstance(value, int):
			return "int"
		elif isinstance(value, float):
			return "float"
		else:
			return "unknown"

	# Example of visiting a new scope (like a block or function)
	def enterNewScope(self, scope_id: str):
		# When entering a new scope, set the current scope
		self.current_scope = scope_id
		if scope_id not in self.variables_scope:
			self.variables_scope[scope_id] = {}
		self.log.debug(f"Entered new scope: {scope_id}")


	def exitScope(self):
		# When exiting the scope, pop the scope stack and return to the parent scope
		self.log.debug(f"Exiting scope: {self.current_scope}")
		self.current_scope = "global_0" if len(self.table_variables.scopes) == 1 else self.table_variables.scopes[-1].id
		self.log.debug(f"Returned to scope: {self.current_scope}")


	def visitStatement(self, ctx:CompiscriptParser.StatementContext):
		text = ctx.getText().strip()
		test = ctx.getText()
		# self.log.debug(f"HAY BREAK {text}")

		# if test[0] == "{" and test[1] == "}":
		# 	raise Exception("Error: La declaracion if no tiene cuerpo")
		
		# Detectar 'break'
		if text == "break;":
			if not self.inside_loop:
				raise Exception("Error: La declaracion 'break' no esta dentro de un bucle.")
			self.log.debug("Declaracion Break encontrada, saliendo del bucle.")
			return "break"  # Indica al bucle que debe terminar
		
		# Detectar 'continue'
		elif text == "continue;":
			if not self.inside_loop:
				raise Exception("Error: La declaracion 'continue' no esta dentro de un bucle.")
			self.log.debug("Declaracion Continue encontrada, continuando el bucle.")
			return "continue"  # Indica al bucle que debe saltar a la siguiente iteración
		
		elif text == "return":
			if not self.inside_block_fun_if:
				raise Exception("Error: La declaracion 'return' return esta fuera de un bloque.")
		
		# Para otras sentencias, delegar al visitor correspondiente
		return self.visitChildren(ctx)


	def visitExprStmt(self, ctx: CompiscriptParser.ExprStmtContext):	
		# Si no es una llamada, delega a la visita de los hijos (otras expresiones)
		return self.visitChildren(ctx)


	def visitForStmt(self, ctx: CompiscriptParser.ForStmtContext):
		# Entrar en un nuevo scope
		self.table_variables.enter_scope()
		new_scope_id = self.table_variables.scopes[-1].id
		self.current_scope = new_scope_id
		self.log.debug(f"Entering 'for' scope: {self.current_scope}")

		# Inicialización, condición y actualización
		if ctx.varDecl():  # Manejo de la declaración de variable dentro del for
			self.visitVarDecl(ctx.varDecl())

		

		# Evaluar la condición
		condition_value = self.visit(ctx.expression(0)) if ctx.expression(0) else True
		self.log.debug(f"CONDICION VALUE: {condition_value}")
		# while condition_value:
		# 	# Ejecutar las oraciones dentro del for
		# 	for stmt in ctx.statement():
		# 		result = self.visit(stmt)
		# 		if result == "break":
		# 			break
		# 		elif result == "continue":
		# 			break  # En Python, continue se maneja rompiendo el loop for stmt y continuando el loop externo
			
		# 	# Actualización de la expresión dentro del for (i++)
		# 	if ctx.expression(1):
		# 		self.visit(ctx.expression(1))

		# 	# Re-evaluar la condición
		# 	condition_value = self.visit(ctx.expression(0)) if ctx.expression(0) else True

		# Salir del scope después de terminar el bucle
		self.log.debug(f"Exiting 'for' scope: {self.current_scope}")
		self.table_variables.exit_scope()
		self.current_scope = self.table_variables.scopes[-1].id if self.table_variables.scopes else "global_0"

		return None


	def visitIfStmt(self, ctx: CompiscriptParser.IfStmtContext):
		# Evaluar la condición del 'if'
		condition_value = self.visit(ctx.expression())
		text = ctx.getText()
		self.log.debug(f"condicion valor: {condition_value}")
		self.log.debug(f"CONDICION IF: {condition_value}")
		if isinstance(condition_value, tuple):
			if not isinstance(condition_value[0], bool):
				raise TypeError(f"Error: La condición en 'if' debe ser booleana, pero se obtuvo {type(condition_value).__name__}.")
		#elif not isinstance(condition_value, bool):
		#	raise TypeError(f"Error: La condición en 'if' debe ser booleana, pero se obtuvo {type(condition_value).__name__}.")
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
		

		self.log.debug(f"Entering 'if' scope: {self.current_scope}")
		
		# Si la condición es True, ejecutar el bloque 'if'
		if condition_value:
			self.visit(ctx.statement(0))
		
		# Salir del scope del bloque 'if'
		self.log.debug(f"Exiting 'if' scope: {self.current_scope}")
		self.table_variables.exit_scope()
		self.current_scope = self.table_variables.scopes[-1].id if self.table_variables.scopes else "global_0"
		

		if ctx.getChildCount() > 5:  # 'if' '(' expression ')' statement 'else' statement
			# Crear un nuevo scope para el bloque 'else'
			self.table_variables.enter_scope()
			# Crear un nuevo scope para el bloque 'else'
			self.current_scope = self.table_variables.scopes[-1].id
			self.log.debug(f"Entering 'else' scope: {self.current_scope}")
			
			# Evaluar el bloque 'else'
			else_block = ctx.statement(1)
			else_block_result = self.visit(else_block)
			
			# Salir del scope del bloque 'else'
			self.log.debug(f"Exiting 'else' scope: {self.current_scope}")
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
		text = ctx.getText()
		if "print" in text:
			if "print" not in self.declared_functions:
				print_function = Symbol_Property()
				print_function.id = "print"
				print_function.parameters = "any"
				print_function.return_type = "void"
				# Agregarlo a la tabla de funciones
				self.table_functions.add(print_function)
				# Marcar 'print' como declarada
				self.declared_functions.add("print")

			# Obtener la expresión y evaluarla
			expression_value = self.visit(ctx.expression())
			self.log.debug(f'Evaluated expression: {expression_value}')

			# Aquí deberías recibir el valor real de "hola" en lugar de 'global_0'
			self.log.debug(f'Print statement: {expression_value}')

			return None
		else:
			return self.visitChildren(ctx)


	def visitReturnStmt(self, ctx:CompiscriptParser.ReturnStmtContext):
		return self.visitChildren(ctx)


	def visitWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext):
		# Evaluar la condición del 'while'
		condition_value = self.visit(ctx.expression())
		text = ctx.getText()
		self.log.debug(f"Condición valor: {condition_value}")
		
		self.log.debug(f"CONDICION WHILE: {condition_value}")
		if isinstance(condition_value, tuple):
			if not isinstance(condition_value[0], bool):
				raise TypeError(f"Error: La condición en 'while' debe ser booleana, pero se obtuvo {type(condition_value).__name__}.")
		#elif not isinstance(condition_value, bool):
		#	raise TypeError(f"Error: La condición en 'while' debe ser booleana, pero se obtuvo {type(condition_value).__name__}.")
		
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
		
		self.inside_loop = True
		# Crear un nuevo scope para el bloque 'while'
		self.table_variables.enter_scope()
		self.current_scope = self.table_variables.scopes[-1].id
		self.log.debug(f"Entering 'while' scope: {self.current_scope}")
		
		# Mientras la condición sea True, ejecutar el bloque 'while'
		# while condition_value:
		# 	# Iterar sobre todas las declaraciones dentro del bloque 'while'
		# 	for stmt in ctx.statement():
		# 		self.visit(stmt)
			
			# Re-evaluar la condición después de cada iteración
			# condition_value = self.visit(ctx.expression())
		
		# Salir del scope del bloque 'while'
		self.log.debug(f"Exiting 'while' scope: {self.current_scope}")
		self.table_variables.exit_scope()
		self.current_scope = self.table_variables.scopes[-1].id if self.table_variables.scopes else "global_0"
		self.inside_loop = False
		return None


	def visitBlock(self, ctx: CompiscriptParser.BlockContext):
		# Entrar en un nuevo scope, lo que automáticamente incrementa el contador de scopes
		self.table_variables.enter_scope()
		# Imprimir el identificador del nuevo scope para debugging
		self.log.debug(f"Entering scope: {self.table_variables.scopes[-1].id}")
		self.current_scope = self.table_variables.scopes[-1].id
		# Evaluar todas las declaraciones dentro del bloque
		result = None
		for declaration in ctx.declaration():
			result = self.visit(declaration)

		# Salir del scope al final del bloque, lo que también elimina el scope del stack
		self.log.debug(f"Exiting scope: {self.table_variables.scopes[-1].id}")
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
		""" Este sirve para poder hacer la asignacion de valores"""
		
		if ctx.IDENTIFIER() is not None:
			var_name = str(ctx.IDENTIFIER())
			self.log.debug(f"VARNAME: {var_name}")

			current_scope_vars = self.variables_scope.get(self.current_scope)
			self.log.debug(current_scope_vars)
			try:
				if var_name not in current_scope_vars:
					raise Exception(f"Error: La variable '{var_name}' no esta en el scope actual.")
				if ctx.assignment() is not None:
					# Visita la expresión a la derecha del '='
					value = self.visit(ctx.assignment())
				elif ctx.logic_or() is not None:
					# Visita la lógica "or" si está presente
					value = self.visit(ctx.logic_or())

				current_scope_vars[var_name]['value'] = value
				self.variables_scope[self.current_scope] = current_scope_vars
			except:
				self.log.debug(f"{var_name} Has No Parameters")

		return self.visitChildren(ctx)


	def visitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
		text = ctx.getText()
		if "or" in text:
			result = self.visit(ctx.getChild(0))
			self.log.debug(f"Valor inicial para or: {result}")

			for i in range(1, ctx.getChildCount(), 2):
				operator = ctx.getChild(i).getText()
				right = self.visit(ctx.getChild(i + 1))
				self.log.debug(f"Evaluando: {result} or {right}")
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
			self.log.debug(f"Valor inicial para and: {result}")
			
			# Recorremos los otros términos en la expresión
			for i in range(2, ctx.getChildCount(), 2):  # Saltamos el operador 'and' para obtener el siguiente término
				right = self.visit(ctx.getChild(i))
				self.log.debug(f"Evaluando: {result} and {right}")
				result = result and right

				# Si result es False, podemos devolverlo inmediatamente
				if not result:
					return False
			return result
		else:
			return self.visitChildren(ctx)

	
	def visitEquality(self, ctx: CompiscriptParser.EqualityContext):
		return ctx.getText()
		text = ctx.getText()
		data = []
		if "==" in text:
			data = text.split("==")
			self.log.debug(f"Datos después del split por '==': {data}")
			return self.compare_values(data, "==")
		elif "!=" in text:
			data = text.split("!=")
			self.log.debug(f"Datos después del split por '!=': {data}")
			return self.compare_values(data, "!=")
		else:
			return self.visitChildren(ctx)


	def visitComparison(self, ctx: CompiscriptParser.ComparisonContext):
		return ctx.getText()
		text = ctx.getText()
		data = []
		if "<=" in text:
			data = text.split("<=")
			self.log.debug(f"Datos después del split por '<=': {data}")
			return self.compare_values(data, "<=")
		elif ">=" in text:
			data = text.split(">=")
			self.log.debug(f"Datos después del split por '>=': {data}")
			return self.compare_values(data, ">=")
		elif ">" in text:
			data = text.split(">")
			self.log.debug(f"Datos después del split por '>': {data}")
			return self.compare_values(data, ">")
		elif "<" in text:
			data = text.split("<")
			self.log.debug(f"Datos después del split por '<': {data}")
			return self.compare_values(data, "<")
		else:
			return self.visitChildren(ctx)
		

	def compare_values(self, data, operator):
		value1 = data[0]
		value2 = data[1]

		comparison_operations = {
			"==": lambda x, y: x == y,
			"!=": lambda x, y: x != y,
			">": lambda x, y: x > y,
			">=": lambda x, y: x >= y,
			"<": lambda x, y: x < y,
			"<=": lambda x, y: x <= y
		}

		#if value1 in self.global_variables or value1 in self.local_variables:
		#	if value2 in self.global_variables or value2 in self.local_variables:

		# Manejar booleanos (caso especial)
		if isinstance(value1, str) and value1.lower() in ["true", "false"]:
			value1 = value1.lower() == "true"
		if isinstance(value2, str) and value2.lower() in ["true", "false"]:
			value2 = value2.lower() == "true"

		if (is_num(value1) and is_num(value2)) or (is_bool(value1) and is_bool(value2)):
			return comparison_operations[operator](value1, value2)

		# Comparar cadenas solo con `==` y `!=`
		if isinstance(value1, str) and isinstance(value2, str) and operator in ["==", "!="]:
			return comparison_operations[operator](value1, value2)

		raise TypeError(f"No se pueden comparar valores de tipos diferentes para [{value1}] y [{value2}]: {type(value1).__name__} y {type(value2).__name__}")


	def visitTerm(self, ctx: CompiscriptParser.TermContext):
		if ctx.getChildCount() == 1:
			return self.visit(ctx.factor(0))  # Retorna el único factor si no hay operación

		left = self.visit(ctx.factor(0))
		right = self.visit(ctx.factor(1))

		if type(left) is tuple: left = left[0]
		if type(right) is tuple: right = right[0]
		self.log.debug(f"left: {left}, type: {type(left)}")
		self.log.debug(f"right: {right}, type: {type(right)}")
		# Si alguno de los operandos es None, algo salió mal en el procesamiento anterior
		if left is None or right is None:
			raise Exception("Error en la evaluación de la expresión: uno de los operandos es None.")

		if is_num(str(left)) and is_num(str(right)):
			if ctx.getChild(1).getText() == '+':
				return left + right
			elif ctx.getChild(1).getText() == '-':
				return left - right
		else:
			if ctx.getChild(1).getText() == '+':
				return f"({left} + {right})"
			elif ctx.getChild(1).getText() == '-':
				return f"({left} - {right})"


	def visitFactor(self, ctx: CompiscriptParser.FactorContext):
		if ctx.getChildCount() == 1:
			return self.visit(ctx.unary(0))  # Retorna el único unary si no hay operación

		left = self.visit(ctx.unary(0))
		right = self.visit(ctx.unary(1))

		if type(left) is tuple: left = left[0]
		if type(right) is tuple: right = right[0]
		self.log.debug(f"left: {left}, type: {type(left)}")
		self.log.debug(f"right: {right}, type: {type(right)}")
		# Si alguno de los operandos es None, algo salió mal en el procesamiento anterior
		if left is None or right is None:
			raise Exception("Error en la evaluación de la expresión: uno de los operandos es None.")
		
		if is_num(str(left)) and is_num(str(right)):
			if ctx.getChild(1).getText() == '*':
				return left * right
			elif ctx.getChild(1).getText() == '/':
				return left / right
			elif ctx.getChild(1).getText() == '%':
				return left % right
		else:
			if ctx.getChild(1).getText() == '*':
				return f"({left} * {right})"
			elif ctx.getChild(1).getText() == '/':
				return f"({left} / {right})"
			elif ctx.getChild(1).getText() == '%':
				return f"({left} % {right})"


	def visitArray(self, ctx: CompiscriptParser.ArrayContext):
		# Obtener todas las expresiones dentro del array
		elements = [self.visit(expression) for expression in ctx.expression()]
		
		# Aquí podrías devolver una lista o cualquier estructura de datos que represente un array en tu lenguaje.
		return elements


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


	def visitCall(self, ctx: CompiscriptParser.CallContext):
		# function_name = ctx.primary().IDENTIFIER().getText()
		# # self.log.debug(function_name)
		
		# # Verificar si la función ha sido declarada
		# if function_name not in self.declared_functions:
		# 	raise Exception(f"Error: La función '{function_name}' no está definida.")
		
		# # Verificar los argumentos de la función (opcionalmente)
		# expected_params = self.table_functions.lookup(function_name).parameters.split(", ")
		# passed_params = ctx.arguments().expression()
		
		# if len(expected_params) != len(passed_params):
		# 	raise Exception(f"Error: La función '{function_name}' espera {len(expected_params)} argumentos, pero se pasaron {len(passed_params)}.")
		
		# Visitar los hijos (por si hay más cosas que procesar en la llamada)
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
			elif var_name in self.variables_scope[self.current_scope]:
				return self.variables_scope[self.current_scope][var_name]
			else:
				raise Exception(f"Variable '{var_name}' no declarada en el ámbito {self.current_scope}.")
		elif ctx.getText() == "true":
			return True
		elif ctx.getText() == "false":
			return False
		elif ctx.getText() == "nil":
			return None
		elif ctx.expression():
			return self.visit(ctx.expression())  # Delegate to expression handling


	def visitFunction(self, ctx: CompiscriptParser.FunctionContext):
		# Continúa la visita del cuerpo de la función
		# function_name = ctx.IDENTIFIER().getText()
		# parameters = self.visit(ctx.parameters())
		# self.log.debug(f"Function: {function_name}, Parameters: {parameters}")
		return self.visitChildren(ctx)

	# Visit a parse tree produced by CompiscriptParser#parameters.
	def visitParameters(self, ctx:CompiscriptParser.ParametersContext):
		# ctx.IDENTIFIER() devuelve una lista de nodos de identificadores.
		# Extraer el texto de cada uno para obtener los nombres de los parámetros.
		parameters = [param.getText() for param in ctx.IDENTIFIER()]
		# self.log.debug(f"OBTENCION PARAMETROS {parameters}")
		return parameters


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