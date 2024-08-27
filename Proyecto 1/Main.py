from Semantic_Analyzer import *

class Display(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Semantic Compiler")

		self.code_input = QTextEdit()
		self.code_input.setPlaceholderText("Code to compile...")
		self.code_input.setText(
"""var test = 10;
""")

		self.code_output = QTextBrowser()
		self.code_output.setPlaceholderText("Compiled code")

		self.log = QTextBrowser()
		self.log.setPlaceholderText("Log")

		self.tables = QTabWidget()

		self.table_functions = Symbol_Table(self.log)
		self.table_variables = Symbol_Table(self.log)
		self.table_classes = Symbol_Table(self.log)

		self.tables.addTab(self.table_functions, QIcon(), "Functions")
		self.tables.addTab(self.table_variables, QIcon(), "Variables")
		self.tables.addTab(self.table_classes, QIcon(), "Classes")

		tablayout = QHBoxLayout()
		tablayout.addWidget(self.tables)
		tabcontainer = QWidget()
		tabcontainer.setLayout(tablayout)

		sub = QSplitter(Qt.Orientation.Horizontal)
		sub.addWidget(self.log)
		sub.addWidget(tabcontainer)

		main_splitter = QSplitter(Qt.Orientation.Vertical)
		main_splitter.addWidget(self.code_input)
		main_splitter.addWidget(self.code_output)
		main_splitter.addWidget(sub)

		button_compile = QPushButton("Compile")
		button_compile.clicked.connect(self.parse)

		main_layout = QVBoxLayout()
		main_layout.addWidget(main_splitter)
		main_layout.addWidget(button_compile)

		widget = QWidget()
		widget.setLayout(main_layout)

		self.setCentralWidget(widget)

	def parse(self):
		codigo = self.code_input.toPlainText()
		self.code_output.clear()
		self.log.clear()
		#try:
		resultado = self.compile(codigo)
		self.log.append(G + "Comiplation Succesful" + RESET)
		self.code_output.setText(f"{resultado[0]}")
		#except Exception as e:
		#	self.log.append(R + "Compilation Failed" + RESET)
		#	self.code_output.setText(str(e))

	def compile(self, code: str):
		#try:
			lexer = CompiscriptLexer(InputStream(code))
			self.log.append("Lexer")

			token_stream = CommonTokenStream(lexer)
			self.log.append("Token Stream")

			parser = CompiscriptParser(token_stream)
			self.log.append("Parser")
			tree = parser.program()

			visitor = Semantic_Analyzer(self.log, self.table_functions, self.table_variables, self.table_classes, parser)
			visitor.visit(tree)

			if not os.path.exists("./Output"):
				os.makedirs("Output")
			visitor.nodeTree(tree)
			visitor.graph.render("Syntax Graph","./Output", False, True, "png")

			return tree.toStringTree(recog=parser)

		#except Exception as e:
		#	raise Exception(f"Compilation Error {e}")


#QApplication.setAttribute(Qt.ApplicationAttribute.AA_NativeWindows)
app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./RobotoMono-Medium.ttf")
app.setStyleSheet(open("./QStyleSheet.css", "r").read())
Window = Display()
Window.showMaximized()
app.exec()