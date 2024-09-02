def getCode():
	return [
("""
var nombre ;
var edad = 25;
""", True),
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
""", False),
("""
var miVariable;
miVariable = " Ahora tengo un valor ";
print miVariable ; // Imprime : Ahora tengo un valor
""", True),
	]