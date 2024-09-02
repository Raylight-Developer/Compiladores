def getSmallCode():
	return [
(
	"# 7.1 Declaracion y Asignacion",
	True,
"""
var nombre ;
var edad = 25;
"""
),
(
	"# 7.2 Ambito de las Variables",
	False,
"""{
var a = " dentro del bloque " ;
	print a ; // Imprime : dentro del bloque
}
print a ; // Error : a no esta definida
"""
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
"""
),
(
	"# 7.4 Inicializacion Tardia",
	True,
"""
var miVariable;
miVariable = " Ahora tengo un valor ";
print miVariable ; // Imprime : Ahora tengo un valor
"""
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
"""
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
""",
),
(
	"# 8.2 Declaraciones while",
	True,
"""
var condicion = true;
while ( condicion ) {
	// Codigo a ejecutar mientras la condicion sea verdadera
}
"""
),
(
	"# 8.3 Declaraciones for",
	True,
"""for ( var i = 0; i < 10; i = i + 1) {
	// Codigo a ejecutar en cada iteracion
}
"""
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
"""
),
(
	"# 8.5 Declaraciones return",
	True,
"""fun suma (a, b) {
	return a + b;
}
"""
),
(
	"# 9.0 Funciones",
	True,
"""fun saludo ( nombre ) {
print " Hola, " + nombre ;
}
saludo ( " Compiscript " ) ;
""",
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
""",
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
""",
),
(
	"# 10.1 Ejemplo de Captura Tard ́ıa",
	True,
"""fun hacerFunciones () {
	var funciones = [];
	for ( var i = 0; i < 3; i = i + 1) {
		fun imprimir () {
			print i;
		}
		funciones . add ( imprimir ) ;
	}
	return funciones ;
}
var misFunciones = hacerFunciones () ;
misFunciones [0]() ; // "3".
misFunciones [1]() ; // "3".
misFunciones [2]() ; // "3".
""",
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
""",
),
(
	"# 11.1 Definicion de Clases",
	True,
"""class Persona {
	decirHola () {
		print " Hola , mundo ! " ;
	}
}
""",
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
juan . decirHola () ; // Salida : Hola , mundo !
""",
),
(
	"# 11.4 Inicializadores",
	True,
"""class Persona {
	init ( nombre ) {
		this . nombre = nombre ;
	}
	decirNombre () {
		print this . nombre ;
	}
}
var juan = new Persona ( " Juan " ) ;
juan . decirNombre () ; // Salida : Juan
""",
),
(
	"# 11.5 Campos de Instancia",
	True,
"""class Persona {
	init ( nombre , edad ) {
		this . nombre = nombre ;
		this . edad = edad ;
	}
	presentar () {
		print this . nombre + " tiene " + this . edad + " anios . " ;
	}
}
var maria = new Persona ( " Maria " , 30) ;
maria . presentar () ; // Salida : Maria tiene 30 anios .
""",
),
(
	"# 11.6 Herencia",
	True,
"""class Persona {
	init ( nombre ) {
		this . nombre = nombre ;
	}
	decirNombre () {
		print this . nombre ;
	}
}
class Estudiante extends Persona {
	init ( nombre , grado ) {
		super . init ( nombre ) ;
		this . grado = grado ;
	}
	decirGrado () {
		print this . nombre + " esta en " + this . grado + " . " ;
	}
}
var ana = new Estudiante ( " Ana " , " tercer grado " ) ;
ana . decirGrado () ; // Salida : Ana esta en tercer grado .
""",
)
	]