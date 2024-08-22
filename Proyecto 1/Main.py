from Semantic_Analyzer import *

class Display(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Semantic Compiler")


		self.code_input = QTextEdit()
		self.code_input.setPlaceholderText("Code to compile...")
		self.code_input.setText("""var suma = 1 + 2;
var resta = 5 - 3;
var producto = 4 * 2;
var division = 8 / 2;""")

		self.code_output = QTextBrowser()
		self.code_output.setPlaceholderText("Compiled code")

		self.log = QTextBrowser()
		self.log.setPlaceholderText("Log")

		self.table = QTableWidget()

		sub = QSplitter(Qt.Orientation.Horizontal)
		sub.addWidget(self.log)
		sub.addWidget(self.table)

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
		try:
			resultado = self.compile(codigo)
			self.log.append(G + "Comiplation Succesful" + RESET)
			self.code_output.setText(f"{resultado[0]}")
		except Exception as e:
			self.log.append(R + "Compilation Failed" + RESET)
			self.code_output.setText(str(e))

	def compile(self, code: str):
		try:
			input_stream = InputStream(code)
			lexer = CompiscriptLexer(input_stream)
			self.log.append("Lexer")
			token_stream = CommonTokenStream(lexer)
			self.log.append("Token Stream")
			parser = CompiscriptParser(token_stream)
			self.log.append("Parser")
			tree = parser.program()

			visitor = Semantic_Analyzer(self.log, self.table, parser)
			visitor.visit(tree)
			visitor.nodeTree(tree)
			visitor.symbol_table.init()
			if not os.path.exists("./Output"): os.makedirs("Output")
			visitor.graph.render("Syntax Graph","./Output", False, True, "png")

			return tree.toStringTree(recog=parser), visitor.symbol_table

		except Exception as e:
			raise Exception(f"Compilation Error {e}")

def main():
	QApplication.setAttribute(Qt.ApplicationAttribute.AA_NativeWindows)

	app = QApplication(sys.argv)
	app.setStyleSheet(open("./QStyleSheet.css", "r").read())
	Window = Display()
	Window.showMaximized()
	app.exec()

if __name__ == "__main__":
	main()