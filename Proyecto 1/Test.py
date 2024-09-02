from Logger import*
from Editor import *
from Tests.Large_Tests import *
from Tests.Small_Tests import *
from Semantic_Analyzer import *
from SyntaxErrorListener import *

class Tester(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Semantic Compiler")

		self.code_output = Logger(False)
		self.code_output.setPlaceholderText("Compiled code")

		self.log = Logger(False)
		self.log.setPlaceholderText("Log")

		self.table_functions : List[Symbol_Table] = []
		self.table_variables : List[Symbol_Table] = []
		self.table_classes   : List[Symbol_Table] = []

		self.tabs = QTabWidget()
		self.tabs.currentChanged.connect(self.on_tab_changed)
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

		self.code = getSmallCode() + getFullCode() # Full Test
		self.succeses = 0
		self.title_failures = []
		self.title_succeses = []
		self.parse()

	def parse(self):
		for i, (title, should_pass, code) in enumerate(self.code):
			self.log.append(f"<h2>{title}</h2>")
			self.log.append(f"Compiling [{i}]...")
			self.log.append(f"{TEST}<pre>{code}</pre>{RESET}")
			try:
				resultado = self.compile(i, code)
				self.log.append(f"{G}[{i}] Comiplation Succesful{RESET}<br><br>")
				self.code_output.insertPlainText(f"[{i}] {resultado}\n\n")
				self.succeses += 1
				self.title_succeses.append(title)
			except Exception as e:
				output = f'<br>{TAB}{TAB}'.join(self.log.debug_output)
				if should_pass == False:
					self.succeses += 1
					self.title_succeses.append(title)
					self.log.append(f"{G}[{i}] Compilation ''Succesful''{RESET}{Y}(Should fail){RESET} {{<br>{HTAB}{e}<br><br>{TAB}Debug View:<br>{TAB}{TAB}{output}<br>}}<br>")
					self.code_output.insertPlainText(f"[{i}] {e}\n\n")
				else:
					self.log.append(f"{R}[{i}] Compilation Failed{RESET} {{<br>{HTAB}{e}<br><br>{TAB}Debug View:<br>{TAB}{TAB}{output}<br>}}<br>")
					self.code_output.insertPlainText(f"[{i}] {e}\n\n")
					self.title_failures.append(title)

		self.log.append("<h2># Summary</h2>")
		self.log.append(f"TESTS:  {len(self.code)}")
		self.log.append(f"{G}PASSED:{RESET} {self.succeses}")
		self.log.append(f"{R}FAILED:{RESET} {len(self.code) - self.succeses}")
		self.log.append(f"Passed:<br>{TAB}" + f"<br>{TAB}".join(self.title_succeses))
		self.log.append(f"Failed:<br>{TAB}" + f"<br>{TAB}".join(self.title_failures))

	def on_tab_changed(self):
		if self.tabs.currentIndex() != 0:
			self.tabs.currentWidget().widget(0).resizeColumnsToContents()
			self.tabs.currentWidget().widget(1).resizeColumnsToContents()
			self.tabs.currentWidget().widget(2).resizeColumnsToContents()

	def compile(self, i: int, code: str) -> str:
		self.table_functions.append(Symbol_Table(self.log, "Fun"))
		self.table_variables.append(Symbol_Table(self.log, "Var"))
		self.table_classes  .append(Symbol_Table(self.log, "Cla"))

		splitter = QSplitter()
		splitter.addWidget(self.table_classes  [-1])
		splitter.addWidget(self.table_functions[-1])
		splitter.addWidget(self.table_variables[-1])
		self.tabs.addTab(splitter, f"Test [{i}]")

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
			raise Exception(str(e))


app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./RobotoMono-Medium.ttf")
app.setStyleSheet(open("./QStyleSheet.css", "r").read())
Window = Tester()
Window.showMaximized()
app.exec()