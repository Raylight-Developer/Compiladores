package com.compiler.GUI;

import io.qt.widgets.*;
import io.qt.core.*;
import io.qt.gui.*;

import java.util.*;

class HighlightingRule {
	public QRegularExpression pattern;
	public QTextCharFormat format;

	public HighlightingRule(QRegularExpression pattern, QTextCharFormat format) {
		this.pattern = pattern;
		this.format = format;
	}
}

public class Syntax_Highlighter extends QSyntaxHighlighter {
	private List<HighlightingRule> highlightingRules;
	private QTextCharFormat userKeywords;
	private QTextCharFormat control;
	private QTextCharFormat builtinFunctions;
	private QTextCharFormat builtinClasses;
	private QTextCharFormat brackets;
	private QTextCharFormat integers;
	private QTextCharFormat floats;
	private QTextCharFormat strings;
	private QTextCharFormat comments;

	public Syntax_Highlighter(QTextDocument parent) {
		super(parent);
		highlightingRules = new ArrayList<>();

		// User Keywords
		userKeywords = new QTextCharFormat();
		userKeywords.setForeground(new QColor(86, 156, 214));
		String[] keywordPatterns = {"float", "int", "uint", "bool", "class", "struct", "const", "true", "false"};
		for (String pattern : keywordPatterns) {
			HighlightingRule rule = new HighlightingRule(
				new QRegularExpression("\\b" + pattern + "\\b"), userKeywords
			);
			highlightingRules.add(rule);
		}

		// Control Keywords
		control = new QTextCharFormat();
		control.setForeground(new QColor(216, 160, 223));
		String[] controlPatterns = {"if", "else", "else if", "while", "for", "return", "switch", "case", "break", "continue"};
		for (String pattern : controlPatterns) {
			HighlightingRule rule = new HighlightingRule(
				new QRegularExpression("\\b" + pattern + "\\b"), control
			);
			highlightingRules.add(rule);
		}

		// Builtin Functions
		builtinFunctions = new QTextCharFormat();
		builtinFunctions.setForeground(new QColor(225, 225, 120));
		String[] functionPatterns = {"fun", "print", "init", "var"};
		for (String pattern : functionPatterns) {
			HighlightingRule rule = new HighlightingRule(
				new QRegularExpression("\\b" + pattern + "\\b"), builtinFunctions
			);
			highlightingRules.add(rule);
		}

		// Builtin Classes
		builtinClasses = new QTextCharFormat();
		builtinClasses.setForeground(new QColor(78, 201, 176));
		HighlightingRule classRule = new HighlightingRule(
			new QRegularExpression("\\bsuper\\b"), builtinClasses
		);
		highlightingRules.add(classRule);

		// Brackets
		brackets = new QTextCharFormat();
		brackets.setForeground(new QColor(255, 215, 0));
		String[] bracketPatterns = {"\\(", "\\)", "\\[", "\\]", "\\{", "\\}"};
		for (String pattern : bracketPatterns) {
			HighlightingRule rule = new HighlightingRule(
				new QRegularExpression(pattern), brackets
			);
			highlightingRules.add(rule);
		}

		// Integers
		integers = new QTextCharFormat();
		integers.setForeground(new QColor(181, 206, 168));
		HighlightingRule intRule = new HighlightingRule(
			new QRegularExpression("\\b[-+]?[0-9]+[uU]?\\b"), integers
		);
		highlightingRules.add(intRule);

		// Floats
		floats = new QTextCharFormat();
		floats.setForeground(new QColor(185, 225, 172));
		HighlightingRule floatRule = new HighlightingRule(
			new QRegularExpression("\\b[-+]?([0-9]*\\.[0-9]+|[0-9]+\\.)([eE][-+]?[0-9]+)?[fF]?\\b"), floats
		);
		highlightingRules.add(floatRule);

		// Strings
		strings = new QTextCharFormat();
		strings.setForeground(new QColor(214, 157, 133));
		String[] stringPatterns = {"\"([^\"\\\\]|\\\\.)*\"", "'([^'\\\\]|\\\\.)*'"};
		for (String pattern : stringPatterns) {
			HighlightingRule rule = new HighlightingRule(
				new QRegularExpression(pattern), strings
			);
			highlightingRules.add(rule);
		}

		// Comments
		comments = new QTextCharFormat();
		comments.setForeground(new QColor(87, 166, 74));
		String[] commentPatterns = {"//[^\\n]*", "/\\*.*?\\*/"};
		for (String pattern : commentPatterns) {
			HighlightingRule rule = new HighlightingRule(
				new QRegularExpression(pattern), comments
			);
			highlightingRules.add(rule);
		}
	}

	@Override
	protected void highlightBlock(String text) {
		for (HighlightingRule rule : highlightingRules) {
			QRegularExpressionMatchIterator matchIterator = rule.pattern.globalMatch(text);
			while (matchIterator.hasNext()) {
				QRegularExpressionMatch match = matchIterator.next();
				setFormat(((int)match.capturedStart()), ((int)match.capturedLength()), rule.format);
			}
		}
	}
}