# Generated from Compiscript.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .CompiscriptParser import CompiscriptParser
else:
    from CompiscriptParser import CompiscriptParser

# This class defines a complete listener for a parse tree produced by CompiscriptParser.
class CompiscriptListener(ParseTreeListener):

    # Enter a parse tree produced by CompiscriptParser#program.
    def enterProgram(self, ctx:CompiscriptParser.ProgramContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#program.
    def exitProgram(self, ctx:CompiscriptParser.ProgramContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#declaration.
    def enterDeclaration(self, ctx:CompiscriptParser.DeclarationContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#declaration.
    def exitDeclaration(self, ctx:CompiscriptParser.DeclarationContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#classDecl.
    def enterClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#classDecl.
    def exitClassDecl(self, ctx:CompiscriptParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#funDecl.
    def enterFunDecl(self, ctx:CompiscriptParser.FunDeclContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#funDecl.
    def exitFunDecl(self, ctx:CompiscriptParser.FunDeclContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#varDecl.
    def enterVarDecl(self, ctx:CompiscriptParser.VarDeclContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#varDecl.
    def exitVarDecl(self, ctx:CompiscriptParser.VarDeclContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#statement.
    def enterStatement(self, ctx:CompiscriptParser.StatementContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#statement.
    def exitStatement(self, ctx:CompiscriptParser.StatementContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#exprStmt.
    def enterExprStmt(self, ctx:CompiscriptParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#exprStmt.
    def exitExprStmt(self, ctx:CompiscriptParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#forStmt.
    def enterForStmt(self, ctx:CompiscriptParser.ForStmtContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#forStmt.
    def exitForStmt(self, ctx:CompiscriptParser.ForStmtContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#ifStmt.
    def enterIfStmt(self, ctx:CompiscriptParser.IfStmtContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#ifStmt.
    def exitIfStmt(self, ctx:CompiscriptParser.IfStmtContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#printStmt.
    def enterPrintStmt(self, ctx:CompiscriptParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#printStmt.
    def exitPrintStmt(self, ctx:CompiscriptParser.PrintStmtContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#returnStmt.
    def enterReturnStmt(self, ctx:CompiscriptParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#returnStmt.
    def exitReturnStmt(self, ctx:CompiscriptParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#whileStmt.
    def enterWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#whileStmt.
    def exitWhileStmt(self, ctx:CompiscriptParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#block.
    def enterBlock(self, ctx:CompiscriptParser.BlockContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#block.
    def exitBlock(self, ctx:CompiscriptParser.BlockContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#funAnon.
    def enterFunAnon(self, ctx:CompiscriptParser.FunAnonContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#funAnon.
    def exitFunAnon(self, ctx:CompiscriptParser.FunAnonContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#expression.
    def enterExpression(self, ctx:CompiscriptParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#expression.
    def exitExpression(self, ctx:CompiscriptParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#assignment.
    def enterAssignment(self, ctx:CompiscriptParser.AssignmentContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#assignment.
    def exitAssignment(self, ctx:CompiscriptParser.AssignmentContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#logic_or.
    def enterLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#logic_or.
    def exitLogic_or(self, ctx:CompiscriptParser.Logic_orContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#logic_and.
    def enterLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#logic_and.
    def exitLogic_and(self, ctx:CompiscriptParser.Logic_andContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#equality.
    def enterEquality(self, ctx:CompiscriptParser.EqualityContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#equality.
    def exitEquality(self, ctx:CompiscriptParser.EqualityContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#comparison.
    def enterComparison(self, ctx:CompiscriptParser.ComparisonContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#comparison.
    def exitComparison(self, ctx:CompiscriptParser.ComparisonContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#term.
    def enterTerm(self, ctx:CompiscriptParser.TermContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#term.
    def exitTerm(self, ctx:CompiscriptParser.TermContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#factor.
    def enterFactor(self, ctx:CompiscriptParser.FactorContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#factor.
    def exitFactor(self, ctx:CompiscriptParser.FactorContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#array.
    def enterArray(self, ctx:CompiscriptParser.ArrayContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#array.
    def exitArray(self, ctx:CompiscriptParser.ArrayContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#instantiation.
    def enterInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#instantiation.
    def exitInstantiation(self, ctx:CompiscriptParser.InstantiationContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#unary.
    def enterUnary(self, ctx:CompiscriptParser.UnaryContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#unary.
    def exitUnary(self, ctx:CompiscriptParser.UnaryContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#call.
    def enterCall(self, ctx:CompiscriptParser.CallContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#call.
    def exitCall(self, ctx:CompiscriptParser.CallContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#primary.
    def enterPrimary(self, ctx:CompiscriptParser.PrimaryContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#primary.
    def exitPrimary(self, ctx:CompiscriptParser.PrimaryContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#function.
    def enterFunction(self, ctx:CompiscriptParser.FunctionContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#function.
    def exitFunction(self, ctx:CompiscriptParser.FunctionContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#parameters.
    def enterParameters(self, ctx:CompiscriptParser.ParametersContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#parameters.
    def exitParameters(self, ctx:CompiscriptParser.ParametersContext):
        pass


    # Enter a parse tree produced by CompiscriptParser#arguments.
    def enterArguments(self, ctx:CompiscriptParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by CompiscriptParser#arguments.
    def exitArguments(self, ctx:CompiscriptParser.ArgumentsContext):
        pass



del CompiscriptParser