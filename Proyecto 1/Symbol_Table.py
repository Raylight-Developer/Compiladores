from Include import *

class Symbol_Property:
	id: str = ""
	type: str = ""
	size: int = 0
	offset: int = 0
	address: int = 0
	scope: Union[str , None] = ""
	value: str | Any = ""

class Symbol_Table(QTableWidget):
	def __init__(self, log: QTextBrowser):
		super().__init__()
		self.symbols = []
		self.columns = []
		self.log = log

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
		self.columns = ["ID", "Type", "Size", "Offset", "Address", "Scope", "Value"]
		self.setColumnCount(len(self.columns))
		self.setRowCount(0)
		self.setHorizontalHeaderLabels(self.columns)
		self.resizeColumnsToContents()

	def add(self, value: Symbol_Property):
		row = self.rowCount()
		self.setRowCount(row + 1)
		self.setItem(row, 0, QTableWidgetItem(str(value.id)))
		self.setItem(row, 1, QTableWidgetItem(str(value.type)))
		self.setItem(row, 2, QTableWidgetItem(str(value.size)))
		self.setItem(row, 3, QTableWidgetItem(str(value.offset)))
		self.setItem(row, 4, QTableWidgetItem(str(value.address)))
		self.setItem(row, 5, QTableWidgetItem(str(value.scope)))
		self.setItem(row, 6, QTableWidgetItem(str(value.value)))

	def addSingle(self, row: int, column: Union[int, str], value: str):
		if self.rowCount() < row:
			self.setRowCount(row)
		if isinstance(column, str):
			self.setItem(row - 1, self.columns.index(column), QTableWidgetItem(value))
		else:
			self.setItem(row - 1, column, QTableWidgetItem(value))
