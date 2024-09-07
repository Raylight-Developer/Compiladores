from Include import *

from Analyzer.Symbols import *

class Symbol_Table(QTableWidget):
	def __init__(self, type: str):
		super().__init__()
		self.columns = []

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

		if type == "Classes":
			self.columns = ["ID", "Parent", "Code", "Initializer", "Functions", "Variables"]
		if type == "Functions":
			self.columns = ["ID", "Return Type", "Code", "Scope", "Depth", "Parameters"]
		if type == "Variables":
			self.columns = ["ID", "Type", "Code", "Scope", "Depth"]

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
			self.setItem(row, 3, QTableWidgetItem("true" if value.initializer else "false"))
			self.setItem(row, 4, QTableWidgetItem(str(len(value.member_functions))))
			self.setItem(row, 5, QTableWidgetItem(str(len(value.member_variables))))
		elif isinstance(value, Function):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(value.return_type.value))
			self.setItem(row, 2, QTableWidgetItem(str(value.code)))
			self.setItem(row, 3, QTableWidgetItem(str(value.member) if value.member else "Global"))
			self.setItem(row, 4, QTableWidgetItem(str(value.scope_depth)))
			self.setItem(row, 5, QTableWidgetItem('|'.join([param.ID for param in value.parameters])))
		elif isinstance(value, Variable):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(value.type.value))
			self.setItem(row, 2, QTableWidgetItem(str(value.code)))
			self.setItem(row, 3, QTableWidgetItem(str(value.member) if value.member else "Global"))
			self.setItem(row, 4, QTableWidgetItem(str(value.scope_depth)))