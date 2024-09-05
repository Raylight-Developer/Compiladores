from Include import *

from Symbols import *

class Symbol_Table(QTableWidget):
	def __init__(self, log: QTextBrowser, type: str):
		super().__init__()
		self.columns = []
		self.log = log

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

		if type == "Classes":
			self.columns = ["ID", "Parent", "Code"]
		if type == "Functions":
			self.columns = ["ID", "Return Type", "Code"]
		if type == "Variables":
			self.columns = ["ID", "Type", "Code"]

		self.setRowCount(0)
		self.setColumnCount(len(self.columns))
		self.setHorizontalHeaderLabels(self.columns)

	def addSymbol(self, value: Union[Class | Function | Variable]):
		row = self.rowCount()
		self.setRowCount(row + 1)

		if isinstance(value, Class):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(str(value.parent)))
			self.setItem(row, 2, QTableWidgetItem(str(value.code)))
		elif isinstance(value, Function):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(str(value.return_type)))
			self.setItem(row, 2, QTableWidgetItem(str(value.code)))
		elif isinstance(value, Variable):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(str(value.type)))
			self.setItem(row, 2, QTableWidgetItem(str(value.code)))