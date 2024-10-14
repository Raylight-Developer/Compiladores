from Include import *

class HighlightingRule:
	def __init__(self, pattern: QRegularExpression = None, format: QTextCharFormat = None):
		self.pattern = pattern
		self.format = format

class Syntax_Highlighter(QSyntaxHighlighter) :
	def __init__(self, parent: QTextDocument = None):
		super().__init__(parent)

		self.highlightingRules: List[HighlightingRule] = []

		self.user_keywords = QTextCharFormat()
		self.user_keywords.setForeground(QColor(86, 156, 214))
		for pattern in [
			"float", "int", "uint", "bool", "class", "struct", "const", "true", "false"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.user_keywords
			)
			self.highlightingRules.append(rule)

		self.control = QTextCharFormat()
		self.control.setForeground(QColor(216, 160, 223))
		for pattern in [
			"if", "else", "else if", "while", "for", "return", "switch", "case", "break", "continue"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.control
			)
			self.highlightingRules.append(rule)

		self.builtinFunctions = QTextCharFormat()
		self.builtinFunctions.setForeground(QColor(225,225,120))
		for pattern in [
			"fun", "print", "init", "var"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.builtinFunctions
			)
			self.highlightingRules.append(rule)

		self.builtinClasses = QTextCharFormat()
		self.builtinClasses.setForeground(QColor(78,201,176))
		for pattern in [
			"super"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.builtinClasses
			)
			self.highlightingRules.append(rule)
		
		self.brackets = QTextCharFormat()
		self.brackets.setForeground(QColor(255,215,0))
		for pattern in [
			r"\(",
			r"\)",
			r"\[",
			r"\]",
			r"\{",
			r"\}"
		]:
			rule = HighlightingRule(
				QRegularExpression(pattern),
				self.brackets
			)
			self.highlightingRules.append(rule)

		self.integers = QTextCharFormat()
		self.integers.setForeground(QColor(181, 206, 168))
		rule = HighlightingRule(QRegularExpression(r"\b[-+]?[0-9]+[uU]?\b"), self.integers)
		self.highlightingRules.append(rule)

		self.floats = QTextCharFormat()
		self.floats.setForeground(QColor(185, 225, 172))
		rule = HighlightingRule(QRegularExpression(r"\b[-+]?([0-9]*\.[0-9]+|[0-9]+\.)([eE][-+]?[0-9]+)?[fF]?\b"), self.floats)
		self.highlightingRules.append(rule)

		self.strings = QTextCharFormat()
		self.strings.setForeground(QColor(214, 157, 133))
		for pattern in [
			r'"([^"\\]|\\.)*"',
			r"'([^'\\]|\\.)*'"
		]:
			rule = HighlightingRule(
				QRegularExpression(pattern),
				self.strings
			)
			self.highlightingRules.append(rule)

		self.comments = QTextCharFormat()
		self.comments.setForeground(QColor(85, 140, 70))
		for pattern in [
			r"//[^\n]*",
			r"/\*.*?\*/"
		]:
			rule = HighlightingRule(
				QRegularExpression(pattern),
				self.comments
			)
			self.highlightingRules.append(rule)

		self.multi_line_start = QRegularExpression(r"/\*")
		self.multi_line_end = QRegularExpression(r"\*/")

	def highlightBlock(self, text: str):
		for rule in self.highlightingRules:
			matchIterator: QRegularExpressionMatchIterator = rule.pattern.globalMatch(text)
			while matchIterator.hasNext():
				match: QRegularExpressionMatch = matchIterator.next()
				self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)

		# Handle multi-line comments
		self.setCurrentBlockState(0)

		start_idx = 0
		if self.previousBlockState() != 1:
			start_match = self.multi_line_start.match(text)
			start_idx = start_match.capturedStart() if start_match.hasMatch() else -1

		while start_idx >= 0:
			end_match = self.multi_line_end.match(text, start_idx)
			end_idx = end_match.capturedEnd() if end_match.hasMatch() else -1

			if end_idx == -1:
				self.setCurrentBlockState(1)  # Comment block continues to the next line
				self.setFormat(start_idx, len(text) - start_idx, self.comments)
				break
			else:
				self.setFormat(start_idx, end_idx - start_idx, self.comments)
				start_match = self.multi_line_start.match(text, end_idx)
				start_idx = start_match.capturedStart() if start_match.hasMatch() else -1

