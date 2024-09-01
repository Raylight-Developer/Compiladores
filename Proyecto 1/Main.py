from Editor import *
from Semantic_Analyzer import *
from SyntaxErrorListener import *

RENDER_TREE = False

class Display(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Semantic Compiler")

		self.code_input = QTextEdit()
		self.code_input.setPlaceholderText("Code to compile...")
		self.highlighter = Syntax_Highlighter(self.code_input.document())
		self.code_input.setText("var test = 10 + (3*5);")

		self.code_output = QTextBrowser()
		self.code_output.setPlaceholderText("Compiled code")

		self.log = QTextBrowser()
		self.log.setPlaceholderText("Log")

		self.tables = QTabWidget()

		self.table_functions = Symbol_Table(self.log, "Fun")
		self.table_variables = Symbol_Table(self.log, "Var")
		self.table_classes   = Symbol_Table(self.log, "Cla")

		self.tables.addTab(self.table_functions, QIcon(), "Functions")
		self.tables.addTab(self.table_variables, QIcon(), "Variables")
		self.tables.addTab(self.table_classes, QIcon(), "Classes")

		tablayout = QHBoxLayout()
		tablayout.setContentsMargins(12,12,12,14)
		tablayout.addWidget(self.tables)
		tabcontainer = QWidget()
		tabcontainer.setObjectName("Table")
		tabcontainer.setLayout(tablayout)

		sub = QSplitter(Qt.Orientation.Vertical)
		sub.addWidget(self.log)
		sub.addWidget(tabcontainer)

		main_splitter = QSplitter(Qt.Orientation.Horizontal)
		main_splitter.addWidget(self.code_input)
		main_splitter.addWidget(sub)
		main_splitter.addWidget(self.code_output)
		main_splitter.setSizes([500,500,200])

		button_compile = QPushButton("Compile")
		button_compile.clicked.connect(self.parse)

		main_layout = QVBoxLayout()
		main_layout.addWidget(main_splitter)
		main_layout.addWidget(button_compile)

		widget = QWidget()
		widget.setObjectName("Background")
		widget.setLayout(main_layout)

		self.setCentralWidget(widget)

	def parse(self):
		codigo = self.code_input.toPlainText()
		self.code_output.clear()
		self.log.clear()
		try:
			resultado = self.compile(codigo)
			self.log.append(G + "Comiplation Succesful" + RESET)
			self.code_output.setText(f"{resultado}")
		except Exception as e:
			self.log.append(R + "Compilation Failed" + RESET)
			self.code_output.setText(str(e))

	def compile(self, code: str):
		self.log.append("Compiling...")
		self.table_functions.clearContents()
		self.table_variables.clearContents()
		self.table_classes.clearContents()
		self.table_functions.setRowCount(0)
		self.table_variables.setRowCount(0)
		self.table_classes.setRowCount(0)

		try:
			lexer = CompiscriptLexer(InputStream(code))
			token_stream = CommonTokenStream(lexer)
			parser = CompiscriptParser(token_stream)

			# Añadir el ErrorListener personalizado
			error_listener = SyntaxErrorListener(self.log)
			parser.removeErrorListeners()  # Quitar el listener de errores por defecto
			parser.addErrorListener(error_listener)
			
			tree = parser.program()

			# Si hubo errores de sintaxis, lanzar una excepción
			if error_listener.has_error:
				raise Exception("Error de sintaxis detectado durante la compilación.")

			visitor = Semantic_Analyzer(self.log, self.table_functions, self.table_variables, self.table_classes, parser)
			visitor.visit(tree)

			if not os.path.exists("./Output"):
				os.makedirs("Output")
			visitor.nodeTree(tree)
			if RENDER_TREE: visitor.graph.render("Syntax Graph","./Output", False, True, "png")

			self.table_classes.resizeColumnsToContents()
			self.table_functions.resizeColumnsToContents()
			self.table_variables.resizeColumnsToContents()

			return tree.toStringTree(recog=parser)

		except Exception as e:
			raise Exception(f"Compilation Error {e}")


#QApplication.setAttribute(Qt.ApplicationAttribute.AA_NativeWindows)
app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./RobotoMono-Medium.ttf")
app.setStyleSheet(open("./QStyleSheet.css", "r").read())
Window = Display()
Window.showMaximized()
app.exec()