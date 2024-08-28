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
			"float", "int", "uint", "bool", "class", "struct", "const"
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
		self.builtinFunctions.setForeground(QColor(214,211,161))
		for pattern in [
			"fun", "print", "init"
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
		self.comments.setForeground(QColor(87, 166, 74))
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
			