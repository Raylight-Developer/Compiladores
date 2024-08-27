from Include import *

class Symbol_Table:
	def __init__(self, log: QTextBrowser, table: QTableWidget):
		self.symbols = []
		self.columns = []
		self.log = log
		self.table = table

	def init(self):
		self.columns = ['ID', 'Type', 'Scope', 'Value', 'Position', 'Address']
		
		self.table.setColumnCount(len(self.columns))
		self.table.setRowCount(0)
		self.table.setHorizontalHeaderLabels(self.columns)
		self.table.resizeColumnsToContents()
	

	def add(self, row: int, column: Union[int, str], value: str):
		if self.table.rowCount() < row:
			self.table.setRowCount(row)
		if isinstance(column, str):
			self.table.setItem(row, self.columns.index(column), QTableWidgetItem(value))
		else:
			self.table.setItem(row, column, QTableWidgetItem(value))
		labels = ['ID','Type', 'Scope', 'Value', 'Position', 'Address']
		self.table.setColumnCount(len(labels))
		self.table.setRowCount(len(self.symbols))
		self.table.setHorizontalHeaderLabels(labels)
		self.table.resizeColumnsToContents()

	def add_symbol(self, symbol_data):
		print(f"Agregando símbolo: {symbol_data}")  # Depuración
		self.symbols.append(symbol_data)
		
		row_position = self.table.rowCount()
		self.table.insertRow(row_position)
		
		for column, data in enumerate(symbol_data):
			print(f"Setting item at row {row_position}, column {column} with data: {data}")  # Depuración
			item = QTableWidgetItem(str(data))  # Asegúrate de convertir todos los datos a string
			self.table.setItem(row_position, column, item)
		
		# Forzar la actualización de la tabla en la interfaz
		self.table.repaint()

    # Si es necesario, agrega una función para actualizar toda la tabla
	def update_table(self):
		self.table.setRowCount(0)  # Limpia la tabla
		for symbol_data in self.symbols:
			self.add_symbol(symbol_data)