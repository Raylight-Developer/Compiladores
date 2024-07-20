grammar ConfRoomScheduler;

prog: stat+ ;

stat: reserve NEWLINE                # reserveStat
    | cancel NEWLINE                 # cancelStat
    | reschedule NEWLINE             # rescheduleStat
    | list NEWLINE                   # listStat
    | NEWLINE                        # blank
    ;

reserve: 'RESERVAR' ROOMTYPE ID 'PARA' DATE 'DE' TIME 'A' TIME 'POR' NAME ; 
cancel: 'CANCELAR' ID 'PARA' DATE 'DE' TIME 'A' TIME ; 
reschedule: 'REPROGRAMAR' ID 'PARA' DATE 'DE' TIME 'A' TIME 'SOLICITADO_POR' NAME ;
list: 'LISTAR' ; 

ROOMTYPE: 'sala_de_juntas' | 'sala_de_capacitacion' ; 
NAME: [a-zA-Z]+ ; 
DATE: DIGIT DIGIT '/' DIGIT DIGIT '/' DIGIT DIGIT DIGIT DIGIT ; 
TIME: DIGIT DIGIT ':' DIGIT DIGIT ; 
ID  : [a-zA-Z0-9]+ ; 
NEWLINE: '\r'? '\n' ; 
WS  : [ \t]+ -> skip ; 

fragment DIGIT : [0-9] ;
