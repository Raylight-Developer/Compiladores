package com.compiler;

import com.compiler.CompiScript.*;
import com.compiler.CompiScript.CompiScriptParser.ProgramContext;
import com.compiler.GUI.*;

import org.antlr.v4.runtime.*;

import io.qt.widgets.*;
import io.qt.core.*;
import io.qt.gui.*;

import java.util.*;

class Display extends QMainWindow {
	private QTextEdit codeInput;
	private Logger codeOutput;
	private Logger log;
	private QTabWidget tables;
	private Symbol_Table_Classes   tableClasses;
	private Symbol_Table_Functions tableFunctions;
	private Symbol_Table_Variables tableVariables;
	private Map<String, String> options;

	public Display() {
		String[] args = QApplication.arguments().toArray(new String[0]);

		setWindowTitle("Semantic Compiler");

		codeInput = new QTextEdit();
		codeInput.setTabStopDistance(40);
		codeInput.setPlaceholderText("Code to compile...");
		new Syntax_Highlighter(codeInput.document());
		codeInput.setText("""
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
				}

				estudiar() {
					print this.nombre + " esta estudiando en " + this.grado + " grado.";
				}
			}

			var nombre = "Erick";
			var ropero = new Persona(nombre, 20);
			var juan = new Estudiante(nombre, 20, 3);
			juan.saludar();  // Salida: Hola, mi nombre es Juan
			juan.estudiar(); // Salida: Juan esta estudiando en 3 grado

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
			}
			""");

		codeOutput = new Logger();
		codeOutput.setPlaceholderText("Compiled code");

		log = new Logger();
		log.setPlaceholderText("Log");

		tables = new QTabWidget();

		tableClasses   = new Symbol_Table_Classes  ();
		tableFunctions = new Symbol_Table_Functions();
		tableVariables = new Symbol_Table_Variables();

		tables.addTab(tableClasses  , new QIcon(), "Classes"  );
		tables.addTab(tableFunctions, new QIcon(), "Functions");
		tables.addTab(tableVariables, new QIcon(), "Variables");

		QHBoxLayout tableLayout = new QHBoxLayout();
		tableLayout.setContentsMargins(12, 12, 12, 14);
		tableLayout.addWidget(tables);
		QWidget tabContainer = new QWidget();
		tabContainer.setObjectName("Table");
		tabContainer.setLayout(tableLayout);

		QSplitter sub = new QSplitter(Qt.Orientation.Vertical);
		sub.addWidget(log);
		sub.addWidget(tabContainer);

		QSplitter mainSplitter = new QSplitter(Qt.Orientation.Horizontal);
		mainSplitter.addWidget(codeInput);
		mainSplitter.addWidget(sub);
		mainSplitter.addWidget(codeOutput);
		mainSplitter.setSizes(Arrays.asList(500, 500, 200));

		QPushButton buttonCompile = new QPushButton("Compile");
		buttonCompile.clicked.connect(this, "parse()");

		QVBoxLayout mainLayout = new QVBoxLayout();
		mainLayout.addWidget(mainSplitter);
		mainLayout.addWidget(buttonCompile);

		QWidget widget = new QWidget();
		widget.setObjectName("Background");
		widget.setLayout(mainLayout);

		setCentralWidget(widget);

		QTimer.singleShot(200, () -> {
			tableClasses.resizeColumnsToContents();
			tableFunctions.resizeColumnsToContents();
			tableVariables.resizeColumnsToContents();
		});
	}

	private void parse() {
		String code = codeInput.toPlainText();
		codeOutput.clear();
		log.clear();
		try {
			String result = compile(code);
			log.append("<span style='color:green'>Compilation Successful</span>");
			codeOutput.insertPlainText(result);
		} catch (Exception e) {
			log.append("<span style='color:red'>Compilation Failed</span><br><br>" + e.getMessage() + "<br>");
			codeOutput.insertPlainText(e.getMessage());
		}
	}

	private String compile(String code) throws Exception {
		log.append("Compiling...");
		tableFunctions.clearContents();
		tableVariables.clearContents();
		tableClasses.clearContents();
		tableFunctions.setRowCount(0);
		tableVariables.setRowCount(0);
		tableClasses.setRowCount(0);

		try {
			// Initialize your lexer and parser
			CompiScriptLexer lexer = new CompiScriptLexer(new ANTLRInputStream(code));
			CommonTokenStream tokenStream = new CommonTokenStream(lexer);
			CompiScriptParser parser = new CompiScriptParser(tokenStream);

			// Parse the code
			ProgramContext tree = parser.program();

			Semantic_Analyzer visitor = new Semantic_Analyzer(log, tableClasses, tableFunctions, tableVariables, parser);
			visitor.visit(tree);

			tableClasses.resizeColumnsToContents();
			tableFunctions.resizeColumnsToContents();
			tableVariables.resizeColumnsToContents();

			return tree.toStringTree(parser);

		} catch (Exception e) {
			throw new Exception(e.getMessage());
		}
	}
}

public class Main {
	public static void main(String[] args) {
		QApplication.initialize(args);
		Display window = new Display();
		window.showMaximized();
		QApplication.exec();
	}
}