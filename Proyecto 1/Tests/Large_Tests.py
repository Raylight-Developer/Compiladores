def getFullCode():
	return [
(
	"# 12.1 Suma Simple",
	True,
"""fun suma (a , b ) {
	return a + b ;
}
print suma (3 , 4) ; // Salida : 7
""",
),
(
	"# 12.2 Bucle y Condicionales",
	True,
"""fun esPar ( num ) {
	return num % 2 == 0;
}
for ( var i = 1; i <= 10; i = i + 1) {
	if ( esPar ( i ) ) {
		print i + " es par " ;
	}
	else {
		print i + " es impar " ;
	}
}
""",
),
(
	"# 12.3 Sistema de Clases y Herencia",
	True,
"""class Persona {
	init ( nombre , edad ) {
		this.nombre = nombre ;
		this.edad = edad ;
	}
	saludar () {
		print " Hola , mi nombre es " + this.nombre ;
	}
}
class Estudiante extends Persona {
	init ( nombre , edad , grado ) {
		super.init ( nombre , edad ) ;
		this.grado = grado ;
	}
	estudiar () {
		print this.nombre + " esta estudiando en " + this.grado + " grado ." ;
	}
}
var juan = Estudiante ( " Juan " , 20 , 3) ;
juan.saludar () ; // Salida : Hola , mi nombre es Juan
juan.estudiar () ; // Salida : Juan esta estudiando en 3 grado
for ( var i = 1; i <= 5; i = i + 1) {
	if ( i % 2 == 0) {
		print i + " es par " ;
	} else {
		print i + " es impar " ;
	}
}
while ( juan.edad < 25) {
	juan.edad = juan.edad + 1;
	print " Edad de Juan : " + juan.edad ;
}
"""
),
(
	"# 12.4 Funcion Recursiva",
	True,
"""fun factorial ( n ) {
	if ( n <= 1) return 1;
	return n * factorial ( n - 1) ;
}
	print " Factorial de 5: " + factorial (5) ; // Salida : Factorial de 5: 120
fun fibonacci ( n ) {
	if ( n <= 1) return n ;
	return fibonacci ( n - 1) + fibonacci ( n - 2) ;
}
print " Fibonacci de 10: " + fibonacci (10) ; // Salida : Fibonacci de 10: 55
"""
)
	]