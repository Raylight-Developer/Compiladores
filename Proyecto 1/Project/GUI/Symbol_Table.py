from Include import *

from Analyzer.Symbols import *

class Symbol_Table(QTableWidget):
	def __init__(self, type: str):
		super().__init__()
		self.columns = []

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

		if type == "Classes":
			self.columns = ["ID", "Parent", "Code", "Function Members", "Variable Members"]
		if type == "Functions":
			self.columns = ["ID", "Return Type", "Code", "Parent"]
		if type == "Variables":
			self.columns = ["ID", "Type", "Code", "Parent"]

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
			self.setItem(row, 3, QTableWidgetItem('\n'.join([str(item) for item in value.member_functions])))
			self.setItem(row, 4, QTableWidgetItem('\n'.join([str(item) for item in value.member_variables])))
		elif isinstance(value, Function):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(value.return_type.value))
			self.setItem(row, 2, QTableWidgetItem(str(value.code)))
			self.setItem(row, 3, QTableWidgetItem(str(value.member)))
		elif isinstance(value, Variable):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(value.type.value))
			self.setItem(row, 2, QTableWidgetItem(str(value.code)))
			self.setItem(row, 3, QTableWidgetItem(str(value.member)))