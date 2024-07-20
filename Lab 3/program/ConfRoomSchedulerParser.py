# Generated from ConfRoomScheduler.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,16,67,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,4,
        0,14,8,0,11,0,12,0,15,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,3,1,31,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,0,0,6,0,2,4,6,8,10,0,0,65,0,13,1,
        0,0,0,2,30,1,0,0,0,4,32,1,0,0,0,6,44,1,0,0,0,8,53,1,0,0,0,10,64,
        1,0,0,0,12,14,3,2,1,0,13,12,1,0,0,0,14,15,1,0,0,0,15,13,1,0,0,0,
        15,16,1,0,0,0,16,1,1,0,0,0,17,18,3,4,2,0,18,19,5,15,0,0,19,31,1,
        0,0,0,20,21,3,6,3,0,21,22,5,15,0,0,22,31,1,0,0,0,23,24,3,8,4,0,24,
        25,5,15,0,0,25,31,1,0,0,0,26,27,3,10,5,0,27,28,5,15,0,0,28,31,1,
        0,0,0,29,31,5,15,0,0,30,17,1,0,0,0,30,20,1,0,0,0,30,23,1,0,0,0,30,
        26,1,0,0,0,30,29,1,0,0,0,31,3,1,0,0,0,32,33,5,1,0,0,33,34,5,10,0,
        0,34,35,5,14,0,0,35,36,5,2,0,0,36,37,5,12,0,0,37,38,5,3,0,0,38,39,
        5,13,0,0,39,40,5,4,0,0,40,41,5,13,0,0,41,42,5,5,0,0,42,43,5,11,0,
        0,43,5,1,0,0,0,44,45,5,6,0,0,45,46,5,14,0,0,46,47,5,2,0,0,47,48,
        5,12,0,0,48,49,5,3,0,0,49,50,5,13,0,0,50,51,5,4,0,0,51,52,5,13,0,
        0,52,7,1,0,0,0,53,54,5,7,0,0,54,55,5,14,0,0,55,56,5,2,0,0,56,57,
        5,12,0,0,57,58,5,3,0,0,58,59,5,13,0,0,59,60,5,4,0,0,60,61,5,13,0,
        0,61,62,5,8,0,0,62,63,5,11,0,0,63,9,1,0,0,0,64,65,5,9,0,0,65,11,
        1,0,0,0,2,15,30
    ]

