package com.compiler;

import org.antlr.v4.runtime.tree.*;

import javax.lang.model.type.*;
import java.util.regex.*;
import java.util.*;

class Parameter {
	String ID;
	String type;
}
class Function {
	String ID;
	List<Parameter> parameters;
	String return_type;
}
class Variable {
	String ID;
	String type;
	String code;
}
class Class {
	String ID;
	String parent;
	Function constructor;
	List<Function> function_members;
	List<Variable> variable_members;
}

public class Syntax_Analyzer extends CompiScriptBaseVisitor<Object> {
	private Map<String, Map<String,Map<String,Object>>>
			scopes_current = new HashMap<>(){{put("0",new HashMap<>());}};
	private Map<String, Map<String,Map<String,Object>>>
			scopes_classes = new HashMap<>(){{put("0",new HashMap<>());}};
	private Map<String, Map<String,Map<String,Object>>>
			scopes_functions = new HashMap<>(){{put("0",new HashMap<>());}};
	private Map<String, Map<String,Map<String,Object>>>
			scopes_variables = new HashMap<>(){{put("0",new HashMap<>());}};

	@Override public Object visitProgram(CompiScriptParser.ProgramContext ctx) { return visitChildren(ctx); }
	@Override public Object visitDeclaration(CompiScriptParser.DeclarationContext ctx) { return visitChildren(ctx); }
	@Override public Object visitClassDecl(CompiScriptParser.ClassDeclContext ctx) { return visitChildren(ctx); }
	@Override public Object visitFunDecl(CompiScriptParser.FunDeclContext ctx) { return visitChildren(ctx); }
	@Override public Object visitVarDecl(CompiScriptParser.VarDeclContext ctx) { return visitChildren(ctx); }
	@Override public Object visitStatement(CompiScriptParser.StatementContext ctx) { return visitChildren(ctx); }
	@Override public Object visitExprStmt(CompiScriptParser.ExprStmtContext ctx) { return visitChildren(ctx); }
	@Override public Object visitForStmt(CompiScriptParser.ForStmtContext ctx) { return visitChildren(ctx); }
	@Override public Object visitIfStmt(CompiScriptParser.IfStmtContext ctx) { return visitChildren(ctx); }
	@Override public Object visitPrintStmt(CompiScriptParser.PrintStmtContext ctx) { return visitChildren(ctx); }
	@Override public Object visitReturnStmt(CompiScriptParser.ReturnStmtContext ctx) { return visitChildren(ctx); }
	@Override public Object visitWhileStmt(CompiScriptParser.WhileStmtContext ctx) { return visitChildren(ctx); }
	@Override public Object visitBlock(CompiScriptParser.BlockContext ctx) { return visitChildren(ctx); }
	@Override public Object visitFunAnon(CompiScriptParser.FunAnonContext ctx) { return visitChildren(ctx); }
	@Override public Object visitExpression(CompiScriptParser.ExpressionContext ctx) { return visitChildren(ctx); }
	@Override public Object visitAssignment(CompiScriptParser.AssignmentContext ctx) { return visitChildren(ctx); }
	@Override public Object visitLogic_or(CompiScriptParser.Logic_orContext ctx) { return visitChildren(ctx); }
	@Override public Object visitLogic_and(CompiScriptParser.Logic_andContext ctx) { return visitChildren(ctx); }
	@Override public Object visitEquality(CompiScriptParser.EqualityContext ctx) { return visitChildren(ctx); }
	@Override public Object visitComparison(CompiScriptParser.ComparisonContext ctx) { return visitChildren(ctx); }
	@Override public Object visitTerm(CompiScriptParser.TermContext ctx) { return visitChildren(ctx); }
	@Override public Object visitFactor(CompiScriptParser.FactorContext ctx) { return visitChildren(ctx); }
	@Override public Object visitArray(CompiScriptParser.ArrayContext ctx) { return visitChildren(ctx); }
	@Override public Object visitInstantiation(CompiScriptParser.InstantiationContext ctx) { return visitChildren(ctx); }
	@Override public Object visitUnary(CompiScriptParser.UnaryContext ctx) { return visitChildren(ctx); }
	@Override public Object visitCall(CompiScriptParser.CallContext ctx) { return visitChildren(ctx); }
	@Override public Object visitPrimary(CompiScriptParser.PrimaryContext ctx) { return visitChildren(ctx); }
	@Override public Object visitFunction(CompiScriptParser.FunctionContext ctx) { return visitChildren(ctx); }
	@Override public Object visitParameters(CompiScriptParser.ParametersContext ctx) { return visitChildren(ctx); }
	@Override public Object visitArguments(CompiScriptParser.ArgumentsContext ctx) { return visitChildren(ctx); }
}