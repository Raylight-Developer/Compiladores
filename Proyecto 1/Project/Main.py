from GUI.Logger import*
from GUI.Syntax_Highlighting import *
from Analyzer.Semantic_Analyzer import *
from Analyzer.SyntaxErrorListener import *

class Display(QMainWindow):
	def __init__(self):
		super().__init__()
		args = sys.argv[1:]
		self.options = parse_args(args)

		self.setWindowTitle("Semantic Compiler")

		self.code_input = QTextEdit()
		self.code_input.setTabStopDistance(40)
		self.code_input.setPlaceholderText("Code to compile...")
		self.highlighter = Syntax_Highlighter(self.code_input.document())
		self.code_input.setText("""class Persona {
	init(nombre, edad) {
		this.nombre = nombre;
		this.edad = edad;
		this.color = "rojo";
	}

	saludar() {
		print "Hola, mi nombre es " + this.color;
	}
}

class Estudiante extends Persona {
	init(nombre, edad, grado) {
		super.init(nombre, edad);
		this.grado = grado;
	}

	estudiar() {
		print this.nombre + " esta estudiando en " + this.grado + " grado.";
	}
}

var nombre = "Erick";

var ropero = new Persona(nombre, 20);
var juan = new Estudiante(nombre, 20, 3);
juan.saludar();    // Salida: Hola, mi nombre es Juan
juan.estudiar();   // Salida: Juan esta estudiando en 3 grado

for (var i = 1; i <= 5; i = i + 1) {
	if (i % 2 == 0) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

while (juan.edad < 25) {
	juan.edad = juan.edad + 1;
	print "Edad de Juan: " + juan.edad;
}""")

		self.code_output = Logger()
		Antlr_Syntax_Highlighter(self.code_output.document())
		self.code_output.setPlaceholderText("Compiled code")

		self.log = Logger()
		self.log.setPlaceholderText("Log")

		self.tables = QTabWidget()

		self.table_classes   = Symbol_Table("Classes")
		self.table_functions = Symbol_Table("Functions")
		self.table_variables = Symbol_Table("Variables")

		self.tables.addTab(self.table_classes  , QIcon(), "Classes")
		self.tables.addTab(self.table_functions, QIcon(), "Functions")
		self.tables.addTab(self.table_variables, QIcon(), "Variables")

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
		
		QTimer.singleShot(200, lambda: (
			self.table_classes.resizeColumnsToContents(),
			self.table_functions.resizeColumnsToContents(),
			self.table_variables.resizeColumnsToContents()
		))

	def parse(self):
		codigo = self.code_input.toPlainText()
		self.code_output.clear()
		self.log.clear()
		try:
			resultado = self.compile(codigo)
			self.log.append(f"{G}Comiplation Succesful{RESET}")
			self.code_output.insertPlainText(resultado)
		except Exception as e:
			self.log.append(f"{R}Compilation Failed{RESET}<br><br>{e}<br>{traceback.format_exc()}")
			self.code_output.insertPlainText(str(e))

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

			analyzer = Semantic_Analyzer(self.table_classes, self.table_functions, self.table_variables, parser)
			analyzer.visit(tree)

			if self.options["render"]:
				if not os.path.exists("./Output"):
					os.makedirs("Output")
				analyzer.nodeTree(tree)
				analyzer.graph.render("Syntax-Graph","./Output", False, True, "png")

			self.table_classes.resizeColumnsToContents()
			self.table_functions.resizeColumnsToContents()
			self.table_variables.resizeColumnsToContents()

			self.log.debug(str(analyzer.debug).strip())

			return tree.toStringTree(recog=parser)

		except Exception as e:
			raise Exception(str(e))


app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./Resources/RobotoMono-Medium.ttf")
app.setStyleSheet(open("./Resources/QStyleSheet.css", "r").read())
Window = Display()
Window.showMaximized()
app.exec()