# Generated from MiniLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .MiniLangParser import MiniLangParser
else:
    from MiniLangParser import MiniLangParser

# This class defines a complete listener for a parse tree produced by MiniLangParser.
class MiniLangListener(ParseTreeListener):

    # Enter a parse tree produced by MiniLangParser#prog.
    def enterProg(self, ctx:MiniLangParser.ProgContext):
        pass

    # Exit a parse tree produced by MiniLangParser#prog.
    def exitProg(self, ctx:MiniLangParser.ProgContext):
        pass


    # Enter a parse tree produced by MiniLangParser#printExpr.
    def enterPrintExpr(self, ctx:MiniLangParser.PrintExprContext):
        pass

    # Exit a parse tree produced by MiniLangParser#printExpr.
    def exitPrintExpr(self, ctx:MiniLangParser.PrintExprContext):
        pass


    # Enter a parse tree produced by MiniLangParser#assign.
    def enterAssign(self, ctx:MiniLangParser.AssignContext):
        pass

    # Exit a parse tree produced by MiniLangParser#assign.
    def exitAssign(self, ctx:MiniLangParser.AssignContext):
        pass


    # Enter a parse tree produced by MiniLangParser#if.
    def enterIf(self, ctx:MiniLangParser.IfContext):
        pass

    # Exit a parse tree produced by MiniLangParser#if.
    def exitIf(self, ctx:MiniLangParser.IfContext):
        pass


    # Enter a parse tree produced by MiniLangParser#while.
    def enterWhile(self, ctx:MiniLangParser.WhileContext):
        pass

    # Exit a parse tree produced by MiniLangParser#while.
    def exitWhile(self, ctx:MiniLangParser.WhileContext):
        pass


    # Enter a parse tree produced by MiniLangParser#func.
    def enterFunc(self, ctx:MiniLangParser.FuncContext):
        pass

    # Exit a parse tree produced by MiniLangParser#func.
    def exitFunc(self, ctx:MiniLangParser.FuncContext):
        pass


    # Enter a parse tree produced by MiniLangParser#call.
    def enterCall(self, ctx:MiniLangParser.CallContext):
        pass

    # Exit a parse tree produced by MiniLangParser#call.
    def exitCall(self, ctx:MiniLangParser.CallContext):
        pass


    # Enter a parse tree produced by MiniLangParser#blank.
    def enterBlank(self, ctx:MiniLangParser.BlankContext):
        pass

    # Exit a parse tree produced by MiniLangParser#blank.
    def exitBlank(self, ctx:MiniLangParser.BlankContext):
        pass


    # Enter a parse tree produced by MiniLangParser#parens.
    def enterParens(self, ctx:MiniLangParser.ParensContext):
        pass

    # Exit a parse tree produced by MiniLangParser#parens.
    def exitParens(self, ctx:MiniLangParser.ParensContext):
        pass


    # Enter a parse tree produced by MiniLangParser#string.
    def enterString(self, ctx:MiniLangParser.StringContext):
        pass

    # Exit a parse tree produced by MiniLangParser#string.
    def exitString(self, ctx:MiniLangParser.StringContext):
        pass


    # Enter a parse tree produced by MiniLangParser#MulDiv.
    def enterMulDiv(self, ctx:MiniLangParser.MulDivContext):
        pass

    # Exit a parse tree produced by MiniLangParser#MulDiv.
    def exitMulDiv(self, ctx:MiniLangParser.MulDivContext):
        pass


    # Enter a parse tree produced by MiniLangParser#AddSub.
    def enterAddSub(self, ctx:MiniLangParser.AddSubContext):
        pass

    # Exit a parse tree produced by MiniLangParser#AddSub.
    def exitAddSub(self, ctx:MiniLangParser.AddSubContext):
        pass


    # Enter a parse tree produced by MiniLangParser#Compare.
    def enterCompare(self, ctx:MiniLangParser.CompareContext):
        pass

    # Exit a parse tree produced by MiniLangParser#Compare.
    def exitCompare(self, ctx:MiniLangParser.CompareContext):
        pass


    # Enter a parse tree produced by MiniLangParser#id.
    def enterId(self, ctx:MiniLangParser.IdContext):
        pass

    # Exit a parse tree produced by MiniLangParser#id.
    def exitId(self, ctx:MiniLangParser.IdContext):
        pass


    # Enter a parse tree produced by MiniLangParser#int.
    def enterInt(self, ctx:MiniLangParser.IntContext):
        pass

    # Exit a parse tree produced by MiniLangParser#int.
    def exitInt(self, ctx:MiniLangParser.IntContext):
        pass


    # Enter a parse tree produced by MiniLangParser#error.
    def enterError(self, ctx:MiniLangParser.ErrorContext):
        pass

    # Exit a parse tree produced by MiniLangParser#error.
    def exitError(self, ctx:MiniLangParser.ErrorContext):
        pass



del MiniLangParser