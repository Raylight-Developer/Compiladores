from GUI.Logger import*
from GUI.Syntax_Highlighting import *

from Analyzer.Semantic_Analyzer import *
from Intermediate_Code.TAC import *

INFO = True

class Display(QMainWindow):
	def __init__(self):
		super().__init__()
		args = sys.argv[1:]
		self.options = parse_args(args)

		self.setWindowTitle("Semantic Compiler")

		self.code_input = QTextEdit()
		self.code_input.setTabStopDistance(40)
		self.code_input.setPlaceholderText("Code to compile...")
		Syntax_Highlighter(self.code_input.document())
		self.code_input.setText((
"""
class Persona {
	init(nombre, edad) {
		this.nombre = nombre;
		this.edad = edad;
		this.color = "rojo";
	}

	saludar() {
		print "Hola, mi nombre es " + this.nombre;
	}

	incrementarEdad(anos) {
		this.edad = this.edad + anos;
		print "Ahora tengo " + this.edad + " años.";
	}
}

class Estudiante extends Persona {
	init(nombre, edad, grado) {
		super.init(nombre, edad);
		this.grado = grado;
	}

	estudiar() {
		print this.nombre + " está estudiando en " + this.grado + " grado.";
	}

	promedioNotas(nota1, nota2, nota3) {
		var promedio = (nota1 + nota2 + nota3) / 3;
		print "El promedio de " + this.nombre + " es " + promedio;
	}
}

var nombre = "Erick";

var juan = new Estudiante(nombre, 20, 3);
juan.saludar();    // Salida: Hola, mi nombre es Erick
juan.estudiar();   // Salida: Erick está estudiando en 3 grado
juan.incrementarEdad(5);

for (var i = 1; i <= 5; i = i + 1) {
	if (i % 2 == 0) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

// Expresión aritmética
var resultado = (juan.edad * 2) + (5 - 3) / 2;
print "Resultado de la expresión: " + resultado;
""").strip())
		self.tac_output = Logger()
		self.tac_output.setPlaceholderText("TAC code")
		self.tac_highlight = TAC_Syntax_Highlighter(self.tac_output.document())

		self.sam_output = Logger()
		self.sam_output.setPlaceholderText("SAM output")
		self.sam_output.setTabStopDistance(10)
		self.sam_highlight = SAM_Syntax_Highlighter(self.sam_output.document())

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
		sub.addWidget(self.sam_output)
		sub.addWidget(tabcontainer)

		self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
		self.main_splitter.addWidget(self.code_input)
		self.main_splitter.addWidget(self.tac_output)
		self.main_splitter.addWidget(sub)
		self.main_splitter.setSizes([500,500,0])

		button_compile = QPushButton("Compile")
		button_compile.clicked.connect(self.compile)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.main_splitter)
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
		self.tac_output.clear()
		self.sam_output.clear()
		
		self.tac_highlight = TAC_Syntax_Highlighter(self.tac_output.document())
		self.sam_highlight = SAM_Syntax_Highlighter(self.sam_output.document())

		self.sam_output.append("Compiling...\n{")
		self.table_functions.clearContents()
		self.table_variables.clearContents()
		self.table_classes.clearContents()
		self.table_functions.setRowCount(0)
		self.table_variables.setRowCount(0)
		self.table_classes.setRowCount(0)

#		try:
#			lexer = CompiscriptLexer(InputStream(self.code_input.toPlainText()))
#			token_stream = CommonTokenStream(lexer)
#			parser = CompiscriptParser(token_stream)
#			program = parser.program()
#			sma = Semantic_Analyzer(self.table_classes, self.table_functions, self.table_variables, program)
#
#			self.table_classes.resizeColumnsToContents()
#			self.table_functions.resizeColumnsToContents()
#			self.table_variables.resizeColumnsToContents()
#
#			if sma.output.error:
#				self.sam_output.append("\t" + str(sma.output).strip())
#				self.sam_output.append("}" + f"\n{R} Compilation Failed")
#				self.main_splitter.setSizes([self.main_splitter.sizes()[0], self.main_splitter.sizes()[1], 500])
#				QTimer.singleShot(100, lambda: (
#					self.sam_output.verticalScrollBar().setValue(0),
#					self.sam_output.horizontalScrollBar().setValue(0),
#					self.tac_output.verticalScrollBar().setValue(self.tac_output.verticalScrollBar().maximum()),
#					self.tac_output.horizontalScrollBar().setValue(0)
#				))
#			else:
#				self.sam_output.append("\t" + str(sma.output).strip())
#				self.sam_output.append("}" + f"\n{G} Comiplation Succesful")
#				QTimer.singleShot(100, lambda: (
#					self.sam_output.verticalScrollBar().setValue(0),
#					self.sam_output.horizontalScrollBar().setValue(0)
#				))
#				self.main_splitter.setSizes([self.main_splitter.sizes()[0], self.main_splitter.sizes()[1], 0])
#
#
#		except Exception as e:
#			self.sam_highlight = Python_Syntax_Highlighter(self.sam_output.document())
#			self.sam_output.append("\t" + str(traceback.format_exc()).strip())
#			self.sam_output.append("}" + f"\n{R} Compilation Failed")
#			self.sam_output.append(str(e))
#			self.main_splitter.setSizes([self.main_splitter.sizes()[0], self.main_splitter.sizes()[1], 500])
#			QTimer.singleShot(100, lambda: (
#				self.sam_output.verticalScrollBar().setValue(self.sam_output.verticalScrollBar().maximum()),
#				self.sam_output.horizontalScrollBar().setValue(0)
#			))

		try:
			lexer = CompiscriptLexer(InputStream(self.code_input.toPlainText()))
			token_stream = CommonTokenStream(lexer)
			parser = CompiscriptParser(token_stream)
			program = parser.program()
			tac = TAC_Generator(program, INFO)
			self.tac_output.append(str(tac.output).strip())
			QTimer.singleShot(100, lambda: (
				self.tac_output.verticalScrollBar().setValue(0),
				self.tac_output.horizontalScrollBar().setValue(0)
			))
		except Exception as e:
			self.tac_highlight = Python_Syntax_Highlighter(self.tac_output.document())
			self.tac_output.append(str(traceback.format_exc()).strip())
			QTimer.singleShot(100, lambda: (
				self.tac_output.verticalScrollBar().setValue(self.tac_output.verticalScrollBar().maximum()),
				self.tac_output.horizontalScrollBar().setValue(0)
			))

app = QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("./Resources/RobotoMono-Medium.ttf")
app.setStyleSheet(open("./Resources/QStyleSheet.css", "r").read())
Window = Display()
Window.showMaximized()
app.exec()