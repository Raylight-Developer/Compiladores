package com.compiler.CompiScript;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link CompiScriptParser}.
 */
public interface CompiScriptListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(CompiScriptParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(CompiScriptParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#declaration}.
	 * @param ctx the parse tree
	 */
	void enterDeclaration(CompiScriptParser.DeclarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#declaration}.
	 * @param ctx the parse tree
	 */
	void exitDeclaration(CompiScriptParser.DeclarationContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#classDecl}.
	 * @param ctx the parse tree
	 */
	void enterClassDecl(CompiScriptParser.ClassDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#classDecl}.
	 * @param ctx the parse tree
	 */
	void exitClassDecl(CompiScriptParser.ClassDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#funDecl}.
	 * @param ctx the parse tree
	 */
	void enterFunDecl(CompiScriptParser.FunDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#funDecl}.
	 * @param ctx the parse tree
	 */
	void exitFunDecl(CompiScriptParser.FunDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#varDecl}.
	 * @param ctx the parse tree
	 */
	void enterVarDecl(CompiScriptParser.VarDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#varDecl}.
	 * @param ctx the parse tree
	 */
	void exitVarDecl(CompiScriptParser.VarDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(CompiScriptParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(CompiScriptParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#exprStmt}.
	 * @param ctx the parse tree
	 */
	void enterExprStmt(CompiScriptParser.ExprStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#exprStmt}.
	 * @param ctx the parse tree
	 */
	void exitExprStmt(CompiScriptParser.ExprStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#forStmt}.
	 * @param ctx the parse tree
	 */
	void enterForStmt(CompiScriptParser.ForStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#forStmt}.
	 * @param ctx the parse tree
	 */
	void exitForStmt(CompiScriptParser.ForStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void enterIfStmt(CompiScriptParser.IfStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void exitIfStmt(CompiScriptParser.IfStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#printStmt}.
	 * @param ctx the parse tree
	 */
	void enterPrintStmt(CompiScriptParser.PrintStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#printStmt}.
	 * @param ctx the parse tree
	 */
	void exitPrintStmt(CompiScriptParser.PrintStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void enterReturnStmt(CompiScriptParser.ReturnStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void exitReturnStmt(CompiScriptParser.ReturnStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void enterWhileStmt(CompiScriptParser.WhileStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void exitWhileStmt(CompiScriptParser.WhileStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(CompiScriptParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(CompiScriptParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#funAnon}.
	 * @param ctx the parse tree
	 */
	void enterFunAnon(CompiScriptParser.FunAnonContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#funAnon}.
	 * @param ctx the parse tree
	 */
	void exitFunAnon(CompiScriptParser.FunAnonContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(CompiScriptParser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(CompiScriptParser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#assignment}.
	 * @param ctx the parse tree
	 */
	void enterAssignment(CompiScriptParser.AssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#assignment}.
	 * @param ctx the parse tree
	 */
	void exitAssignment(CompiScriptParser.AssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#logic_or}.
	 * @param ctx the parse tree
	 */
	void enterLogic_or(CompiScriptParser.Logic_orContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#logic_or}.
	 * @param ctx the parse tree
	 */
	void exitLogic_or(CompiScriptParser.Logic_orContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#logic_and}.
	 * @param ctx the parse tree
	 */
	void enterLogic_and(CompiScriptParser.Logic_andContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#logic_and}.
	 * @param ctx the parse tree
	 */
	void exitLogic_and(CompiScriptParser.Logic_andContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#equality}.
	 * @param ctx the parse tree
	 */
	void enterEquality(CompiScriptParser.EqualityContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#equality}.
	 * @param ctx the parse tree
	 */
	void exitEquality(CompiScriptParser.EqualityContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#comparison}.
	 * @param ctx the parse tree
	 */
	void enterComparison(CompiScriptParser.ComparisonContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#comparison}.
	 * @param ctx the parse tree
	 */
	void exitComparison(CompiScriptParser.ComparisonContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#term}.
	 * @param ctx the parse tree
	 */
	void enterTerm(CompiScriptParser.TermContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#term}.
	 * @param ctx the parse tree
	 */
	void exitTerm(CompiScriptParser.TermContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#factor}.
	 * @param ctx the parse tree
	 */
	void enterFactor(CompiScriptParser.FactorContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#factor}.
	 * @param ctx the parse tree
	 */
	void exitFactor(CompiScriptParser.FactorContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#array}.
	 * @param ctx the parse tree
	 */
	void enterArray(CompiScriptParser.ArrayContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#array}.
	 * @param ctx the parse tree
	 */
	void exitArray(CompiScriptParser.ArrayContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#instantiation}.
	 * @param ctx the parse tree
	 */
	void enterInstantiation(CompiScriptParser.InstantiationContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#instantiation}.
	 * @param ctx the parse tree
	 */
	void exitInstantiation(CompiScriptParser.InstantiationContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#unary}.
	 * @param ctx the parse tree
	 */
	void enterUnary(CompiScriptParser.UnaryContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#unary}.
	 * @param ctx the parse tree
	 */
	void exitUnary(CompiScriptParser.UnaryContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#call}.
	 * @param ctx the parse tree
	 */
	void enterCall(CompiScriptParser.CallContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#call}.
	 * @param ctx the parse tree
	 */
	void exitCall(CompiScriptParser.CallContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterPrimary(CompiScriptParser.PrimaryContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitPrimary(CompiScriptParser.PrimaryContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#function}.
	 * @param ctx the parse tree
	 */
	void enterFunction(CompiScriptParser.FunctionContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#function}.
	 * @param ctx the parse tree
	 */
	void exitFunction(CompiScriptParser.FunctionContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#parameters}.
	 * @param ctx the parse tree
	 */
	void enterParameters(CompiScriptParser.ParametersContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#parameters}.
	 * @param ctx the parse tree
	 */
	void exitParameters(CompiScriptParser.ParametersContext ctx);
	/**
	 * Enter a parse tree produced by {@link CompiScriptParser#arguments}.
	 * @param ctx the parse tree
	 */
	void enterArguments(CompiScriptParser.ArgumentsContext ctx);
	/**
	 * Exit a parse tree produced by {@link CompiScriptParser#arguments}.
	 * @param ctx the parse tree
	 */
	void exitArguments(CompiScriptParser.ArgumentsContext ctx);
}