class ConfRoomSchedulerParser ( Parser ):

    grammarFileName = "ConfRoomScheduler.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'RESERVAR'", "'PARA'", "'DE'", "'A'", 
                     "'POR'", "'CANCELAR'", "'REPROGRAMAR'", "'SOLICITADO_POR'", 
                     "'LISTAR'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "ROOMTYPE", "NAME", "DATE", 
                      "TIME", "ID", "NEWLINE", "WS" ]

    RULE_prog = 0
    RULE_stat = 1
    RULE_reserve = 2
    RULE_cancel = 3
    RULE_reschedule = 4
    RULE_list = 5

    ruleNames =  [ "prog", "stat", "reserve", "cancel", "reschedule", "list" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    ROOMTYPE=10
    NAME=11
    DATE=12
    TIME=13
    ID=14
    NEWLINE=15
    WS=16

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ConfRoomSchedulerParser.StatContext)
            else:
                return self.getTypedRuleContext(ConfRoomSchedulerParser.StatContext,i)


        def getRuleIndex(self):
            return ConfRoomSchedulerParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)




    def prog(self):

        localctx = ConfRoomSchedulerParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 12
                self.stat()
                self.state = 15 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 33474) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ConfRoomSchedulerParser.RULE_stat

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class BlankContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ConfRoomSchedulerParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NEWLINE(self):
            return self.getToken(ConfRoomSchedulerParser.NEWLINE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlank" ):
                listener.enterBlank(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlank" ):
                listener.exitBlank(self)


    class RescheduleStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ConfRoomSchedulerParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def reschedule(self):
            return self.getTypedRuleContext(ConfRoomSchedulerParser.RescheduleContext,0)

        def NEWLINE(self):
            return self.getToken(ConfRoomSchedulerParser.NEWLINE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRescheduleStat" ):
                listener.enterRescheduleStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRescheduleStat" ):
                listener.exitRescheduleStat(self)


    class ListStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ConfRoomSchedulerParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def list_(self):
            return self.getTypedRuleContext(ConfRoomSchedulerParser.ListContext,0)

        def NEWLINE(self):
            return self.getToken(ConfRoomSchedulerParser.NEWLINE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListStat" ):
                listener.enterListStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListStat" ):
                listener.exitListStat(self)


    class ReserveStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ConfRoomSchedulerParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def reserve(self):
            return self.getTypedRuleContext(ConfRoomSchedulerParser.ReserveContext,0)

        def NEWLINE(self):
            return self.getToken(ConfRoomSchedulerParser.NEWLINE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReserveStat" ):
                listener.enterReserveStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReserveStat" ):
                listener.exitReserveStat(self)


    class CancelStatContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ConfRoomSchedulerParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def cancel(self):
            return self.getTypedRuleContext(ConfRoomSchedulerParser.CancelContext,0)

        def NEWLINE(self):
            return self.getToken(ConfRoomSchedulerParser.NEWLINE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCancelStat" ):
                listener.enterCancelStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCancelStat" ):
                listener.exitCancelStat(self)



    def stat(self):

        localctx = ConfRoomSchedulerParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stat)
        try:
            self.state = 30
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                localctx = ConfRoomSchedulerParser.ReserveStatContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 17
                self.reserve()
                self.state = 18
                self.match(ConfRoomSchedulerParser.NEWLINE)
                pass
            elif token in [6]:
                localctx = ConfRoomSchedulerParser.CancelStatContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 20
                self.cancel()
                self.state = 21
                self.match(ConfRoomSchedulerParser.NEWLINE)
                pass
            elif token in [7]:
                localctx = ConfRoomSchedulerParser.RescheduleStatContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 23
                self.reschedule()
                self.state = 24
                self.match(ConfRoomSchedulerParser.NEWLINE)
                pass
            elif token in [9]:
                localctx = ConfRoomSchedulerParser.ListStatContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 26
                self.list_()
                self.state = 27
                self.match(ConfRoomSchedulerParser.NEWLINE)
                pass
            elif token in [15]:
                localctx = ConfRoomSchedulerParser.BlankContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 29
                self.match(ConfRoomSchedulerParser.NEWLINE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReserveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ROOMTYPE(self):
            return self.getToken(ConfRoomSchedulerParser.ROOMTYPE, 0)

        def ID(self):
            return self.getToken(ConfRoomSchedulerParser.ID, 0)

        def DATE(self):
            return self.getToken(ConfRoomSchedulerParser.DATE, 0)

        def TIME(self, i:int=None):
            if i is None:
                return self.getTokens(ConfRoomSchedulerParser.TIME)
            else:
                return self.getToken(ConfRoomSchedulerParser.TIME, i)

        def NAME(self):
            return self.getToken(ConfRoomSchedulerParser.NAME, 0)

        def getRuleIndex(self):
            return ConfRoomSchedulerParser.RULE_reserve

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReserve" ):
                listener.enterReserve(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReserve" ):
                listener.exitReserve(self)




    def reserve(self):

        localctx = ConfRoomSchedulerParser.ReserveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_reserve)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.match(ConfRoomSchedulerParser.T__0)
            self.state = 33
            self.match(ConfRoomSchedulerParser.ROOMTYPE)
            self.state = 34
            self.match(ConfRoomSchedulerParser.ID)
            self.state = 35
            self.match(ConfRoomSchedulerParser.T__1)
            self.state = 36
            self.match(ConfRoomSchedulerParser.DATE)
            self.state = 37
            self.match(ConfRoomSchedulerParser.T__2)
            self.state = 38
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 39
            self.match(ConfRoomSchedulerParser.T__3)
            self.state = 40
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 41
            self.match(ConfRoomSchedulerParser.T__4)
            self.state = 42
            self.match(ConfRoomSchedulerParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CancelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ConfRoomSchedulerParser.ID, 0)

        def DATE(self):
            return self.getToken(ConfRoomSchedulerParser.DATE, 0)

        def TIME(self, i:int=None):
            if i is None:
                return self.getTokens(ConfRoomSchedulerParser.TIME)
            else:
                return self.getToken(ConfRoomSchedulerParser.TIME, i)

        def getRuleIndex(self):
            return ConfRoomSchedulerParser.RULE_cancel

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCancel" ):
                listener.enterCancel(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCancel" ):
                listener.exitCancel(self)




    def cancel(self):

        localctx = ConfRoomSchedulerParser.CancelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_cancel)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(ConfRoomSchedulerParser.T__5)
            self.state = 45
            self.match(ConfRoomSchedulerParser.ID)
            self.state = 46
            self.match(ConfRoomSchedulerParser.T__1)
            self.state = 47
            self.match(ConfRoomSchedulerParser.DATE)
            self.state = 48
            self.match(ConfRoomSchedulerParser.T__2)
            self.state = 49
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 50
            self.match(ConfRoomSchedulerParser.T__3)
            self.state = 51
            self.match(ConfRoomSchedulerParser.TIME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RescheduleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ConfRoomSchedulerParser.ID, 0)

        def DATE(self):
            return self.getToken(ConfRoomSchedulerParser.DATE, 0)

        def TIME(self, i:int=None):
            if i is None:
                return self.getTokens(ConfRoomSchedulerParser.TIME)
            else:
                return self.getToken(ConfRoomSchedulerParser.TIME, i)

        def NAME(self):
            return self.getToken(ConfRoomSchedulerParser.NAME, 0)

        def getRuleIndex(self):
            return ConfRoomSchedulerParser.RULE_reschedule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReschedule" ):
                listener.enterReschedule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReschedule" ):
                listener.exitReschedule(self)




    def reschedule(self):

        localctx = ConfRoomSchedulerParser.RescheduleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_reschedule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(ConfRoomSchedulerParser.T__6)
            self.state = 54
            self.match(ConfRoomSchedulerParser.ID)
            self.state = 55
            self.match(ConfRoomSchedulerParser.T__1)
            self.state = 56
            self.match(ConfRoomSchedulerParser.DATE)
            self.state = 57
            self.match(ConfRoomSchedulerParser.T__2)
            self.state = 58
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 59
            self.match(ConfRoomSchedulerParser.T__3)
            self.state = 60
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 61
            self.match(ConfRoomSchedulerParser.T__7)
            self.state = 62
            self.match(ConfRoomSchedulerParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ConfRoomSchedulerParser.RULE_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterList" ):
                listener.enterList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitList" ):
                listener.exitList(self)




    def list_(self):

        localctx = ConfRoomSchedulerParser.ListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_list)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(ConfRoomSchedulerParser.T__8)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





