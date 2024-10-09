from GUI.Logger import*
from GUI.Syntax_Highlighting import *

from Analyzer.Semantic_Analyzer import *
from Intermediate_Code.TAC import *

TAC_INFO = False

class Display(QMainWindow):
	def __init__(self):
		super().__init__()
		args = sys.argv[1:]
		self.options = parse_args(args)

		self.setWindowTitle("Semantic Compiler")

		self.code_input = QTextEdit()
		self.code_input.setTabStopDistance(40)
		self.code_input.setPlaceholderText("Code to compile...")
		Syntax_Highlighter(self.code_input.document())
		self.code_input.setText(open("./Tests/Ejemplo4.cspt", "r", -1, "utf-8").read())
		self.tac_output = Logger()
		self.tac_output.setPlaceholderText("TAC code")
		self.tac_highlight = TAC_Syntax_Highlighter(self.tac_output.document())

		self.sam_output = Logger()
		self.sam_output.setPlaceholderText("SAM output")
		self.sam_output.setTabStopDistance(10)
		self.sam_highlight = SAM_Syntax_Highlighter(self.sam_output.document())

		self.tables = QTabWidget()

		self.table_classes   = Symbol_Table("Classes")
		self.table_functions = Symbol_Table("Functions")
		self.table_variables = Symbol_Table("Variables")

		self.tables.addTab(self.table_classes  , QIcon(), "Classes")
		self.tables.addTab(self.table_functions, QIcon(), "Functions")
		self.tables.addTab(self.table_variables, QIcon(), "Variables")

		tablayout = QHBoxLayout()
		tablayout.setContentsMargins(12,12,12,14)
		tablayout.addWidget(self.tables)
		tabcontainer = QWidget()
		tabcontainer.setObjectName("Table")
		tabcontainer.setLayout(tablayout)

		sub = QSplitter(Qt.Orientation.Vertical)
		sub.addWidget(self.sam_output)
		sub.addWidget(tabcontainer)

		self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
		self.main_splitter.addWidget(self.code_input)
		self.main_splitter.addWidget(self.tac_output)
		self.main_splitter.addWidget(sub)
		self.main_splitter.setSizes([500,500,0])

		button_compile = QPushButton("Compile")
		button_compile.clicked.connect(self.compile)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.main_splitter)
		main_layout.addWidget(button_compile)

		widget = QWidget()
		widget.setObjectName("Background")
		widget.setLayout(main_layout)

		self.setCentralWidget(widget)
		
		QTimer.singleShot(200, lambda: (
			self.table_classes.resizeColumnsToContents(),
			self.table_functions.resizeColumnsToContents(),
			self.table_variables.resizeColumnsToContents()
		))
		self.compile()

	def compile(self):
		self.tac_highlight = TAC_Syntax_Highlighter(self.tac_output.document())
		self.sam_highlight = SAM_Syntax_Highlighter(self.sam_output.document())

		self.tac_output.clear()
		self.sam_output.clear()
		self.table_functions.clean()
		self.table_variables.clean()
		self.table_classes.clean()

#		try:
#			self.sam_output.append("Compiling...\n{")
#			lexer = CompiscriptLexer(InputStream(self.code_input.toPlainText()))
#			token_stream = CommonTokenStream(lexer)
#			parser = CompiscriptParser(token_stream)
#			program = parser.program()
#			sma = Semantic_Analyzer(self.table_classes, self.table_functions, self.table_variables, program)
#
#			self.table_classes.resizeColumnsToContents()
#			self.table_functions.resizeColumnsToContents()
#			self.table_variables.resizeColumnsToContents()
#
#			if sma.output.error:
#				self.sam_output.append("\t" + str(sma.output).strip())
#				self.sam_output.append("}" + f"\n{R} Compilation Failed")
#				self.main_splitter.setSizes([self.main_splitter.sizes()[0], self.main_splitter.sizes()[1], 500])
#				QTimer.singleShot(100, lambda: (
#					self.sam_output.verticalScrollBar().setValue(0),
#					self.sam_output.horizontalScrollBar().setValue(0),
#					self.tac_output.verticalScrollBar().setValue(self.tac_output.verticalScrollBar().maximum()),
#					self.tac_output.horizontalScrollBar().setValue(0)
#				))
#			else:
#				self.sam_output.append("\t" + str(sma.output).strip())
#				self.sam_output.append("}" + f"\n{G} Comiplation Succesful")
#				QTimer.singleShot(100, lambda: (
#					self.sam_output.verticalScrollBar().setValue(0),
#					self.sam_output.horizontalScrollBar().setValue(0)
#				))
#				self.main_splitter.setSizes([self.main_splitter.sizes()[0], self.main_splitter.sizes()[1], 0])
#
#
#		except Exception as e:
#			self.sam_highlight = Python_Syntax_Highlighter(self.sam_output.document())
#			self.sam_output.append("\t" + str(traceback.format_exc()).strip())
#			self.sam_output.append("}" + f"\n{R} Compilation Failed")
#			self.sam_output.append(str(e))
#			self.main_splitter.setSizes([self.main_splitter.sizes()[0], self.main_splitter.sizes()[1], 500])
#			QTimer.singleShot(100, lambda: (
#				self.sam_output.verticalScrollBar().setValue(self.sam_output.verticalScrollBar().maximum()),
#				self.sam_output.horizontalScrollBar().setValue(0)
#			))

		try:
			lexer = CompiscriptLexer(InputStream(self.code_input.toPlainText()))
			token_stream = CommonTokenStream(lexer)
			parser = CompiscriptParser(token_stream)
			program = parser.program()
			tac = TAC_Generator(program, TAC_INFO)
			self.tac_output.append(str(tac.output).strip())
			QTimer.singleShot(100, lambda: (
				self.tac_output.verticalScrollBar().setValue(0),
				self.tac_output.horizontalScrollBar().setValue(0)
			))
		except Exception as e:
			self.tac_highlight = Python_Syntax_Highlighter(self.tac_output.document())
			self.tac_output.append(str(traceback.format_exc()).strip())
			QTimer.singleShot(100, lambda: (
				self.tac_output.verticalScrollBar().setValue(self.tac_output.verticalScrollBar().maximum()),
				self.tac_output.horizontalScrollBar().setValue(0)
			))

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./Resources/RobotoMono-Medium.ttf")
app.setStyleSheet(open("./Resources/QStyleSheet.css", "r").read())
Window = Display()
Window.showMaximized()
app.exec()