class PYT_Syntax_Highlighter(QSyntaxHighlighter) :
	def __init__(self, parent: QTextDocument = None):
		super().__init__(parent)

		self.highlightingRules: List[HighlightingRule] = []

		self.user_keywords = QTextCharFormat()
		self.user_keywords.setForeground(QColor(86, 156, 214))
		for pattern in [
			"class", "True", "False", "or", "and", "not", "in"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.user_keywords
			)
			self.highlightingRules.append(rule)

		self.control = QTextCharFormat()
		self.control.setForeground(QColor(216, 160, 223))
		for pattern in [
			"if", "else", "elif", "while", "for", "return", "switch", "case", "break", "continue"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.control
			)
			self.highlightingRules.append(rule)

		self.builtinFunctions = QTextCharFormat()
		self.builtinFunctions.setForeground(QColor(225,225,120))
		for pattern in [
			"fun", "print", "init", "var"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.builtinFunctions
			)
			self.highlightingRules.append(rule)

		self.builtinClasses = QTextCharFormat()
		self.builtinClasses.setForeground(QColor(78,201,176))
		for pattern in [
			"float", "int", "uint", "bool", "super"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.builtinClasses
			)
			self.highlightingRules.append(rule)
		
		self.brackets = QTextCharFormat()
		self.brackets.setForeground(QColor(255,215,0))
		for pattern in [
			r"\(",
			r"\)",
			r"\[",
			r"\]",
			r"\{",
			r"\}"
		]:
			rule = HighlightingRule(
				QRegularExpression(pattern),
				self.brackets
			)
			self.highlightingRules.append(rule)

		self.integers = QTextCharFormat()
		self.integers.setForeground(QColor(181, 206, 168))
		rule = HighlightingRule(QRegularExpression(r"\b[-+]?[0-9]+[uU]?\b"), self.integers)
		self.highlightingRules.append(rule)

		self.floats = QTextCharFormat()
		self.floats.setForeground(QColor(185, 225, 172))
		rule = HighlightingRule(QRegularExpression(r"\b[-+]?([0-9]*\.[0-9]+|[0-9]+\.)([eE][-+]?[0-9]+)?[fF]?\b"), self.floats)
		self.highlightingRules.append(rule)

		self.strings = QTextCharFormat()
		self.strings.setForeground(QColor(214, 157, 133))
		for pattern in [
			r'"([^"\\]|\\.)*"',
			r"'([^'\\]|\\.)*'"
		]:
			rule = HighlightingRule(
				QRegularExpression(pattern),
				self.strings
			)
			self.highlightingRules.append(rule)

		self.comments = QTextCharFormat()
		self.comments.setForeground(QColor(85, 140, 70))
		for pattern in [
			r"//[^\n]*",
			r"/\*.*?\*/"
		]:
			rule = HighlightingRule(
				QRegularExpression(pattern),
				self.comments
			)
			self.highlightingRules.append(rule)

	def highlightBlock(self, text: str):
		for rule in self.highlightingRules:
			matchIterator: QRegularExpressionMatchIterator = rule.pattern.globalMatch(text)
			while matchIterator.hasNext():
				match: QRegularExpressionMatch = matchIterator.next()
				self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)

