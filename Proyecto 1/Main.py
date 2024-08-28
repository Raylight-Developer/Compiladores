from Editor import *
from Semantic_Analyzer import *
from SyntaxErrorListener import *

class Display(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Semantic Compiler")

		self.code_input = QTextEdit()
		self.code_input.setPlaceholderText("Code to compile...")
		self.highlighter = Syntax_Highlighter(self.code_input.document())
		self.code_input.setText(
"""fun suma(a , b) {
	return a + b ;
}
print suma(3 , 4) ; // Salida : 7

fun esPar(num) {
	return num % 2 == 0;
}
for (var i = 1; i <= 10; i = i + 1) {
	if (esPar( i )) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

class Persona {
	init(nombre , edad) {
		this.nombre = nombre ;
		this.edad = edad ;
	}
	saludar () {
		print "Hola , mi nombre es: " + this.nombre ;
	}
}
class Estudiante extends Persona {
	init(nombre , edad , grado) {
		super.init(nombre , edad);
		this.grado = grado;
	}
	estudiar() {
		print this.nombre + " esta estudiando en " + this . grado + " grado.";
	}
}
var juan = Estudiante ( " Juan " , 20 , 3);
juan.saludar(); // Salida : Hola , mi nombre es Juan
juan.estudiar(); // Salida : Juan esta estudiando en 3 grado
for ( var j = 1; j <= 5; j = j + 1) { // TODO; si es si tiene confilcto
	if ( j % 2 == 0) {
		print j + " es par";
	} else {
		print j + " es impar";
	}
}
while ( juan.edad < 25) {
	juan.edad = juan.edad + 1;
	print "Edad de Juan: " + juan.edad ;
}""")

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
		try:
			resultado = self.compile(codigo)
			self.log.append(G + "Comiplation Succesful" + RESET)
			self.code_output.setText(f"{resultado}")
		except Exception as e:
			self.log.append(R + "Compilation Failed" + RESET)
			self.code_output.setText(str(e))

	def compile(self, code: str):
		#try:
			lexer = CompiscriptLexer(InputStream(code))
			self.log.append("Lexer")

			token_stream = CommonTokenStream(lexer)
			self.log.append("Token Stream")

			parser = CompiscriptParser(token_stream)
			self.log.append("Parser")

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
			visitor.graph.render("Syntax Graph","./Output", False, True, "png")

			self.table_classes.resizeColumnsToContents()
			self.table_functions.resizeColumnsToContents()
			self.table_variables.resizeColumnsToContents()

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