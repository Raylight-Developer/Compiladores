package com.compiler.GUI;

import com.compiler.Types.*;

import io.qt.widgets.*;
import java.util.*;

public class Symbol_Table_Functions extends QTableWidget {
	private List<String>   columns = Arrays.asList("ID", "Return Type");

	public Symbol_Table_Functions() {
		setSelectionMode(QAbstractItemView.SelectionMode.NoSelection);
		setColumnCount(columns.size());
		setRowCount(0);
		setHorizontalHeaderLabels(columns);
		resizeColumnsToContents();
	}

	public void add(Function value) {
		int row = rowCount();
		setRowCount(row + 1);

		setItem(row, 0, new QTableWidgetItem(value.ID));
		setItem(row, 1, new QTableWidgetItem(value.return_type));
	}
}
