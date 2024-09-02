from Include import *

DEBUG = True

class Logger (QTextBrowser):
	def __init__(self, parent: QWidget = None):
		super().__init__(parent)
		self.setTabStopDistance(40)

	def debug(self, value: str):
		if DEBUG:
			self.append("\t" + value)