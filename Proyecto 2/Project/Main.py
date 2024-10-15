from GUI.QT import*
from GUI.Syntax_Highlighting import *

from Intermediate_Code.TAC import *

TAC_INFO = False

class Display(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Compiler")

		self.code_input = Input()
		self.code_number = LineNumberWidget(self.code_input)
		self.code_input.setPlaceholderText("Code to compile...")
		Syntax_Highlighter(self.code_input.document())
		self.code_input.setPlainText(open("./Tests/Ejemplo1.cspt", "r", -1, "utf-8").read())
		self.tac_output = Logger()
		self.tac_output.setPlaceholderText("TAC code")
		TAC_Syntax_Highlighter(self.tac_output.document())
		self.tac_number = LineNumberWidget(self.tac_output)

		self.debug_output = Logger()
		self.debug_output.setPlaceholderText("Debug output")
		self.debug_output.setTabStopDistance(10)
		PYT_Syntax_Highlighter(self.debug_output.document())

		self.tables = QTabWidget()

		self.table_classes   = Symbol_Table("Classes")
		self.table_functions = Symbol_Table("Functions")
		self.table_variables = Symbol_Table("Variables")

		self.tables.addTab(self.table_classes  , QIcon(), "Classes")
		self.tables.addTab(self.table_functions, QIcon(), "Functions")
		self.tables.addTab(self.table_variables, QIcon(), "Variables")

		tablayout = QHBoxLayout()
		tablayout.setContentsMargins(12,12,12,12)
		tablayout.addWidget(self.tables)
		tabcontainer = QWidget()
		tabcontainer.setObjectName("Table")
		tabcontainer.setLayout(tablayout)

		self.sub = QSplitter(Qt.Orientation.Vertical)
		self.sub.addWidget(self.debug_output)
		self.sub.addWidget(tabcontainer)

		h_layout = QHBoxLayout()
		h_layout.addWidget(self.code_number)
		h_layout.addWidget(self.code_input)
		h_layout.setContentsMargins(0,0,0,0)
		h_widget = QWidget()
		h_widget.setContentsMargins(0,0,0,0)
		h_widget.setLayout(h_layout)
		
		h2_layout = QHBoxLayout()
		h2_layout.addWidget(self.tac_number)
		h2_layout.addWidget(self.tac_output)
		h2_layout.setContentsMargins(0,0,0,0)
		h2_widget = QWidget()
		h2_widget.setContentsMargins(0,0,0,0)
		h2_widget.setLayout(h2_layout)
		
		self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
		self.main_splitter.addWidget(h_widget)
		self.main_splitter.addWidget(h2_widget)
		self.main_splitter.addWidget(self.sub)

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
		self.tac_output.clear()
		self.debug_output.clear()
		self.table_classes.clean()
		self.table_functions.clean()
		self.table_variables.clean()

		try:
			lexer = CompiscriptLexer(InputStream(self.code_input.toPlainText()))
			token_stream = CommonTokenStream(lexer)
			parser = CompiscriptParser(token_stream)
			parser.removeErrorListeners()
			parser.addErrorListener(MyErrorListener())
			program = parser.program()
			tac = TAC_Generator(self.table_classes, self.table_functions, self.table_variables, program, TAC_INFO)
			self.table_classes.end()
			self.table_functions.end()
			self.table_variables.end()
			self.tac_output.setPlainText(str(tac.output).strip())
			QTimer.singleShot(50, lambda: (
				self.tac_output.verticalScrollBar().setValue(0),
				self.tac_output.horizontalScrollBar().setValue(0),
				self.sub.setSizes([0,500]),
				self.main_splitter.setSizes([500,500,500])
			))
		except Exception as e:
			self.debug_output.setPlainText(str(traceback.format_exc())+"\n\n\n"+str(e))
			QTimer.singleShot(50, lambda: (
				self.tac_output.verticalScrollBar().setValue(self.tac_output.verticalScrollBar().maximum()),
				self.tac_output.horizontalScrollBar().setValue(0),
				self.sub.setSizes([500,0]),
				self.main_splitter.setSizes([500,0,500])
			))

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./Resources/RobotoMono-Medium.ttf")
app.setStyleSheet(open("./Resources/QStyleSheet.css", "r").read())
Window = Display()
Window.showMaximized()
sys.exit(app.exec())