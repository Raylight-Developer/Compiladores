from Include import *

class Symbol_Table:
	def __init__(self, log: QTextBrowser, table: QTableWidget):
		self.symbols = []
		self.columns = []
		self.log = log
		self.table = table

	def init(self):
<<<<<<< HEAD
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
=======
		labels = ['ID','Type', 'Scope', 'Value', 'Position', 'Address']
		self.table.setColumnCount(len(labels))
		self.table.setRowCount(len(self.symbols))
		self.table.setHorizontalHeaderLabels(labels)
		self.table.resizeColumnsToContents()

	def add_symbol(self, symbol_data):
		"""
		Agrega un símbolo a la tabla de símbolos y actualiza el QTableWidget.

		:param symbol_data: Una lista que contiene los datos del símbolo en el orden de las columnas.
		"""
		self.symbols.append(symbol_data)
		
		row_position = self.table.rowCount()
		self.table.insertRow(row_position)
		
		for column, data in enumerate(symbol_data):
			# item = QTableWidgetItem(str(data))  # Asegúrate de convertir todos los datos a string
			item = QTableWidgetItem(f"Test {column}")
			self.table.setItem(row_position, column, item)
>>>>>>> 26f1dcc (Modificaciones para las tablas, funciona para variables, flata para mucho mas)
