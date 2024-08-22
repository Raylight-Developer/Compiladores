from Semantic_Analyzer import *

class Display(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Semantic Compiler")

		self.main_layout = QVBoxLayout()

		self.text_input_code = QTextEdit()
		self.text_input_code.setPlaceholderText("Code to compile...")
		self.text_input_code.setText("""var suma = 1 + 2;
var resta = 5 - 3;
var producto = 4 * 2;
var division = 8 / 2;""")
		self.main_layout.addWidget(self.text_input_code)

		self.text_output_compiled_code = QTextBrowser()
		self.text_output_compiled_code.setPlaceholderText("Compiled code")
		self.main_layout.addWidget(self.text_output_compiled_code)

		self.log = QTextBrowser()
		self.log.setPlaceholderText("Log")

		self.table = QTableWidget()
	
		sub = QHBoxLayout()
		sub.addWidget(self.log)
		sub.addWidget(self.table)
		self.main_layout.addLayout(sub)

		self.button_compile = QPushButton("Compile")
		self.button_compile.clicked.connect(self.parse)
		self.main_layout.addWidget(self.button_compile)

		self.central_widget = QWidget()
		self.central_widget.setLayout(self.main_layout)

		self.setCentralWidget(self.central_widget)

	def parse(self):
		codigo = self.text_input_code.toPlainText()
		self.text_output_compiled_code.clear()
		self.log.clear()
		try:
			resultado = self.compile(codigo)
			self.log.append(G + "Comiplation Succesful" + RESET)
			self.text_output_compiled_code.setText(f"{resultado[0]}")
		except Exception as e:
			self.log.append(R + "Compilation Failed" + RESET)
			self.text_output_compiled_code.setText(str(e))

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
	app = QApplication(sys.argv)
	app.setStyleSheet(open("./QStyleSheet.css", "r").read())
	Window = Display()
	Window.showMaximized()
	app.exec()

if __name__ == "__main__":
	main()