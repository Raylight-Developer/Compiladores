package com.compiler.GUI;

import com.compiler.Types.Class;
import com.compiler.Types.*;

import io.qt.widgets.*;
import java.util.*;

public class Symbol_Table_Classes extends QTableWidget {
	private List<String>   columns = Arrays.asList("ID", "Parent");

	public Symbol_Table_Classes() {
		setSelectionMode(QAbstractItemView.SelectionMode.NoSelection);
		setColumnCount(columns.size());
		setRowCount(0);
		setHorizontalHeaderLabels(columns);
		resizeColumnsToContents();
	}

	public void add(Class value) {
		int row = rowCount();
		setRowCount(row + 1);

		setItem(row, 0, new QTableWidgetItem(value.ID));
		setItem(row, 1, new QTableWidgetItem(value.parent));
	}
}
