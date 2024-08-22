from PyQt6.QtWidgets import *

class Symbol_Table:
	def __init__(self, log: QTextBrowser, table: QTableWidget):
		self.symbols = []
		self.log = log
		self.table = table

	def init(self):
		labels = ['Type', 'ID', 'Scope', 'Value', 'Position', 'Address', 'IsParameter', 'IsInherited']
		self.table.setColumnCount(len(labels))
		self.table.setRowCount(len(self.symbols) + 1)
		self.table.setHorizontalHeaderLabels(labels)