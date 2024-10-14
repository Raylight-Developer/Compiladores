from Include import *
from GUI.Syntax_Highlighting import *

class Logger(QPlainTextEdit):
	def __init__(self, debug: bool = True, parent: QWidget = None):
		super().__init__(parent)
		self.setTabStopDistance(40)
		self.setObjectName("Main")
		self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
		self.setReadOnly(True)

class Input(QPlainTextEdit):
	def __init__(self):
		super().__init__()
		self.setTabStopDistance(40)
		self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
		self.cursorPositionChanged.connect(self.highlight_current_line)

	def highlight_current_line(self):
		extra_selections = []
		# Check if the selection is not empty and is not multiple characters
		if not self.isReadOnly() and self.textCursor().selectionStart() == self.textCursor().selectionEnd():
			selection = QTextEdit.ExtraSelection()
			line_color = QColor(40,70,70)
			selection.format.setBackground(line_color)
			selection.format.setProperty(QTextFormat.FullWidthSelection, True)
			selection.cursor = self.textCursor()
			selection.cursor.clearSelection()
			extra_selections.append(selection)
		
		# Apply the extra selections
		self.setExtraSelections(extra_selections)

class LineNumberWidget(QWidget):
	def __init__(self, editor):
		super().__init__(editor)
		self.setObjectName("Code")
		self.editor = editor
		self.editor.blockCountChanged.connect(self.update_width)
		self.editor.updateRequest.connect(self.update_area)
		self.update_width(0)

	def update_width(self, _):
		width = self.fontMetrics().horizontalAdvance(str(self.editor.blockCount() + 1)) + 10
		self.setFixedWidth(width)

	def update_area(self, rect, dy):
		if dy:
			self.scroll(0, dy)
		else:
			self.update(0, rect.y(), self.width(), rect.height())

		if rect.contains(self.editor.viewport().rect()):
			self.update_width(0)

	def paintEvent(self, event):
		rect = self.rect().adjusted(0,10,0,-10)
		painter = QPainter(self)
		painter.fillRect(rect, Qt.transparent)

		block = self.editor.firstVisibleBlock()
		block_number = block.blockNumber()
		top = int(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()) + 15
		bottom = top + int(self.editor.blockBoundingRect(block).height())

		while block.isValid() and top <= rect.bottom() - 15:
			if block.isVisible() and bottom >= rect.top():
				number = str(block_number + 1)
				painter.setPen(Qt.white)
				painter.drawText(0, top, self.width(), self.fontMetrics().height(), Qt.AlignRight, number)

			block = block.next()
			top = bottom
			bottom = top + int(self.editor.blockBoundingRect(block).height())
			block_number += 1