class TAC_Syntax_Highlighter(QSyntaxHighlighter) :
	def __init__(self, parent: QTextDocument = None):
		super().__init__(parent)

		self.highlightingRules: List[HighlightingRule] = []

		self.control = QTextCharFormat()
		self.control.setForeground(QColor(216, 160, 223))
		for pattern in [
			"IF", "GO_TO", "LINK_BACK", "IF_NOT", "SYSCALL", "PRINT", "RETURN", "CALL"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.control
			)
			self.highlightingRules.append(rule)

		self.user_keywords = QTextCharFormat()
		self.user_keywords.setForeground(QColor(86, 156, 214))
		for pattern in [
			"true", "false", "nil", "this"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.user_keywords
			)
			self.highlightingRules.append(rule)

		self.operation = QTextCharFormat()
		self.operation.setForeground(QColor(100, 255, 120))
		for pattern in [
			"ADD", "SUB", "MUL", "DIV", "MOD",
			"AND", "OR", "NOT", "EQ", "NEQ", "LEQ", "GEQ","LT", "GT",
			"ALLOCATE", "MOV"
		]:
			rule = HighlightingRule(
				QRegularExpression(r"\b" + pattern + r"\b"),
				self.operation
			)
			self.highlightingRules.append(rule)
			
		self.label = QTextCharFormat()
		self.label.setForeground(QColor(255, 120, 100))
		rule = HighlightingRule(
			QRegularExpression(r"\bL_[0-9]*\b"),
			self.label
		)
		self.highlightingRules.append(rule)

		self.temporal = QTextCharFormat()
		self.temporal.setForeground(QColor(120, 130, 140))
		rule = HighlightingRule(
			QRegularExpression(r"\bT_[0-9]*\b"),
			self.temporal
		)
		self.highlightingRules.append(rule)

		self.internal = QTextCharFormat()
		self.internal.setForeground(QColor(120, 220, 220))
		rule = HighlightingRule(
			QRegularExpression(r"\b(IT_|LT_)\S*\b"),
			self.internal
		)
		self.highlightingRules.append(rule)
	
		self.brackets = QTextCharFormat()
		self.brackets.setForeground(QColor(255, 215, 0))
		for pattern in [
			r"\(",
			r"\)",
			r"\[",
			r"\]",
			r"\{",
			r"\}"
		]:
			rule = HighlightingRule(
				QRegularExpression(pattern),
				self.brackets
			)
			self.highlightingRules.append(rule)

		self.integers = QTextCharFormat()
		self.integers.setForeground(QColor(181, 206, 168))
		rule = HighlightingRule(QRegularExpression(r"\b[-+]?[0-9]+[uU]?\b"), self.integers)
		self.highlightingRules.append(rule)

		self.floats = QTextCharFormat()
		self.floats.setForeground(QColor(185, 225, 172))
		rule = HighlightingRule(QRegularExpression(r"\b[-+]?([0-9]*\.[0-9]+|[0-9]+\.)([eE][-+]?[0-9]+)?[fF]?\b"), self.floats)
		self.highlightingRules.append(rule)

		self.strings = QTextCharFormat()
		self.strings.setForeground(QColor(214, 157, 133))
		for pattern in [
			r'"([^"\\]|\\.)*"',
			r"'([^'\\]|\\.)*'"
		]:
			rule = HighlightingRule(
				QRegularExpression(pattern),
				self.strings
			)
			self.highlightingRules.append(rule)

		self.comments = QTextCharFormat()
		self.comments.setForeground(QColor(85, 140, 70))
		for pattern in [
			r"//[^\n]*",
			r"/\*.*?\*/"
		]:
			rule = HighlightingRule(
				QRegularExpression(pattern),
				self.comments
			)
			self.highlightingRules.append(rule)

	def highlightBlock(self, text: str):
		for rule in self.highlightingRules:
			matchIterator: QRegularExpressionMatchIterator = rule.pattern.globalMatch(text)
			while matchIterator.hasNext():
				match: QRegularExpressionMatch = matchIterator.next()
				self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)

class SAM_Syntax_Highlighter(QSyntaxHighlighter) :
	def __init__(self, parent: QTextDocument = None):
		super().__init__(parent)

		self.highlightingRules: List[HighlightingRule] = []

		self.success = QTextCharFormat()
		self.success.setForeground(QColor(100, 255, 100))
		rule = HighlightingRule(
			QRegularExpression(r"\bSUCCESS\s*(.*)\b"),
			self.success
		)
		self.highlightingRules.append(rule)

		self.fail = QTextCharFormat()
		self.fail.setForeground(QColor(255, 100, 100))
		rule = HighlightingRule(
			QRegularExpression(r"\bFAILURE\s*(.*)\b"),
			self.fail
		)
		self.highlightingRules.append(rule)

	def highlightBlock(self, text: str):
		for rule in self.highlightingRules:
			matchIterator: QRegularExpressionMatchIterator = rule.pattern.globalMatch(text)
			while matchIterator.hasNext():
				match: QRegularExpressionMatch = matchIterator.next()
				self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)