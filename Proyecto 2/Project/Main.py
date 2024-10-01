from GUI.Logger import*
from GUI.Syntax_Highlighting import *

from Analyzer.Semantic_Analyzer import *
from Intermediate_Code.TAC import *

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
		self.code_input.setText((
"""
/*
fun saludar(val) {
	print "Hola, mi nombre es " + val;
}
var nombre = "Alejandro";
saludar("Alejandro");
saludar(nombre);
*/

var testa = 3;
var testb = "3";
var menor = 3 < 5; // true
var mayorIgual = 10 >= 10; // true
var igual = 1 == 1; // true
var diferente = "a" != "b" ; // true
var y = true and false ; // false
var o = true or false ; // true
var no = ! true ; // false
var min = 0;
var max = 10;
var promedio = ( min + max ) / 2;
/*
var string = "Hola Mundo";

for (var i = 1; i <= 5; i = i + 1) {
	if (i % 2 == 0) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

class Persona {
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
		this.edad = 10;
	}

	estudiar() {
		print this.nombre + " esta estudiando en " + this.grado + " grado.";
	}
}

fun estudiar() {
	print " esta estudiando en grado.";
}
estudiar();
fun saludar(val) {
	print "Hola, mi nombre es " + val;
}
saludar("Alejandro");

var nombre = "Alejandro";

var ropero = new Persona(nombre, 20);
var juan = new Estudiante(nombre, 20, 3);
juan.saludar();    // Salida: Hola, mi nombre es Alejandro
juan.estudiar();   // Salida: Juan esta estudiando en 3 grado
*/
""").strip())
		self.tac_highlighter = None
		self.tac_output = Logger()
		self.tac_output.setPlaceholderText("TAC code")

		self.log = Logger()
		self.log.setPlaceholderText("Log")
		self.log.setTabStopDistance(10)
		self.debug = Lace()
		LOG_Syntax_Highlighter(self.log.document())

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
		main_splitter.addWidget(self.tac_output)
		main_splitter.setSizes([500,500,500])

		button_compile = QPushButton("Compile")
		button_compile.clicked.connect(self.compile)

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
		self.compile()

	def compile(self):
		code = self.code_input.toPlainText()
		self.tac_output.clear()
		self.tac_highlighter = None
		self.debug.clear()
		self.debug.current_tab = 1
		self.log.clear()
	
		self.log.append("Compiling...\n{")
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
			analyzer = Semantic_Analyzer(self.debug, self.table_classes, self.table_functions, self.table_variables, parser.program())

			self.table_classes.resizeColumnsToContents()
			self.table_functions.resizeColumnsToContents()
			self.table_variables.resizeColumnsToContents()

			if not self.debug.error:
				self.log.append("\t" + str(self.debug).strip())
				self.log.append("}" + f"\n{G} Comiplation Succesful")
				self.tac_highlighter = TAC_Syntax_Highlighter(self.tac_output.document())
				self.tac_output.append(str(analyzer.tac.code).strip())

			else:
				self.log.append("\t" + str(self.debug).strip())
				self.log.append("}" + f"\n{R} Compilation Failed")
				self.tac_highlighter = Python_Syntax_Highlighter(self.tac_output.document())
				self.tac_output.clear()

		except Exception as e:
			self.log.append("\t" + str(self.debug).strip())
			self.log.append("}" + f"\n{R} Compilation Failed")
			self.log.append(str(e))
			self.tac_highlighter = Python_Syntax_Highlighter(self.tac_output.document())
			self.tac_output.insertPlainText("\n".join(traceback.format_exc().splitlines()))

		self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
		self.tac_output.verticalScrollBar().setValue(self.tac_output.verticalScrollBar().maximum())

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./Resources/RobotoMono-Medium.ttf")
app.setStyleSheet(open("./Resources/QStyleSheet.css", "r").read())
Window = Display()
Window.showMaximized()
app.exec()