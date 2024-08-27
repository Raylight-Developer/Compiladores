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