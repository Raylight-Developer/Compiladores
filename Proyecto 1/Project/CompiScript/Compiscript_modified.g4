grammar Compiscript;

program         : declaration* EOF ;

declaration     : classDecl
                | funDecl
                | varDecl
                | statement ;

classDecl       : 'class' IDENTIFIER ('extends' IDENTIFIER)? '{' classBody '}' ;

classBody       : classMember* ;
classMember     : 'this.' variable
                | function ;

funDecl         : 'fun' function ;
varDecl         : 'var' variable ;

statement       : exprStmt
                | forStmt
                | ifStmt
                | printStmt
                | returnStmt
                | whileStmt
                | block ;

exprStmt        : expression ';' ;
forStmt         : 'for' '(' (varDecl | exprStmt | ';') expression? ';' expression? ')' statement ;
ifStmt          : 'if' '(' expression ')' statement ('else' statement)? ;
printStmt       : 'print' expression ';' ;
returnStmt      : 'return' expression? ';' ;
whileStmt       : 'while' '(' expression ')' statement ;
block           : '{' declaration* '}' ;
funAnon         : 'fun' '(' parameters? ')' block;

expression      : assignment
                | funAnon;

assignment      : (call '.')? IDENTIFIER '=' assignment
                | logic_or;

logic_or        : logic_and (('or' | '||') logic_and)* ;
logic_and       : equality (('and' | '&&') equality)* ;
equality        : comparison (( '!=' | '==' ) comparison)* ;
comparison      : term (( '>' | '>=' | '<' | '<=' ) term)* ;
term            : factor (( '-' | '+' ) factor)* ;
factor          : unary (( '/' | '*' | '%'  ) unary)* ;
array           : '[' (expression (',' expression)*)? ']';
instantiation   : 'new' IDENTIFIER '(' arguments? ')';

unary           : ( '!' | '-' ) unary
                | call ;

call            : primary ( '(' arguments? ')' | '.' IDENTIFIER | '[' expression ']')* 
                | funAnon;

primary         : 'true' | 'false' | 'nil' | 'this'
                | NUMBER | STRING | IDENTIFIER | '(' expression ')'
                | 'super' '.' IDENTIFIER 
                | array | instantiation;

function        : IDENTIFIER '(' parameters? ')' block ;
variable        : IDENTIFIER ('=' expression)? ';'
parameters      : IDENTIFIER ( ',' IDENTIFIER )* ;
arguments       : expression ( ',' expression )* ;

NUMBER          : DIGIT+ ( '.' DIGIT+ )? ;
STRING          : '"' (~["\\])* '"' ;
IDENTIFIER      : ALPHA ( ALPHA | DIGIT )* ;
fragment ALPHA  : [a-zA-Z_] ;
fragment DIGIT  : [0-9] ;
WS              : [ \t\r\n]+ -> skip ;
ONE_LINE_COMMENT: '//' (~ '\n')* '\n'? -> skip;
MULTI_LINE_COMMENT: '/*' .*? '*/' -> skip;  // This is the new rule for multi-line comments