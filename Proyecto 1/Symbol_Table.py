from Include import *

class Symbol_Property:
	id: str
	value: str | Any
	scope: Union[str , None]

class Symbol_Table(QTableWidget):
	def __init__(self, log: QTextBrowser):
		super().__init__()
		self.symbols = []
		self.columns = []
		self.log = log

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
		self.columns = ["ID", "Type", "Scope", "Value", "Position", "Address"]
		self.setColumnCount(len(self.columns))
		self.setRowCount(0)
		self.setHorizontalHeaderLabels(self.columns)
		self.resizeColumnsToContents()

	def add(self, row: int, column: Union[int, str], value: str):
		if self.rowCount() < row:
			self.setRowCount(row)
		if isinstance(column, str):
			self.setItem(row - 1, self.columns.index(column), QTableWidgetItem(value))
		else:
			self.setItem(row - 1, column, QTableWidgetItem(value))