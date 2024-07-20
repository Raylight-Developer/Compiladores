import sys
from antlr4 import *
from ConfRoomSchedulerLexer import ConfRoomSchedulerLexer
from ConfRoomSchedulerParser import ConfRoomSchedulerParser
from ConfRoomSchedulerListener import ConfRoomSchedulerListener

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ConfRoomSchedulerLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ConfRoomSchedulerParser(stream)

    tree = parser.prog()
    listener = ConfRoomSchedulerListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    
if __name__ == '__main__':
    main(sys.argv)
