from GUI.Syntax_Highlighting import *
from GUI.Logger import*

from Tests.Final_Tests import *
from Tests.Large_Tests import *
from Tests.Small_Tests import *

from Analyzer.Semantic_Analyzer import *

class Tester(QMainWindow):
	def __init__(self):
		super().__init__()
		args = sys.argv[1:]
		self.options = parse_args(args)
		self.setWindowTitle("Semantic Compiler")

		self.code_output = Test_Logger()

		self.log = Test_Logger()
		self.debug = Lace()

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

		self.code = getFinalCode()#getSmallCode() + getFullCode() # Full Test
		self.title_failures = []
		self.title_succeses = []
		QTimer.singleShot(50, lambda: self.parse())

	def parse(self):
		for i, (title, should_pass, code, expected_classes, expected_functions, expected_variables) in enumerate(self.code):
			title_id = title.split()[1]
			self.log.append(f"<h2>{title}</h2>")
			self.log.append("CODE: {")
			self.log.addCode(code.strip(), 1)
			self.log.append("}")
			self.log.append(f"<h4>Compiling [{i}] - ({title_id})...</h4>")
			result, output, error = self.compile(i, code, title_id)
			if result:
				self.code_output.append(f"<br>{G}[{i}] - ({title_id}){RESET}")
				self.code_output.insertPlainText(f"\n{output}\n", 1)
				if should_pass:
					self.log.append(f"{G}Compilation Succesful{RESET}<br>")
					self.title_succeses.append((i, title, expected_classes, expected_functions, expected_variables))
					self.log.addCollapse(f"Debug Output [{i}] - ({title_id})", self.debug)
				else:
					self.title_failures.append((i, title, expected_classes, expected_functions, expected_variables))
					self.log.append(f"{R}Compilation Failed{RESET}{Y}(Should fail and did not fail){RESET}")
					self.log.addCollapse(f"Debug Output [{i}] - ({title_id})", self.debug)
			else:
				self.code_output.append(f"<br>{R}[{i}] - ({title_id}){RESET}")
				self.code_output.insertPlainText(f"\n{output}\n", 1)
				if should_pass == False:
					self.title_succeses.append((i, title, expected_classes, expected_functions, expected_variables))
					self.log.append(f"{G}Compilation Succesful{RESET}{Y}(Should fail and did fail){RESET}")
					self.log.addCollapse(f"Debug Output [{i}] - ({title_id})", self.debug)
				else:
					self.title_failures.append((i, title, expected_classes, expected_functions, expected_variables))
					self.log.append(f"{R}Compilation Failed{RESET}")
					self.log.addCollapse(f"Debug Output [{i}] - ({title_id})", self.debug)
					self.log.addCollapse(f"Traceback", f"{error}")

			self.log.addSep()
			self.code_output.addSep()

		self.log.append("<h2># Summary</h2>")
		
		Succeses = []
		Warnings = []
		Failures = []
		for i, (title, should_pass, code, expected_classes, expected_functions, expected_variables) in enumerate(self.code):
			existing_classes   = self.tabs.widget(i + 1).widget(1).layout().itemAt(1).widget().rowCount()
			existing_functions = self.tabs.widget(i + 1).widget(2).layout().itemAt(1).widget().rowCount()
			existing_variables = self.tabs.widget(i + 1).widget(3).layout().itemAt(1).widget().rowCount()
			if existing_classes == expected_classes and existing_functions == expected_functions and existing_variables == expected_variables:
				Succeses.append((i, title, f"[{G}{existing_classes}{RESET} == {expected_classes}] | [{G}{existing_functions}{RESET} == {expected_functions}] | [{G}{existing_variables}{RESET} == {expected_variables}]"))
			elif existing_classes == expected_classes or existing_functions == expected_functions or existing_variables == expected_variables:
				existing_classes   = G + str(existing_classes)   + RESET + " ==" if existing_classes   == expected_classes   else Y + str(existing_classes)   + RESET + " !="
				existing_functions = G + str(existing_functions) + RESET + " ==" if existing_functions == expected_functions else Y + str(existing_functions) + RESET + " !="
				existing_variables = G + str(existing_variables) + RESET + " ==" if existing_variables == expected_variables else Y + str(existing_variables) + RESET + " !="
				Warnings.append((i, title, f"[{existing_classes} {expected_classes}] | [{existing_functions} {expected_functions}] | [{existing_variables} {expected_variables}]"))
			else:
				Failures.append((i, title, f"[{R}{existing_classes}{RESET} != {expected_classes}] | [{R}{existing_functions}{RESET} != {expected_functions}] | [{R}{existing_variables}{RESET} != {expected_variables}]"))


		self.log.append("<h3>TABLE TESTS</h3>")
		self.log.append("[INDEX] - (NAME)")
		self.log.append("[Output_Class_Symbol_Count    OPERATOR Expected_Class_Symbol_Count   ] | [Output_Function_Symbol_Count OPERATOR Expected_Function_Symbol_Count] | [Output_Variable_Symbol_Count OPERATOR Expected_Variable_Symbol_Count]", 1)
		self.log.append("Passed:")
		for (i, title, msg) in Succeses:
			self.log.append(f"[{i}] - ({title})", 1)
			self.log.append(msg, 2)
		self.log.append("Warned:")
		for (i, title, msg) in Warnings:
			self.log.append(f"[{i}] - ({title})", 1)
			self.log.append(msg, 2)
		self.log.append("Failed:")
		for (i, title, msg) in Failures:
			self.log.append(f"[{i}] - ({title})", 1)
			self.log.append(msg, 2)

		self.log.append("<h3>RUNTHROUGH TESTS</h3>")
		self.log.append("Passed:")
		for (i, title, expected_classes, expected_functions, expected_variables) in self.title_succeses:
			self.log.append(f"[{i}] - ({title})", 1)
		self.log.append("Failed:")
		for (i, title, expected_classes, expected_functions, expected_variables) in self.title_failures:
			self.log.append(f"[{i}] - ({title})", 1)

		self.log.append("<h3>TABLE TESTS</h3>")
		self.log.append(f"TESTS  #: {len(self.code)}")
		self.log.append(f"{G}PASSED #:{RESET} {len(Succeses)}")
		self.log.append(f"{Y}WARNED #:{RESET} {len(Warnings)}")
		self.log.append(f"{R}FAILED #:{RESET} {len(Failures)}")

		self.log.append("<h3>RUNTHROUGH TESTS</h3>")
		self.log.append(f"TESTS #: {len(self.code)}")
		self.log.append(f"{G}PASSED#:{RESET} {len(self.title_succeses)}")
		self.log.append(f"{R}FAILED#:{RESET} {len(self.title_failures)}")

		self.setCentralWidget(self.widget)
		QTimer.singleShot(50, lambda: (
			self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
		))

	def on_tab_changed(self):
		if self.tabs.currentIndex() != 0:
			self.tabs.currentWidget().widget(1).layout().itemAt(1).widget().resizeColumnsToContents()
			self.tabs.currentWidget().widget(2).layout().itemAt(1).widget().resizeColumnsToContents()
			self.tabs.currentWidget().widget(3).layout().itemAt(1).widget().resizeColumnsToContents()

	def compile(self, i: int, code: str, title_id: str) -> Tuple[bool, str, str]:
		self.debug.clear()
		self.table_classes  .append(Symbol_Table("Classes"))
		self.table_functions.append(Symbol_Table("Functions"))
		self.table_variables.append(Symbol_Table("Variables"))

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

		Text = QTextBrowser()
		Text.setTabStopDistance(40)
		Syntax_Highlighter(Text.document())
		Text.append(code)

		splitter = QSplitter()
		splitter.addWidget(Text)
		splitter.addWidget(w1)
		splitter.addWidget(w2)
		splitter.addWidget(w3)
		self.tabs.addTab(splitter, f"[{i}] - ({title_id})")

		try:
			lexer = CompiscriptLexer(InputStream(code))
			token_stream = CommonTokenStream(lexer)
			parser = CompiscriptParser(token_stream)

			tree = parser.program()

			analyzer = Semantic_Analyzer(self.debug, self.table_classes[-1], self.table_functions[-1], self.table_variables[-1], parser)
			analyzer.visit(tree)

			return True, tree.toStringTree(recog=parser), ""

		except Exception as e:
			return False, e, traceback.format_exc()

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./Resources/RobotoMono-Medium.ttf")
app.setStyleSheet(open("./Resources/QStyleSheet.css", "r").read())
Window = Tester()
Window.showMaximized()
app.exec()