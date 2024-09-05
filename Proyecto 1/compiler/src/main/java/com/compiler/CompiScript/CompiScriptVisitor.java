package com.compiler.CompiScript;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link CompiScriptParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface CompiScriptVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#program}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProgram(CompiScriptParser.ProgramContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#declaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDeclaration(CompiScriptParser.DeclarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#classDecl}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitClassDecl(CompiScriptParser.ClassDeclContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#funDecl}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunDecl(CompiScriptParser.FunDeclContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#varDecl}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVarDecl(CompiScriptParser.VarDeclContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#statement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStatement(CompiScriptParser.StatementContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#exprStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExprStmt(CompiScriptParser.ExprStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#forStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitForStmt(CompiScriptParser.ForStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#ifStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIfStmt(CompiScriptParser.IfStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#printStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrintStmt(CompiScriptParser.PrintStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#returnStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitReturnStmt(CompiScriptParser.ReturnStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#whileStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWhileStmt(CompiScriptParser.WhileStmtContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#block}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlock(CompiScriptParser.BlockContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#funAnon}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunAnon(CompiScriptParser.FunAnonContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpression(CompiScriptParser.ExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#assignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssignment(CompiScriptParser.AssignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#logic_or}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLogic_or(CompiScriptParser.Logic_orContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#logic_and}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLogic_and(CompiScriptParser.Logic_andContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#equality}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEquality(CompiScriptParser.EqualityContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#comparison}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComparison(CompiScriptParser.ComparisonContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#term}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTerm(CompiScriptParser.TermContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#factor}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFactor(CompiScriptParser.FactorContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#array}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArray(CompiScriptParser.ArrayContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#instantiation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInstantiation(CompiScriptParser.InstantiationContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#unary}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnary(CompiScriptParser.UnaryContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#call}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCall(CompiScriptParser.CallContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#primary}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrimary(CompiScriptParser.PrimaryContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#function}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction(CompiScriptParser.FunctionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#parameters}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameters(CompiScriptParser.ParametersContext ctx);
	/**
	 * Visit a parse tree produced by {@link CompiScriptParser#arguments}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArguments(CompiScriptParser.ArgumentsContext ctx);
}