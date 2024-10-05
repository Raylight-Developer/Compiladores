from Include import *
from GUI.Syntax_Highlighting import *

class Logger(QTextBrowser):
	def __init__(self, debug: bool = True, parent: QWidget = None):
		super().__init__(parent)
		self.setTabStopDistance(40)
		self.setObjectName("Main")
		self.setWordWrapMode(QTextOption.WrapMode.NoWrap)