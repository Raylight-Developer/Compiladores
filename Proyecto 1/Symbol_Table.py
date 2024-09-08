from Include import *

class Scope:
	def __init__(self, id: str):
		self.id = id  # Identificador del scope
		self.symbols = {}  # Diccionario de símbolos dentro del scope

	
class Symbol_Property:
	id: str = ""

	type: str = ""
	size: int = 0
	offset: int = 0
	scope: Union[str , None] = ""
	# Modificación aquí: Acepta str o List[Any]
	value: Union[str, List[Any]]= ""

	parameters: str = ""
	return_type: str = ""

	attributes: str = ""
	inherits: str = ""
	methods: str = ""

class Symbol_Table(QTableWidget):
	def __init__(self, log: QTextBrowser, type: str):
		super().__init__()
		self.symbols = []
		self.columns = []
		self.log = log
		self.type = type
		self.scope_counter = 0  # Contador para enumerar los scopes
		self.scopes = [Scope(f"global_{self.scope_counter}")]  # Stack de scopes, iniciando con el scope global

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

		if self.type == "Var":
			self.columns = ["ID", "Type", "Size", "Offset", "Scope", "Code"]
		elif self.type == "Fun":
			self.columns = ["ID", "Parameters", "Return Type", "Code"]
		elif self.type == "Cla":
			self.columns = ["ID", "Size", "Attributes", "Inherits", "Methods"]

		self.setColumnCount(len(self.columns))
		self.setRowCount(0)
		self.setHorizontalHeaderLabels(self.columns)
		self.resizeColumnsToContents()

	def add(self, value: Symbol_Property):
		row = self.rowCount()
		# Convertir el valor si es una lista
		if isinstance(value.value, list):
			value.value = ", ".join(map(str, value.value))  # Convierte la lista a una cadena de texto
		else:
			value.value = str(value.value)
		self.setRowCount(row + 1)
		if self.type == "Var":
			self.setItem(row, 0, QTableWidgetItem(str(value.id)))
			self.setItem(row, 1, QTableWidgetItem(str(value.type)))
			self.setItem(row, 2, QTableWidgetItem(str(value.size)))
			self.setItem(row, 3, QTableWidgetItem(str(value.offset)))
			self.setItem(row, 4, QTableWidgetItem(str(value.scope)))
			self.setItem(row, 5, QTableWidgetItem((value.value)))
		elif self.type == "Fun":
			self.setItem(row, 0, QTableWidgetItem(str(value.id)))
			self.setItem(row, 1, QTableWidgetItem(str(value.parameters)))
			self.setItem(row, 2, QTableWidgetItem(str(value.return_type)))
			self.setItem(row, 3, QTableWidgetItem(str(value.value)))
		elif self.type == "Cla":
			self.setItem(row, 0, QTableWidgetItem(str(value.id)))
			self.setItem(row, 1, QTableWidgetItem(str(value.size)))
			self.setItem(row, 2, QTableWidgetItem(str(value.attributes)))
			self.setItem(row, 3, QTableWidgetItem(str(value.inherits)))
			self.setItem(row, 4, QTableWidgetItem(str(value.methods)))

	def addSingle(self, row: int, column: Union[int, str], value: str):
		if self.rowCount() < row:
			self.setRowCount(row)
		if isinstance(column, str):
			self.setItem(row - 1, self.columns.index(column), QTableWidgetItem(value))
		else:
			self.setItem(row - 1, column, QTableWidgetItem(value))
	
	def enter_scope(self):
		# Incrementa el contador y añade un nuevo scope con un ID único
		self.scope_counter += 1
		new_scope_id = f"scope{self.scope_counter}"
		self.scopes.append(Scope(new_scope_id))

	def exit_scope(self):
		# Elimina el scope actual del stack
		if len(self.scopes) > 1:  # Asegúrate de no eliminar el scope global
			self.scopes.pop()

	def add_scope(self, symbol_property: Symbol_Property):
		# Añade una nueva variable al scope actual
		current_scope = self.scopes[-1]
		current_scope.symbols[symbol_property.id] = symbol_property
		symbol_property.scope = current_scope.id  # Asigna el ID del scope a la propiedad del símbolo


	def lookup(self, var_name):
		"""Buscar una variable en los scopes locales y globales."""
		# Primero busca en los scopes locales, desde el más interno hacia afuera.
		for scope in reversed(self.scopes):
			if var_name in scope.symbols:
				return scope.symbols[var_name]

		# Si no se encuentra, lanza una excepción.
		raise Exception(f"Error: Variable '{var_name}' no declarada.")
	
	def add_and_scope(self, value: Symbol_Property):
		self.add(value)
		self.add_scope(value)