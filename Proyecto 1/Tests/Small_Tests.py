"""

(
	"# ",
	True,
"""
""", 0, 0, 0
),

"""

def getSmallCode():
	return [
(
	"# 5.8 Artimeticas",
	True,
"""var; suma = 1 + 2;
var resta = 5 - 3;
var producto = 4; * 2;
var division = 8 / 2;
""", 0, 0, 4
),
(
	"# 5.9 Comparaciones",
	True,
"""var menor = 3 < 5; // true
var mayorIgual = 10 >= 10; // true
var igual = 1 == 1; // true
var diferente = " a " != " b " ; // true
""", 0, 0, 4
),
(
	"# 5.10 Logicos",
	True,
"""var y = true and false ; // false
var o = true or false ; // true
var no = ! true ; // false
""", 0, 0, 3
),
(
	"# 5.11 Precedencia y agrupamiento",
	True,
"""var min = 0;
var max = 10;
var promedio = ( min + max ) / 2;
""", 0, 0, 3
),
(
	"# 6.2 Declaraciones de Impresion",
	True,
"""print " Hola , mundo ! " ;
""", 0, 0, 0
),
(
	"# 6.3 Bloques",
	True,
"""{
	var a = " dentro del bloque " ;
	print a ;
}
""", 0, 0, 1
),
(
	"# 6.4 Declaraciones de Control de Flujo",
	True,
"""var condicion = true;
// if
if ( condicion ) {
	print " Condicion verdadera " ;
} else {
	print " Condicion falsa " ;
}
// while
while ( condicion ) {
	print " Bucle while " ;
}
// for
for ( var i = 0; i < 10; i = i + 1) {
	print i ;
}
""", 0, 4, 1
),
(
	"# 6.5 Declaraciones de Variables",
	True,
"""var nombre = " Compiscript " ;
var edad ;
""", 0, 0, 2
),
(
	"# 6.6 Declaraciones de Funciones",
	True,
"""fun saludar ( nombre ) {
	print " Hola, " + nombre ;
}
""", 0, 1, 1
),
(
	"# 7.1 Declaracion y Asignacion",
	True,
"""var nombre;
var edad = 25;
""", 0, 0, 2
),
(
	"# 7.2 Ambito de las Variables",
	False,
"""{
var a = " dentro del bloque " ;
	print a ; // Imprime : dentro del bloque
}
print a ; // Error : a no esta definida
""", 0, 0, 1
),
(
	"# 7.3 Variables Globales y Locales",
	False,
"""
var globalVar = " soy global";
fun miFuncion () {
	var localVar = " soy local";
	print globalVar; // Acceso permitido
	print localVar; // Acceso permitido
}
miFuncion ();
print globalVar; // Acceso permitido
print localVar; // Error : localVar no esta definida
""", 0, 1, 2
),
(
	"# 7.4 Inicializacion Tardia",
	True,
"""
var miVariable;
miVariable = " Ahora tengo un valor ";
print miVariable ; // Imprime : Ahora tengo un valor
""", 0, 0, 1
),
(
	"# 7.5 Variables Constantes",
	False,
"""fun obtenerConstante () {
	var constante = " No modificar";
	return constante ;
}
var constante = obtenerConstante ();
print constante ; // Imprime : No modificar
// constante = " Intento de modificacion " ; // Error intencional
""", 0, 1, 1
),
(
	"# 8.1 Declaraciones if",
	True,
"""// Estructura basica de if
var condicion = true;
if ( condicion ) {
	// Codigo si la condicion es verdadera
}
else {
	// Codigo si la condicion es falsa
}
""", 0, 2, 1
),
(
	"# 8.2 Declaraciones while",
	True,
"""
var condicion = true;
while ( condicion ) {
	// Codigo a ejecutar mientras la condicion sea verdadera
}
""", 0, 1, 1
),
(
	"# 8.3 Declaraciones for",
	True,
"""for ( var i = 0; i < 10; i = i + 1) {
	// Codigo a ejecutar en cada iteracion
}
""", 0, 1, 1
),
(
	"# 8.4 Declaraciones break y continue",
	True,
"""
var condicion = true;
while ( true ) {
	if ( condicion ) {
		break ;
	}
	// Mas codigo
}
// Uso de continue
for ( var i = 0; i < 10; i = i + 1) {
	if ( i % 2 == 0) {
		continue ;
	}
	print i ; // Solo imprime numeros impares
}
""", 0, 4, 2
),
(
	"# 8.5 Declaraciones return",
	True,
"""fun suma (a, b) {
	return a + b;
}
""", 0, 1, 2
),
(
	"# 9.0 Funciones",
	True,
"""fun saludo ( nombre ) {
	print " Hola, " + nombre ;
}
saludo ( " Compiscript " ) ;
""", 0, 1, 0
),
(
	"# 9.2 Captura de Variables",
	True,
"""fun hacerContador () {
	var i = 0;
	fun contar () {
		i = i + 1;
		print i ;
	}
	return contar ;
}
var contador = hacerContador () ;
contador () ; // "1".
contador () ; // "2".
""", 0, 1, 2
),
(
	"# 9.4 Almacenamiento de Variables Capturadas",
	True,
"""fun crearSumador ( n ) {
	return fun ( x ) {
		return x + n ;
	};
}
var suma5 = crearSumador (5) ;
print suma5 (10) ; // "15".
print suma5 (20) ; // "25".
""", 0, 2, 3
),
(
	"# 10.1 Ejemplo de Captura Tardia",
	True,
"""fun hacerFunciones () {
	var funciones = [];
	for ( var i = 0; i < 3; i = i + 1) {
		fun imprimir () {
			print i;
		}
		funciones.add ( imprimir ) ;
	}
	return funciones ;
}
var misFunciones = hacerFunciones () ;
misFunciones [0]() ; // "3".
misFunciones [1]() ; // "3".
misFunciones [2]() ; // "3".
""", 0, 3, 4
),
(
	"# 10.2	Uso Practico de las Closures",
	True,
"""fun crearContador () {
	var contador = 0;
	return fun () {
		contador = contador + 1;
		return contador ;
	};
}
var contar = crearContador () ;
print contar () ; // "1".
print contar () ; // "2".
""", 0, 2, 2
),
(
	"# 11.1 Definicion de Clases",
	True,
"""class Persona {
	decirHola () {
		print " Hola , mundo ! " ;
	}
}
""", 1, 1, 0
),
(
	"# 11.2 Instanciacion de Clases",
	True,
"""class Persona {
	decirHola () {
		print " Hola , mundo ! " ;
	}
}
var juan = new Persona () ;
juan.decirHola () ; // Salida : Hola , mundo !
""", 1, 1, 1
),
(
	"# 11.4 Inicializadores",
	True,
"""class Persona {
	init ( nombre ) {
		this.nombre = nombre ;
	}
	decirNombre () {
		print this.nombre ;
	}
}
var juan = new Persona ( " Juan " ) ;
juan.decirNombre () ; // Salida : Juan
""", 1, 2, 3
),
(
	"# 11.5 Campos de Instancia",
	True,
"""class Persona {
	init ( nombre , edad ) {
		this.nombre = nombre ;
		this.edad = edad ;
	}
	presentar () {
		print this.nombre + " tiene " + this.edad + " anios." ;
	}
}
var maria = new Persona ( " Maria " , 30) ;
maria.presentar () ; // Salida : Maria tiene 30 anios .
""", 1, 2, 5
),
(
	"# 11.6 Herencia",
	True,
"""class Persona {
	init ( nombre ) {
		this.nombre = nombre ;
	}
	decirNombre () {
		print this.nombre ;
	}
}
class Estudiante extends Persona {
	init ( nombre , grado ) {
		super.init ( nombre ) ;
		this.grado = grado ;
	}
	decirGrado () {
		print this.nombre + " esta en " + this.grado + "." ;
	}
}
var ana = new Estudiante ( " Ana " , " tercer grado " ) ;
ana.decirGrado () ; // Salida : Ana esta en tercer grado .
""", 2, 0, 7
)
	]