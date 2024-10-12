from Include import *

from Intermediate_Code.TAC_Data import *

class Symbol_Table(QTableWidget):
	def __init__(self, type: str):
		super().__init__()
		self.columns = []

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

		if type == "Functions":
			self.columns = ["ID", "TAC", "Params", "Scope"]
		if type == "Variables":
			self.columns = ["ID", "TAC", "Scope"]

		self.setRowCount(0)
		self.setColumnCount(len(self.columns))
		self.setHorizontalHeaderLabels(self.columns)

	def addSymbol(self, value: Tac_Class | Tac_Function | Tac_Variable):
		row = self.rowCount()
		self.setRowCount(row + 1)

		if isinstance(value, Tac_Variable) and value.instance:
			self.setItem(row, 1, QTableWidgetItem(str(value.ID)))
		elif isinstance(value, Tac_Function):
			self.setItem(row, 0, QTableWidgetItem(str(value.name)))
			self.setItem(row, 1, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 2, QTableWidgetItem('|'.join([param.name for param in value.parameters])))
			self.setItem(row, 3, QTableWidgetItem(value.member.name if value.member else "Global"))
		elif isinstance(value, Tac_Variable):
			self.setItem(row, 0, QTableWidgetItem(str(value.name)))
			self.setItem(row, 1, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 2, QTableWidgetItem(value.member.name if value.member else "Global"))
	
			if value.instance:
				self.setItem(row, 3, QTableWidgetItem(str(value.instance.name)))
				self.setItem(row, 4, QTableWidgetItem("Yes" if value.instance.initializer else "No"))
				self.setItem(row, 5, QTableWidgetItem(str(len(value.instance.member_functions))))
				self.setItem(row, 6, QTableWidgetItem(str(len(value.instance.member_variables))))
				self.setItem(row, 7, QTableWidgetItem(value.instance.extends.name if value.instance.extends else 'Global'))

	def clean(self):
		self.clearContents()
		self.setRowCount(0)