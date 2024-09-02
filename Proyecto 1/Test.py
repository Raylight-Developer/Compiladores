from Logger import*
from Editor import *
from Test_Data import *
from Semantic_Analyzer import *
from SyntaxErrorListener import *

class Tester(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Semantic Compiler")

		self.code_output = Logger()
		self.code_output.setPlaceholderText("Compiled code")

		self.log = Logger()
		self.log.setPlaceholderText("Log")

		self.table_functions : List[Symbol_Table] = []
		self.table_variables : List[Symbol_Table] = []
		self.table_classes   : List[Symbol_Table] = []

		self.tabs = QTabWidget()
		splitter = QSplitter()
		splitter.addWidget(self.code_output)
		splitter.addWidget(self.log)
		self.tabs.addTab(splitter, "Main")

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.tabs)
		widget = QWidget()
		widget.setObjectName("Background")
		widget.setLayout(main_layout)

		self.setCentralWidget(widget)

		self.code = getCode()
		self.succeses = 0
		self.parse()

	def parse(self):
		for i, codigo in enumerate(self.code):
			try:
				resultado = self.compile(i, codigo)
				self.log.append(G + f"Comiplation Succesful [{i}]" + RESET + "<br><br>")
				self.code_output.append(f"{resultado}")
				self.succeses += 1
			except Exception as e:
				self.log.append(R + f"Compilation Failed [{i}]" + RESET + "<br><br>")
				self.code_output.append(str(e))
		self.log.append(f"TESTS:  {len(self.code)}")
		self.log.append(G + "PASSED: " + RESET + f"{self.succeses}")
		self.log.append(R + "FAILED: " + RESET + f"{len(self.code) - self.succeses}")

	def compile(self, i: int, code: str):
		self.table_functions.append(Symbol_Table(self.log, "Fun"))
		self.table_variables.append(Symbol_Table(self.log, "Var"))
		self.table_classes  .append(Symbol_Table(self.log, "Cla"))

		splitter = QSplitter()
		splitter.addWidget(self.table_classes  [-1])
		splitter.addWidget(self.table_functions[-1])
		splitter.addWidget(self.table_variables[-1])
		self.tabs.addTab(splitter, f"Test [{i}]")

		self.log.append(f"Compiling [{i}]...")
		self.log.append(TEST + f"<pre>{code}</pre>" + RESET)

		try:
			lexer = CompiscriptLexer(InputStream(code))
			token_stream = CommonTokenStream(lexer)
			parser = CompiscriptParser(token_stream)

			error_listener = SyntaxErrorListener(self.log)
			parser.removeErrorListeners()
			parser.addErrorListener(error_listener)
			
			tree = parser.program()

			if error_listener.has_error:
				raise Exception("Error de sintaxis detectado durante la compilación.")

			visitor = Semantic_Analyzer(self.log, self.table_functions[-1], self.table_variables[-1], self.table_classes[-1], parser)
			visitor.visit(tree)

			self.table_classes  [-1].resizeColumnsToContents()
			self.table_functions[-1].resizeColumnsToContents()
			self.table_variables[-1].resizeColumnsToContents()

			return tree.toStringTree(recog=parser)

		except Exception as e:
			raise Exception(f"Compilation Error for [{i}] {e}")


app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./RobotoMono-Medium.ttf")
app.setStyleSheet(open("./QStyleSheet.css", "r").read())
Window = Tester()
Window.showMaximized()
app.exec()