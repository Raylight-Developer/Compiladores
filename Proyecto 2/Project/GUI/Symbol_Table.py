from Include import *

from Intermediate_Code.TAC_Data import *

class Symbol_Table(QTableWidget):
	def __init__(self, type: str):
		super().__init__()
		self.columns = []

		self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

		if type == "Classes":
			self.columns = ["ID", "Extends", "Init?", "Fun", "Var", "Functions", "Variables", "Size", "Addr"]
		if type == "Functions":
			self.columns = ["ID", "TAC", "Return", "Params", "Member"]
		if type == "Variables":
			self.columns = ["ID", "TAC", "Type", "Member", "Size", "Addr"]

		self.setRowCount(0)
		self.setColumnCount(len(self.columns))
		self.setHorizontalHeaderLabels(self.columns)

	def addSymbol(self, value: Tac_Class | Tac_Function | Tac_Variable):
		for row in range(self.rowCount()):
			if isinstance(value, Tac_Class):
				if (self.item(row, 0).text() == value.name):
					self.setItem(row, 1, QTableWidgetItem(str(value.extends.name) if value.extends else "-", Qt.ItemFlag.NoItemFlags))
					self.setItem(row, 2, QTableWidgetItem("Yes" if value.initializer else "-"))
					self.setItem(row, 3, QTableWidgetItem(str(len(value.member_functions))))
					self.setItem(row, 4, QTableWidgetItem(str(len(value.member_variables))))
					self.setItem(row, 5, QTableWidgetItem("[" + ", ".join([mem.name for key, mem in value.member_functions.items()]) + "]"))
					self.setItem(row, 6, QTableWidgetItem("[" + ", ".join([mem.name for key, mem in value.member_variables.items()]) + "]"))
					self.setItem(row, 7, QTableWidgetItem(str(len(value.member_variables)*8)))
					self.setItem(row, 8, QTableWidgetItem(str(value.offset)))
					return
			elif isinstance(value, Tac_Function):
				if (self.item(row, 0).text() == value.name and self.item(row, 1).text() == value.ID):
					self.setItem(row, 2, QTableWidgetItem(value.return_ID))
					self.setItem(row, 3, QTableWidgetItem("[" + ", ".join([param.name for param in value.parameters]) + "]"))
					self.setItem(row, 4, QTableWidgetItem(value.member.name if value.member else "-"))
					return
			elif isinstance(value, Tac_Variable):
				if (self.item(row, 0).text() == value.name and self.item(row, 1).text() == value.ID):
					self.setItem(row, 3, QTableWidgetItem(value.member.name if isinstance(value.member, Tac_Class) else (value.member.name + "()" if isinstance(value.member, Tac_Function) else "-") if value.member else "-"))
					if value.instance:
						self.setItem(row, 4, QTableWidgetItem(str(len(value.instance.member_variables)*8+8)))
					else:
						self.setItem(row, 4, QTableWidgetItem("8"))
					if value.member and isinstance(value.member, Tac_Class):
						self.setItem(row, 5, QTableWidgetItem(f"{value.member.offset} + {value.offset}"))
					else:
						self.setItem(row, 5, QTableWidgetItem(str(value.offset)))
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
			self.setItem(row, 7, QTableWidgetItem(str(len(value.member_variables)*8)))
			self.setItem(row, 8, QTableWidgetItem(str(value.offset)))
		elif isinstance(value, Tac_Function):
			self.setItem(row, 0, QTableWidgetItem(str(value.name)))
			self.setItem(row, 1, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 2, QTableWidgetItem(value.return_ID))
			self.setItem(row, 3, QTableWidgetItem("[" + ", ".join([param.name for param in value.parameters]) + "]"))
			self.setItem(row, 4, QTableWidgetItem(value.member.name if value.member else "-"))
		elif isinstance(value, Tac_Variable):
			self.setItem(row, 0, QTableWidgetItem(str(value.name)))
			self.setItem(row, 1, QTableWidgetItem(str(value.ID)))
			self.setItem(row, 2, QTableWidgetItem("Instance of "+str(value.instance.name) if value.instance else (str(value.array if value.array else (value.type if value.type else "Object")))))
			self.setItem(row, 3, QTableWidgetItem(value.member.name if isinstance(value.member, Tac_Class) else (value.member.name + "()" if isinstance(value.member, Tac_Function) else "-") if value.member else "-"))
			if value.instance:
				self.setItem(row, 4, QTableWidgetItem(str(len(value.instance.member_variables)*8+8)))
			else:
				self.setItem(row, 4, QTableWidgetItem("8"))
			if value.member and isinstance(value.member, Tac_Class):
				self.setItem(row, 5, QTableWidgetItem(f"{value.member.offset} + {value.offset}"))
			else:
				self.setItem(row, 5, QTableWidgetItem(str(value.offset)))

	def clean(self):
		self.clearContents()
		self.setRowCount(0)

	def end(self):
		row_count = self.rowCount()
		column_count = self.columnCount()

		for row in range(row_count):
			for col in range(column_count):
				item = self.item(row, col)
				if item:  # Make sure the item exists
					item.setFlags(item.flags() & ~Qt.ItemIsEditable)