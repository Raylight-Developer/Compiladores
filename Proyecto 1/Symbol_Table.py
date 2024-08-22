from PyQt6.QtWidgets import *

class Symbol_Table:
	def __init__(self, log: QTextBrowser, table: QTableWidget):
		self._symbols = []
		self.log = log
		self.table = table

	def add(self, type, id, scope, value=None, position=None, address=None, isParameter=False, isInherited=False):
		symbol = {
			'Type': type,
			'ID': id,
			'Scope': scope,
			'Value': value,
			'Position': position,
			'Address': address,
			'IsParameter': isParameter,
			'IsInherited': isInherited
		}
		self._symbols.append(str(symbol))
		self.log.append(f"Add Symbol: {symbol}")

	def lookup(self, id):
		for symbol in reversed(self._symbols):
			if symbol['ID'] == id:
				return symbol
		return None

	def lookup_w_type(self, id, type):
		for symbol in reversed(self._symbols):
			if symbol['ID'] == id and symbol['Type'] == type:
				return symbol
		return None

	def getsize(self):
		return len(self._symbols)

	def totable(self):
		labels = ['Type', 'ID', 'Scope', 'Value', 'Position', 'Address', 'IsParameter', 'IsInherited']
		self.table.setColumnCount(len(labels))
		self.table.setRowCount(len(self._symbols) + 1)
		self.table.setHorizontalHeaderLabels(labels)

		for i, symbol in enumerate(self._symbols):
			rows = [symbol.get(field, '') for field in labels]
			for j, row in enumerate(rows):
				self.table.setItem(i, j, QTableWidgetItem(str(row)))

	def delete(self, ID):
		self._symbols = [symbol for symbol in self._symbols if symbol['ID'] != ID]

	def update(self, ID, value):
		for symbol in self._symbols:
			if symbol['ID'] == ID:
				symbol['Value'] = value
				break

	def update_global(self, ID, value, scope):
		for symbol in self._symbols:
			if symbol['ID'] == ID and symbol['Scope'] == scope:
				symbol['Value'] = value
				break