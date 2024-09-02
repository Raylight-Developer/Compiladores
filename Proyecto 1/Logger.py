from Include import *

class Logger (QTextBrowser):
	def __init__(self, debug: bool = True, parent: QWidget = None):
		super().__init__(parent)
		self.setTabStopDistance(40)
		self.should_debug = debug
		self.debug_output = []

	def debug(self, value: str):
		if self.should_debug:
			self.append("\t" + value)
		else:
			self.debug_output.append(value)