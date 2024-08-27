from Semantic_Analyzer import *
from SyntaxErrorListener import *

class Display(QMainWindow):
    """
    Clase Display para la interfaz gráfica del compilador semántico.

    Esta clase crea la ventana principal de la aplicación, que permite al usuario ingresar código Compiscript,
    compilarlo y ver los resultados. Los resultados incluyen el código compilado, los registros de logs y una tabla de símbolos.
    """

    def __init__(self):
        """
        Inicializa la ventana principal de la aplicación del compilador semántico.

        Este método configura el área de entrada de código, el área de salida para el código compilado, los registros de logs y la tabla de símbolos.
        También configura el diseño de la interfaz y el botón de Compilar.
        """
        super().__init__()
        self.setWindowTitle("Semantic Compiler")

        # Área de entrada para el código Compiscript
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("Código para compilar...")
        self.code_input.setText("""var suma = 1 + 2;
var resta = 5 - 3;
var producto = 4 * 2;
var division = 8 / 2;""")

        # Área de salida para el código compilado
        self.code_output = QTextBrowser()
        self.code_output.setPlaceholderText("Código compilado")

        # Área de logs para mostrar mensajes de compilación
        self.log = QTextBrowser()
        self.log.setPlaceholderText("Log")

        # Tabla para mostrar la tabla de símbolos
        self.table = QTableWidget()

        # Divisores para organizar el diseño de la interfaz
        sub = QSplitter(Qt.Orientation.Horizontal)
        sub.addWidget(self.log)
        sub.addWidget(self.table)

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.addWidget(self.code_input)
        main_splitter.addWidget(self.code_output)
        main_splitter.addWidget(sub)

        # Botón de Compilar para iniciar el proceso de compilación
        button_compile = QPushButton("Compilar")
        button_compile.clicked.connect(self.parse)

        # Configuración del diseño principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(main_splitter)
        main_layout.addWidget(button_compile)

        # Configuración del widget central de la ventana principal
        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

    def parse(self):
        """
        Analiza el código Compiscript ingresado por el usuario.

<<<<<<< HEAD
	def compile(self, code: str):
		try:
			lexer = CompiscriptLexer(InputStream(code))
			self.log.append("Lexer")

			token_stream = CommonTokenStream(lexer)
			self.log.append("Token Stream")

			parser = CompiscriptParser(token_stream)
			self.log.append("Parser")
			tree = parser.program()

			visitor = Semantic_Analyzer(self.log, self.table, parser)
			visitor.visit(tree)
			visitor.symbol_table.init()

			if not os.path.exists("./Output"):
				os.makedirs("Output")
			visitor.nodeTree(tree)
			visitor.graph.render("Syntax Graph","./Output", False, True, "png")
=======
        Este método limpia la salida y los logs anteriores, luego intenta compilar el código.
        Si tiene éxito, muestra los resultados en las áreas de log y salida.
        """
        codigo = self.code_input.toPlainText()
        self.code_output.clear()
        self.log.clear()
        try:
            resultado = self.compile(codigo)
            self.log.append(G + "Compilación exitosa" + RESET)
            self.code_output.setText(f"{resultado[0]}")
        except Exception as e:
            self.log.append(R + "Compilación fallida" + RESET)
            self.code_output.setText(str(e))

>>>>>>> 26f1dcc (Modificaciones para las tablas, funciona para variables, flata para mucho mas)

    def compile(self, code: str):
        """
        Compila el código Compiscript proporcionado.

        Este método crea el lexer, el parser y el visitor (analizador semántico) para el código.
        Luego genera el árbol de sintaxis y lo renderiza como una imagen. Finalmente, inicializa
        la tabla de símbolos y devuelve el árbol como una cadena.

        :param code: El código Compiscript a compilar.
        :return: Una tupla que contiene la representación en cadena del árbol de sintaxis y la tabla de símbolos.
        :raises Exception: Si ocurre algún error durante el proceso de compilación.
        """
        try:
            # Crear el lexer y parser
            input_stream = InputStream(code)
            lexer = CompiscriptLexer(input_stream)
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
            # Crear el visitor del analizador semántico
            visitor = Semantic_Analyzer(self.log, self.table, parser)
            visitor.visit(tree)
            visitor.nodeTree(tree)
            visitor.symbol_table.init()

            # Renderizar el árbol de sintaxis como imagen
            if not os.path.exists("./Output"): os.makedirs("Output")
            visitor.graph.render("Syntax Graph", "./Output", False, True, "png")

            return tree.toStringTree(recog=parser), visitor.symbol_table

        except Exception as e:
            raise Exception(f"Error de compilación: {e}")

<<<<<<< HEAD

#QApplication.setAttribute(Qt.ApplicationAttribute.AA_NativeWindows)
app = QApplication(sys.argv)
app.setStyleSheet(open("./QStyleSheet.css", "r").read())
Window = Display()
Window.showMaximized()
app.exec()
=======
def main():
    """
    Punto de entrada principal de la aplicación.

    Esta función configura la QApplication, aplica estilos y muestra la ventana principal.
    """
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_NativeWindows)

    app = QApplication(sys.argv)
    app.setStyleSheet(open("./QStyleSheet.css", "r").read())
    Window = Display()
    Window.showMaximized()
    app.exec()

if __name__ == "__main__":
    main()
>>>>>>> 26f1dcc (Modificaciones para las tablas, funciona para variables, flata para mucho mas)
