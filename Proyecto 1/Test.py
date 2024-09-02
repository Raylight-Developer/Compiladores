from Logger import*
from Syntax_Highlighting import *
from Tests.Large_Tests import *
from Tests.Small_Tests import *
from Semantic_Analyzer import *
from SyntaxErrorListener import *

class Tester(QMainWindow):
	def __init__(self):
		super().__init__()
		args = sys.argv[1:]
		self.options = parse_args(args)
		self.setWindowTitle("Semantic Compiler")

		self.code_output = Test_Logger(False)

		self.log = Test_Logger(False)

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
		self.widget = QWidget()
		self.widget.setObjectName("Background")
		self.widget.setLayout(main_layout)

		label = QLabel("Compiling...")
		label.setObjectName("FS")
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.setCentralWidget(label)

		self.code = getSmallCode() + getFullCode() # Full Test
		self.succeses = 0
		self.title_failures = []
		self.title_succeses = []
		QTimer.singleShot(50, lambda: self.parse())

	def parse(self):
		for i, (title, should_pass, code) in enumerate(self.code):
			title_id = title.split()[1]
			self.log.append(f"<h2>{title}</h2>")
			self.log.append(f"<h4>Compiling [{i}] - ({title_id})...</h4>")
			self.log.append("CODE: {")
			self.log.addCode(code.strip(), 1)
			self.log.append("}")
			try:
				resultado = self.compile(i, code, title_id)
				self.log.append(f"{G}Compilation Succesful{RESET}<br>")
				self.code_output.insertAntlrText(f"\n[{i}] - ({title_id}) {resultado}\n")
				self.succeses += 1
				self.title_succeses.append(title)
			except Exception as e:
				self.code_output.insertAntlrText(f"\n[{i}] - ({title_id}) {e}\n")
				if should_pass == False:
					self.succeses += 1
					self.title_succeses.append(title)
					self.log.append(f"{G}Compilation ''Succesful''{RESET}{Y}(Should fail and did fail){RESET}" + " {")
				else:
					self.title_failures.append(title)
					self.log.append(f"{R}Compilation Failed{RESET}" + " {")

				self.log.append(f"{e}", 1)
				self.log.append("}")
			debug = "\n".join(self.log.debug_output)
			self.log.addCollapse(f"Debug Output [{i}] - ({title_id})", debug, 1)

			self.log.addSep()
			self.code_output.addSep()

		self.log.append("<h2># Summary</h2>")
		self.log.append(f"TESTS:  {len(self.code)}")
		self.log.append(f"{G}PASSED:{RESET} {self.succeses}")
		self.log.append(f"{R}FAILED:{RESET} {len(self.code) - self.succeses}")
		self.log.append(f"Passed:<br>{TAB}" + f"<br>{TAB}".join(self.title_succeses))
		self.log.append(f"Failed:<br>{TAB}" + f"<br>{TAB}".join(self.title_failures))

		self.setCentralWidget(self.widget)
		QTimer.singleShot(50, lambda: (
			self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
		))

	def on_tab_changed(self):
		if self.tabs.currentIndex() != 0:
			self.tabs.currentWidget().widget(0).layout().itemAt(1).widget().resizeColumnsToContents()
			self.tabs.currentWidget().widget(1).layout().itemAt(1).widget().resizeColumnsToContents()
			self.tabs.currentWidget().widget(2).layout().itemAt(1).widget().resizeColumnsToContents()

	def compile(self, i: int, code: str, title_id: str) -> str:
		self.table_functions.append(Symbol_Table(self.log, "Fun"))
		self.table_variables.append(Symbol_Table(self.log, "Var"))
		self.table_classes  .append(Symbol_Table(self.log, "Cla"))

		l1 = QVBoxLayout()
		l1.addWidget(QLabel("Classes"))
		l1.addWidget(self.table_classes[-1])
		w1 = QWidget()
		w1.setLayout(l1)
		
		l2 = QVBoxLayout()
		l2.addWidget(QLabel("Functions"))
		l2.addWidget(self.table_functions[-1])
		w2 = QWidget()
		w2.setLayout(l2)
		
		l3 = QVBoxLayout()
		w3 = QWidget()
		l3.addWidget(QLabel("Variables"))
		l3.addWidget(self.table_variables[-1])
		w3.setLayout(l3)

		splitter = QSplitter()
		splitter.addWidget(w1)
		splitter.addWidget(w2)
		splitter.addWidget(w3)
		self.tabs.addTab(splitter, f"[{i}] - ({title_id})")

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

			if self.options["render"]:
				if not os.path.exists("./Output/Tests"):
					os.makedirs("Output/Tests")
				visitor.nodeTree(tree)
				visitor.graph.render(f"Syntax-Graph[{i}]-({title_id})","./Output/Tests", False, True, "png")

			self.table_classes  [-1].resizeColumnsToContents()
			self.table_functions[-1].resizeColumnsToContents()
			self.table_variables[-1].resizeColumnsToContents()

			return tree.toStringTree(recog=parser)

		except Exception as e:
			raise e

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./RobotoMono-Medium.ttf")
app.setStyleSheet(open("./QStyleSheet.css", "r").read())
Window = Tester()
Window.showMaximized()
app.exec()