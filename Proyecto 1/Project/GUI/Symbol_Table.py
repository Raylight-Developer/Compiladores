from Include import *

from Analyzer.Symbols import *

class Symbol_Table(QTableWidget):
	def __init__(self, type: str):
		super().__init__()
		self.columns = []

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

		if type == "Classes":
			self.columns = ["ID", "Scope", "S", "D", "Has Init?", "Functions", "Variables"]
		if type == "Functions":
			self.columns = ["ID", "Scope", "S", "D", "Return Type", "Origin", "Parameters", "Code"]
		if type == "Variables":
			self.columns = ["ID", "Scope", "S", "D", "Type", "Origin", "Code"]

		self.setRowCount(0)
		self.setColumnCount(len(self.columns))
		self.setHorizontalHeaderLabels(self.columns)

	def addSymbol(self, value: Class | Function | Variable):
		row = self.rowCount()
		self.setRowCount(row + 1)

		if isinstance(value, Class):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(value.parent.ID if value.parent else 'Global'))
			self.setItem(row, 2, QTableWidgetItem(str(value.scope_depth_count)))
			self.setItem(row, 3, QTableWidgetItem(str(value.scope_depth)))
			self.setItem(row, 4, QTableWidgetItem("Yes" if value.initializer else "No"))
			self.setItem(row, 5, QTableWidgetItem(str(len(value.member_functions))))
			self.setItem(row, 6, QTableWidgetItem(str(len(value.member_variables))))
		elif isinstance(value, Function):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(value.member.ID if value.member else "Global"))
			self.setItem(row, 2, QTableWidgetItem(str(value.scope_depth_count)))
			self.setItem(row, 3, QTableWidgetItem(str(value.scope_depth) if not value.member else "-"))
			self.setItem(row, 4, QTableWidgetItem(value.return_type.value))
			self.setItem(row, 5, QTableWidgetItem(value.origin))
			self.setItem(row, 6, QTableWidgetItem('|'.join([param.ID for param in value.parameters])))
			self.setItem(row, 7, QTableWidgetItem(str(value.data)))
		elif isinstance(value, Variable):
			self.setItem(row, 0, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 1, QTableWidgetItem(value.member.ID if value.member else "Global"))
			self.setItem(row, 2, QTableWidgetItem(str(value.scope_depth_count)))
			self.setItem(row, 3, QTableWidgetItem(str(value.scope_depth) if not value.member else "-"))
			self.setItem(row, 4, QTableWidgetItem(value.type.value))
			self.setItem(row, 5, QTableWidgetItem(value.origin))
			self.setItem(row, 6, QTableWidgetItem(str(value.data)))

	def removeSymbol(self, value: Class | Function | Variable):
		for row in range(self.rowCount()):
			if isinstance(value, Class):
				if self.item(row, 0).text() == value.ID and self.item(row, 1).text() == value.parent.ID if value.parent else "Global":
					self.removeRow(row)
					break
			elif isinstance(value, Function):
				if self.item(row, 0).text() == value.ID and self.item(row, 1).text() == value.member.ID if value.member else "Global":
					self.removeRow(row)
					break
			elif isinstance(value, Variable):
				if self.item(row, 0).text() == value.ID and self.item(row, 1).text() == value.member.ID if value.member else "Global":
					self.removeRow(row)
					break

	def updateSymbol(self, value: Class | Function | Variable):
		for row in range(self.rowCount()):
			if isinstance(value, Class):
				if (self.item(row, 0).text() == value.ID and self.item(row, 1).text() == (value.parent.ID if value.parent else "Global")):
					self.setItem(row, 2, QTableWidgetItem(str(value.scope_depth_count)))
					self.setItem(row, 3, QTableWidgetItem(str(value.scope_depth)))
					self.setItem(row, 4, QTableWidgetItem("Yes" if value.initializer else "No"))
					self.setItem(row, 5, QTableWidgetItem(str(len(value.member_functions))))
					self.setItem(row, 6, QTableWidgetItem(str(len(value.member_variables))))
					break

			elif isinstance(value, Function):
				if (self.item(row, 0).text() == value.ID and self.item(row, 1).text() == (value.member.ID if value.member else "Global")):
					self.setItem(row, 2, QTableWidgetItem(str(value.scope_depth_count)))
					self.setItem(row, 3, QTableWidgetItem(str(value.scope_depth) if not value.member else "-"))
					self.setItem(row, 4, QTableWidgetItem(value.return_type.value))
					self.setItem(row, 5, QTableWidgetItem(value.origin))
					self.setItem(row, 6, QTableWidgetItem('|'.join([param.ID for param in value.parameters])))
					self.setItem(row, 7, QTableWidgetItem(str(value.data)))
					break

			elif isinstance(value, Variable):
				# Check for matching ID and member
				if (self.item(row, 0).text() == value.ID and self.item(row, 1).text() == (value.member.ID if value.member else "Global")):
					self.setItem(row, 2, QTableWidgetItem(str(value.scope_depth_count)))
					self.setItem(row, 3, QTableWidgetItem(str(value.scope_depth) if not value.member else "-"))
					self.setItem(row, 4, QTableWidgetItem(value.type.value))
					self.setItem(row, 5, QTableWidgetItem(value.origin))
					self.setItem(row, 6, QTableWidgetItem(str(value.data)))
					break