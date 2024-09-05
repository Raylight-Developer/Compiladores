package com.compiler.GUI;

import io.qt.widgets.*;
import io.qt.core.*;
import io.qt.gui.*;

import java.util.*;

class Viewer extends QTextBrowser {
	public Viewer() {
		setReadOnly(true);
		setTabStopDistance(40);
		textChanged.connect(this, "autoResize()");
	}

	private void autoResize() {
		document().setTextWidth(viewport().width());
		QMargins margins = contentsMargins();
		int height = (int) (document().size().height() + margins.top() + margins.bottom());
		setFixedHeight(height);
	}

	@Override
	protected void resizeEvent(QResizeEvent event) {
		autoResize();
		super.resizeEvent(event);
	}
}

public class Multi_Logger extends QScrollArea {
	private boolean shouldDebug;
	private List<String> debugOutput;
	private QVBoxLayout contentsLayout;

	public Multi_Logger(boolean debug) {
		this.shouldDebug = debug;
		this.debugOutput = new ArrayList<>();
		this.setWidgetResizable(true);

		contentsLayout = new QVBoxLayout();
		contentsLayout.setAlignment(Qt.AlignmentFlag.AlignTop);
		contentsLayout.setSpacing(0);

		QWidget content = new QWidget();
		content.setContentsMargins(0, 0, 0, 0);
		content.setLayout(contentsLayout);
		setWidget(content);
	}

	public void debug(String value, int indent) {
		if (shouldDebug) {
			Viewer text = new Viewer();
			text.append(value);
			text.setStyleSheet("padding-left: " + (5 + indent * 40) + "px");
			contentsLayout.addWidget(text);
		}
		debugOutput.add(value);
	}

	public void append(String value, int indent) {
		Viewer text = new Viewer();
		text.append(value);
		text.setStyleSheet("padding-left: " + (5 + indent * 40) + "px");
		contentsLayout.addWidget(text);
	}

	public void insertPlainText(String value, int indent) {
		Viewer text = new Viewer();
		text.insertPlainText(value);
		text.setStyleSheet("padding-left: " + (5 + indent * 40) + "px");
		contentsLayout.addWidget(text);
	}

	public void addCode(String value, int indent) {
		Viewer text = new Viewer();
		text.setStyleSheet("padding-left: " + (5 + indent * 40) + "px");
		new Syntax_Highlighter(text.document()); // Placeholder for general syntax highlighting
		text.append(value);
		contentsLayout.addWidget(text);
	}

	public void addCollapse(String title, String value, int indent) {
		QPushButton button = new QPushButton(title);

		Viewer text = new Viewer();
		text.insertPlainText(value);
		new Python_Syntax_Highlighter(text.document()); // Placeholder for Python syntax highlighting
		text.setStyleSheet("margin-left: " + (5 + indent * 40) + "px; background:rgb(50,50,50);");

		QWidget container = new QWidget();
		container.setStyleSheet("margin: 0px; margin-top:4px; margin-bottom:4px;");
		QVBoxLayout layout = new QVBoxLayout();
		layout.setSpacing(0);
		layout.setContentsMargins(0, 0, 0, 0);
		container.setLayout(layout);
		layout.addWidget(button);
		layout.addWidget(text);
		text.setVisible(false);

		button.clicked.connect(text, "setVisible(boolean)");
		contentsLayout.addWidget(container);
	}

	public void addSep() {
		QWidget separator = new QWidget();
		separator.setFixedHeight(2);
		separator.setStyleSheet("background:rgb(150,150,150);");
		contentsLayout.addWidget(separator);
	}
}
