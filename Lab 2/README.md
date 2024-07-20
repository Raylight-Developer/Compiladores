# Alejandro Martínez - 21430
# Samuel Argueta - 211024

<i><u>[GRAMATICA](./program/MiniLang.g4)</u></i>

```python
grammar MiniLang;

prog:   stat+ ;

stat:   expr NEWLINE                              # printExpr
    |   ID '=' expr NEWLINE                       # assign
    |   'if' expr 'then' stat+ 'end'              # if
    |   'while' expr 'do' stat+ 'end'             # while
    |   'def' ID '(' ID ')' stat+ 'end'           # func
    |   ID '(' expr ')' NEWLINE                   # call
    |   NEWLINE                                   # blank
    ;

expr:   expr ('*'|'/') expr                       # MulDiv
    |   expr ('+'|'-') expr                       # AddSub
    |   expr ('=='|'!='|'<'|'>'|'<='|'>=') expr   # Compare
    |   INT                                       # int
    |   STRING                                    # string
    |   ID                                        # id
    |   '(' expr ')'                              # parens
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

error
    : . {"Invalid character: " + $text }
    ;
```

## 1. Cree un programa que asigne un valor a una variable.
Test
```python
a = 5

```
## 2. Cree un programa que realice una operacion aritmetica simple.
Test
```python
3 + 4

```
## 3. Experimente con expresiones mas complejas.
Test
```python
a = 5
b = 10
a * (b + 3) / 2

```
## 4. Modifique el lenguaje para incluir la asignacion de variables con expresiones aritmeticas.
Modificacion

**ya existia, no es necesario modificar*
```python
stat: ID '=' expr NEWLINE
```
Test
```python
a = 5
b = 10
c = a * (b + 3) / 2

```
## 5. Agregue manejo de errores al compilador para detectar tokens invalidos en el programa fuente.
Modificacion
```python
error
    : . {"Invalid character: " + $text }
    ;
```
## 6. Cree un programa que utilice parentesis para cambiar la precedencia de operadores.
Test
```python
3 + 4 * 2
(3 + 4) * 2

```
## 7. Extienda el lenguaje para soportar comentarios de una sola linea.
Modificacion
```python
COMMENT
    :   '//' ~[\r\n]* -> skip
    ;
```
Test
```python
3 + 4 * 2
(3 + 4) * 2 // Comentario

```
## 8. Agregue operadores de comparacion (==, !=, ¡, >, ¡=, >=) al lenguaje.
Modification
```python
expr:   expr ('*'|'/') expr                     # MulDiv
    |   expr ('+'|'-') expr                     # AddSub
    |   expr ('=='|'!='|'<'|'>'|'<='|'>=') expr # Compare
    |   INT                                     # int
    |   ID                                      # id
    |   '(' expr ')'                            # parens
    ;

EQ  : '==';
NEQ : '!=';
LT  : '<';
GT  : '>';
LE  : '<=';
GE  : '>=';
```
## 9. Cree un programa que utilice operadores de comparacion.
Test
```python
3 == 4
5 != 2
a = 10
a >= 5

```
## 10. Extienda el lenguaje para soportar estructuras de control como ‘if‘ y ‘while‘.
Modification
```python
prog:   stat+ ;

stat:   expr NEWLINE                            # printExpr
    |   ID '=' expr NEWLINE                     # assign
    |   'if' expr 'then' stat+ 'end'            # if
    |   'while' expr 'do' stat+ 'end'           # while
    |   NEWLINE                                 # blank
    ;

expr:   expr ('*'|'/') expr                     # MulDiv
    |   expr ('+'|'-') expr                     # AddSub
    |   expr ('=='|'!='|'<'|'>'|'<='|'>=') expr # Compare
    |   INT                                     # int
    |   ID                                      # id
    |   '(' expr ')'                            # parens
    ;

IF      : 'if';
THEN    : 'then';
WHILE   : 'while';
DO      : 'do';
END     : 'end';
```
## 11. Cree un programa que utilice una estructura ‘if‘.
Test
```python
a = 10
if a > 5 then
  b = 3
end

```
## 12. Cree un programa que utilice una estructura ‘while‘.
Test
```python
a = 10
while a > 0 do
  a = a - 1
end

```
## 13. Agregue soporte para funciones definidas por el usuario.
Modification
```python
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
    |   ID                                      # id
    |   '(' expr ')'                            # parens
    ;

DEF     : 'def';
END     : 'end';
```
## 14. Cree un programa que defina y llame a una funcion.
Test
```python
def square(x)
  x * x
end

square(4)

```
## 15. Implemente un sistema de tipos basico que, ademas de incluir enteros, tambien incluya cadenas.
Modification
```python
expr:   expr ('*'|'/') expr                     # MulDiv
    |   expr ('+'|'-') expr                     # AddSub
    |   expr ('=='|'!='|'<'|'>'|'<='|'>=') expr # Compare
    |   INT                                     # int
    |   STRING                                  # string
    |   ID                                      # id
    |   '(' expr ')'                            # parens
    ;

STRING  : '"' (~["\\] | '\\' .)* '"';
```