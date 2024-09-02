from Include import *
from Syntax_Highlighting import *

class Viewer(QTextBrowser):
	def __init__(self):
		super().__init__()
		self.setReadOnly(True)
		self.setTabStopDistance(40)
		self.textChanged.connect(self.autoResize)

	def autoResize(self):
		self.document().setTextWidth(self.viewport().width())
		margins = self.contentsMargins()
		height = int(self.document().size().height() + margins.top() + margins.bottom())
		self.setFixedHeight(height)

	def resizeEvent(self, event):
		self.autoResize()

class Logger(QTextBrowser):
	def __init__(self, debug: bool = True, parent: QWidget = None):
		super().__init__(parent)
		self.setTabStopDistance(40)
		self.setObjectName("Main")
		self.should_debug = debug
		self.debug_output = []

	def debug(self, value: str):
		if self.should_debug:
			self.append("\t" + value)
		else:
			self.debug_output.append(value)

class Test_Logger(QScrollArea):
	def __init__(self, debug: bool = True, parent: QWidget = None):
		super().__init__(parent)
		self.setWidgetResizable(True)
		self.should_debug = debug
		self.debug_output = []
		self.contents = QVBoxLayout()
		self.contents.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.contents.setSpacing(0)
		content = QWidget()
		content.setContentsMargins(0,0,0,0)
		content.setLayout(self.contents)
		self.setWidget(content)

	def debug(self, value: str, indent: int = 0):
		if self.should_debug:
			Text = Viewer()
			Text.append(value)
			Text.setStyleSheet(f"padding-left: {5 + indent * 40}px")
			self.contents.addWidget(Text)
		else:
			self.debug_output.append(value)

	def append(self, value:str, indent: int = 0):
		Text = Viewer()
		Text.append(value)
		Text.setStyleSheet(f"padding-left: {5 +indent * 40}px")
		self.contents.addWidget(Text)

	def insertPlainText(self, value:str, indent: int = 0):
		Text = Viewer()
		Text.insertPlainText(value)
		Text.setStyleSheet(f"padding-left: {5 +indent * 40}px")
		self.contents.addWidget(Text)

	def addCode(self, value:str, indent: int = 0):
		Text = Viewer()
		Text.setStyleSheet(f"padding-left: {5 +indent * 40}px")
		Syntax_Highlighter(Text.document())

		Text.append(value)
		self.contents.addWidget(Text)

	def addCollapse(self, title: str, value: str, indent: int = 0):
		button = QPushButton(title)

		Text = Viewer()
		Text.insertPlainText(value)
		Text.setStyleSheet(f"margin-left: {5 +indent * 40}px; background:rgb(50,50,50);")

		container = QWidget()
		container.setStyleSheet("margin: 0px; margin-top:4px; margin-bottom:4px;")
		layout = QVBoxLayout()
		layout.setSpacing(0)
		layout.setContentsMargins(0,0,0,0)
		container.setLayout(layout)
		layout.addWidget(button)
		layout.addWidget(Text)
		Text.hide()
		button.clicked.connect(lambda: (
			Text.hide() if Text.isVisible() else Text.show()
		))

		self.contents.addWidget(container)

	def addSep(self):
		separator = QWidget()
		separator.setFixedHeight(2)
		separator.setStyleSheet("background:rgb(150,150,150);")
		self.contents.addWidget(separator)