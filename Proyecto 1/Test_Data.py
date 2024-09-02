def getCode():
	return [
("""
var nombre ;
var edad = 25;
""", True, "# 7.1 Declaracion y Asignacion"),
("""{
var a = " dentro del bloque " ;
print a ; // Imprime : dentro del bloque
}
print a ; // Error : a no esta definida""", False, "# 7.2 Ambito de las Variables"),

("""
var globalVar = " soy global" ;
fun miFuncion () {
var localVar = " soy local" ;
print globalVar ; // Acceso permitido
print localVar ; // Acceso permitido
}
miFuncion () ;
print globalVar ; // Acceso permitido
print localVar ; // Error : localVar no esta definida
""", False, "# 7.3"),

("""
var miVariable;
miVariable = " Ahora tengo un valor ";
print miVariable ; // Imprime : Ahora tengo un valor
""", True, "# 7.4"),

("""fun obtenerConstante () {
var constante = " No modificar " ;
return constante ;
}
var constante = obtenerConstante () ;
print constante ; // Imprime : No modificar
// constante = " Intento de modificacion " ; // Error intencional
""", False, "# 7.5"),
("""// Estructura basica de if
var condicion = true;
if ( condicion ) {
// Codigo si la condicion es verdadera
} else {
// Codigo si la condicion es falsa
}""", True, "# 8.1"),
("""
""", True, "# 8.2")
	]