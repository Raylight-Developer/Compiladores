package com.compiler.GUI;

import io.qt.widgets.*;

public class Logger extends QTextBrowser {
	public Logger() {
		setTabStopDistance(40);
		setObjectName("Main");
	}

	public void debug(String value) {
		append("\t" + value);
	}
}