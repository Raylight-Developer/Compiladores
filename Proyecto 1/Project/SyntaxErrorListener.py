from Include import *
from antlr4.error.ErrorListener import ErrorListener

class SyntaxErrorListener(ErrorListener):
	def __init__(self, log: QTextBrowser):
		super(SyntaxErrorListener, self).__init__()
		self.log = log
		self.has_error = False

	def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
		self.has_error = True
		error_message = f"Error de sintaxis en línea {line}, columna {column}: {msg}"
		self.log.append(error_message)