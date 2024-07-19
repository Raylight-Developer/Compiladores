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
        4,1,15,57,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,4,0,12,8,0,
        11,0,12,0,13,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,23,8,1,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,
        1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,0,0,5,0,
        2,4,6,8,0,0,54,0,11,1,0,0,0,2,22,1,0,0,0,4,24,1,0,0,0,6,36,1,0,0,
        0,8,45,1,0,0,0,10,12,3,2,1,0,11,10,1,0,0,0,12,13,1,0,0,0,13,11,1,
        0,0,0,13,14,1,0,0,0,14,1,1,0,0,0,15,16,3,4,2,0,16,17,5,14,0,0,17,
        23,1,0,0,0,18,19,3,6,3,0,19,20,5,14,0,0,20,23,1,0,0,0,21,23,5,14,
        0,0,22,15,1,0,0,0,22,18,1,0,0,0,22,21,1,0,0,0,23,3,1,0,0,0,24,25,
        5,1,0,0,25,26,5,9,0,0,26,27,5,13,0,0,27,28,5,2,0,0,28,29,5,11,0,
        0,29,30,5,3,0,0,30,31,5,12,0,0,31,32,5,4,0,0,32,33,5,12,0,0,33,34,
        5,5,0,0,34,35,5,10,0,0,35,5,1,0,0,0,36,37,5,6,0,0,37,38,5,13,0,0,
        38,39,5,2,0,0,39,40,5,11,0,0,40,41,5,3,0,0,41,42,5,12,0,0,42,43,
        5,4,0,0,43,44,5,12,0,0,44,7,1,0,0,0,45,46,5,7,0,0,46,47,5,13,0,0,
        47,48,5,2,0,0,48,49,5,11,0,0,49,50,5,3,0,0,50,51,5,12,0,0,51,52,
        5,4,0,0,52,53,5,12,0,0,53,54,5,8,0,0,54,55,5,10,0,0,55,9,1,0,0,0,
        2,13,22
    ]

class ConfRoomSchedulerParser ( Parser ):

    grammarFileName = "ConfRoomScheduler.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'RESERVAR'", "'PARA'", "'DE'", "'A'", 
                     "'POR'", "'CANCELAR'", "'REPROGRAMAR'", "'SOLICITADO_POR'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "ROOMTYPE", "NAME", "DATE", "TIME", "ID", 
                      "NEWLINE", "WS" ]

    RULE_prog = 0
    RULE_stat = 1
    RULE_reserve = 2
    RULE_cancel = 3
    RULE_reschedule = 4

    ruleNames =  [ "prog", "stat", "reserve", "cancel", "reschedule" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    ROOMTYPE=9
    NAME=10
    DATE=11
    TIME=12
    ID=13
    NEWLINE=14
    WS=15

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
            self.state = 11 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 10
                self.stat()
                self.state = 13 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 16450) != 0)):
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
            self.state = 22
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                localctx = ConfRoomSchedulerParser.ReserveStatContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 15
                self.reserve()
                self.state = 16
                self.match(ConfRoomSchedulerParser.NEWLINE)
                pass
            elif token in [6]:
                localctx = ConfRoomSchedulerParser.CancelStatContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 18
                self.cancel()
                self.state = 19
                self.match(ConfRoomSchedulerParser.NEWLINE)
                pass
            elif token in [14]:
                localctx = ConfRoomSchedulerParser.BlankContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 21
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
            self.state = 24
            self.match(ConfRoomSchedulerParser.T__0)
            self.state = 25
            self.match(ConfRoomSchedulerParser.ROOMTYPE)
            self.state = 26
            self.match(ConfRoomSchedulerParser.ID)
            self.state = 27
            self.match(ConfRoomSchedulerParser.T__1)
            self.state = 28
            self.match(ConfRoomSchedulerParser.DATE)
            self.state = 29
            self.match(ConfRoomSchedulerParser.T__2)
            self.state = 30
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 31
            self.match(ConfRoomSchedulerParser.T__3)
            self.state = 32
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 33
            self.match(ConfRoomSchedulerParser.T__4)
            self.state = 34
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
            self.state = 36
            self.match(ConfRoomSchedulerParser.T__5)
            self.state = 37
            self.match(ConfRoomSchedulerParser.ID)
            self.state = 38
            self.match(ConfRoomSchedulerParser.T__1)
            self.state = 39
            self.match(ConfRoomSchedulerParser.DATE)
            self.state = 40
            self.match(ConfRoomSchedulerParser.T__2)
            self.state = 41
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 42
            self.match(ConfRoomSchedulerParser.T__3)
            self.state = 43
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
            self.state = 45
            self.match(ConfRoomSchedulerParser.T__6)
            self.state = 46
            self.match(ConfRoomSchedulerParser.ID)
            self.state = 47
            self.match(ConfRoomSchedulerParser.T__1)
            self.state = 48
            self.match(ConfRoomSchedulerParser.DATE)
            self.state = 49
            self.match(ConfRoomSchedulerParser.T__2)
            self.state = 50
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 51
            self.match(ConfRoomSchedulerParser.T__3)
            self.state = 52
            self.match(ConfRoomSchedulerParser.TIME)
            self.state = 53
            self.match(ConfRoomSchedulerParser.T__7)
            self.state = 54
            self.match(ConfRoomSchedulerParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





