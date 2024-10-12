from GUI.Logger import*
from GUI.Syntax_Highlighting import *

#from Analyzer.Semantic_Analyzer import *
from Intermediate_Code.TAC import *

TAC_INFO = True

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
		self.code_input.setText(open("./Tests/Ejemplo1.cspt", "r", -1, "utf-8").read())
		self.tac_output = Logger()
		self.tac_output.setPlaceholderText("TAC code")
		self.tac_highlight = TAC_Syntax_Highlighter(self.tac_output.document())

		self.debug_output = Logger()
		self.debug_output.setPlaceholderText("Debug output")
		self.debug_output.setTabStopDistance(10)
		self.debug_highlight = SAM_Syntax_Highlighter(self.debug_output.document())

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
		sub.addWidget(self.debug_output)
		sub.addWidget(tabcontainer)

		self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
		self.main_splitter.addWidget(self.code_input)
		self.main_splitter.addWidget(self.tac_output)
		self.main_splitter.addWidget(sub)

		button_compile = QPushButton("Compile")
		button_compile.clicked.connect(self.compile)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.main_splitter)
		main_layout.addWidget(button_compile)

		widget = QWidget()
		widget.setObjectName("Background")
		widget.setLayout(main_layout)

		self.setCentralWidget(widget)
		
		self.compile()
		QTimer.singleShot(50, lambda: (
			self.table_classes.resizeColumnsToContents(),
			self.table_functions.resizeColumnsToContents(),
			self.table_variables.resizeColumnsToContents()
		))

	def compile(self):
		self.tac_highlight = TAC_Syntax_Highlighter(self.tac_output.document())
		self.debug_highlight = SAM_Syntax_Highlighter(self.debug_output.document())

		self.tac_output.clear()
		self.debug_output.clear()
		self.table_classes.clean()
		self.table_functions.clean()
		self.table_variables.clean()

		try:
			lexer = CompiscriptLexer(InputStream(self.code_input.toPlainText()))
			token_stream = CommonTokenStream(lexer)
			parser = CompiscriptParser(token_stream)
			program = parser.program()
			tac = TAC_Generator(self.table_classes, self.table_functions, self.table_variables, program, TAC_INFO)
			self.tac_output.append(str(tac.output).strip())
			QTimer.singleShot(50, lambda: (
				self.tac_output.verticalScrollBar().setValue(0),
				self.tac_output.horizontalScrollBar().setValue(0)
			))
		except Exception as e:
			self.tac_highlight = Python_Syntax_Highlighter(self.tac_output.document())
			self.tac_output.append(str(traceback.format_exc()).strip())
			QTimer.singleShot(50, lambda: (
				self.tac_output.verticalScrollBar().setValue(self.tac_output.verticalScrollBar().maximum()),
				self.tac_output.horizontalScrollBar().setValue(0)
			))

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./Resources/RobotoMono-Medium.ttf")
app.setStyleSheet(open("./Resources/QStyleSheet.css", "r").read())
Window = Display()
Window.showMaximized()
sys.exit(app.exec())