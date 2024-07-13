grammar MiniLang;

prog:   stat+ ;

stat:   expr NEWLINE                    # printExpr
    |   ID '=' expr NEWLINE             # assign
    |   'if' expr 'then' stat+ 'end'    # if
    |   'while' expr 'do' stat+ 'end'   # while
    |   'def' ID '(' ID ')' stat+ 'end' # func
    |   ID '(' expr ')' NEWLINE         # call
    |   NEWLINE                         # blank
    ;

expr:   expr ('*'|'/') expr                     # MulDiv
    |   expr ('+'|'-') expr                     # AddSub
    |   expr ('=='|'!='|'<'|'>'|'<='|'>=') expr # Compare
    |   INT                                     # int
    |   STRING                                  # string
    |   ID                                      # id
    |   '(' expr ')'                            # parens
    ;

STRING  : '"' (~["\\] | '\\' .)* '"';

DEF     : 'def';

IF      : 'if';
THEN    : 'then';
WHILE   : 'while';
DO      : 'do';
END     : 'end';

EQ  : '==';
NEQ : '!=';
LT  : '<';
GT  : '>';
LE  : '<=';
GE  : '>=';

MUL : '*' ; // define token for multiplication
DIV : '/' ; // define token for division
ADD : '+' ; // define token for addition
SUB : '-' ; // define token for subtraction
ID  : [a-zA-Z]+ ; // match identifiers
INT : [0-9]+ ; // match integers
NEWLINE:'\r'? '\n' ; // return newlines to parser (is end-statement signal)
WS  : [ \t]+ -> skip ; // toss out whitespace

COMMENT
    :   '//' ~[\r\n]* -> skip
    ;