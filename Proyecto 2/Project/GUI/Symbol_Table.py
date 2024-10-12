from Include import *

from Intermediate_Code.TAC_Data import *

class Symbol_Table(QTableWidget):
	def __init__(self, type: str):
		super().__init__()
		self.columns = []

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

		if type == "Classes":
			self.columns = ["ID", "Extends", "Init?", "Fun", "Var", "Functions", "Variables", "Scope"]
		if type == "Functions":
			self.columns = ["ID", "TAC", "Type", "Params", "Scope"]
		if type == "Variables":
			self.columns = ["ID", "TAC", "Type", "Scope"]

		self.setRowCount(0)
		self.setColumnCount(len(self.columns))
		self.setHorizontalHeaderLabels(self.columns)

	def addSymbol(self, value: Tac_Class | Tac_Function | Tac_Variable):
		for row in range(self.rowCount()):
			if isinstance(value, Tac_Class):
				if (self.item(row, 0).text() == value.name):
					self.setItem(row, 1, QTableWidgetItem(str(value.extends.name) if value.extends else "-"))
					self.setItem(row, 2, QTableWidgetItem("Yes" if value.initializer else "-"))
					self.setItem(row, 3, QTableWidgetItem(str(len(value.member_functions))))
					self.setItem(row, 4, QTableWidgetItem(str(len(value.member_variables))))
					self.setItem(row, 5, QTableWidgetItem("[" + ", ".join([mem.name for key, mem in value.member_functions.items()]) + "]"))
					self.setItem(row, 6, QTableWidgetItem("[" + ", ".join([mem.name for key, mem in value.member_variables.items()]) + "]"))
					return
			elif isinstance(value, Tac_Function):
				if (self.item(row, 0).text() == value.name):
					self.setItem(row, 1, QTableWidgetItem(str(value.ID)))
					self.setItem(row, 2, QTableWidgetItem('|'.join([param.name for param in value.parameters])))
					self.setItem(row, 4, QTableWidgetItem(value.member.name if value.member else "Global"))
					return
			elif isinstance(value, Tac_Variable):
				if (self.item(row, 0).text() == value.name):
					self.setItem(row, 1, QTableWidgetItem(str(value.ID)))
					self.setItem(row, 3, QTableWidgetItem(value.member.name if value.member else "Global"))
					return

		row = self.rowCount()
		self.setRowCount(row + 1)
		if isinstance(value, Tac_Class):
			self.setItem(row, 0, QTableWidgetItem(str(value.name)))
			self.setItem(row, 1, QTableWidgetItem(str(value.extends.name) if value.extends else "-"))
			self.setItem(row, 2, QTableWidgetItem(str(value.initializer.name) if value.initializer else "-"))
			self.setItem(row, 3, QTableWidgetItem(str(len(value.member_functions))))
			self.setItem(row, 4, QTableWidgetItem(str(len(value.member_variables))))
			self.setItem(row, 5, QTableWidgetItem("[" + ", ".join([mem.name for key, mem in value.member_functions.items()]) + "]"))
			self.setItem(row, 6, QTableWidgetItem("[" + ", ".join([mem.name for key, mem in value.member_variables.items()]) + "]"))
		elif isinstance(value, Tac_Function):
			self.setItem(row, 0, QTableWidgetItem(str(value.name)))
			self.setItem(row, 1, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 2, QTableWidgetItem("[" + ", ".join([param.name for param in value.parameters]) + "]"))
			self.setItem(row, 3, QTableWidgetItem(value.return_ID))
			self.setItem(row, 4, QTableWidgetItem(value.member.name if value.member else "Global"))
		elif isinstance(value, Tac_Variable):
			self.setItem(row, 0, QTableWidgetItem(str(value.name)))
			self.setItem(row, 1, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 2, QTableWidgetItem("Instance of "+str(value.instance.name) if value.instance else (str(value.array if value.array else "Object"))))
			self.setItem(row, 3, QTableWidgetItem(value.member.name if value.member else "Global"))

	def clean(self):
		self.clearContents()
		self.setRowCount(0)