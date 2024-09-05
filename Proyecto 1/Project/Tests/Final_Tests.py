def getFinalCode():
	return [
(
	"# Default",
	True,
"""class Persona {
	init(nombre, edad) {
		this.nombre = nombre;
		this.edad = edad;
		this.color = "rojo";
	}

	saludar() {
		print "Hola, mi nombre es " + this.color;
	}
}

class Estudiante extends Persona {
	init(nombre, edad, grado) {
		super.init(nombre, edad);
		this.grado = grado;
	}

	estudiar() {
		print this.nombre + " esta estudiando en " + this.grado + " grado.";
	}
}

var nombre = "Erick";

var ropero = new Persona(nombre, 20);
var juan = new Estudiante(nombre, 20, 3);
juan.saludar();    // Salida: Hola, mi nombre es Juan
juan.estudiar();   // Salida: Juan esta estudiando en 3 grado

for (var i = 1; i <= 5; i = i + 1) {
	if (i % 2 == 0) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

while (juan.edad < 25) {
	juan.edad = juan.edad + 1;
	print "Edad de Juan: " + juan.edad;
}
""", 0, 0, 0
),
(
	"# ERROR [class Estudiante extends Persona] &| [var ropero = new Persona(nombre, 20);] class Personas not defined",
	False,
"""class Personas {
	init(nombre, edad) {
		this.nombre = nombre;
		this.edad = edad;
		this.color = "rojo";
	}

	saludar() {
		print "Hola, mi nombre es " + this.color;
	}
}

class Estudiante extends Persona {
	init(nombre, edad, grado) {
		super.init(nombre, edad);
		this.grado = grado;
	}

	estudiar() {
		print this.nombre + " esta estudiando en " + this.grado + " grado.";
	}
}

var nombre = "Erick";

var ropero = new Persona(nombre, 20);
var juan = new Estudiante(nombre, 20, 3);
juan.saludar();    // Salida: Hola, mi nombre es Juan
juan.estudiar();   // Salida: Juan esta estudiando en 3 grado

for (var i = 1; i <= 5; i = i + 1) {
	if (i % 2 == 0) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

while (juan.edad < 25) {
	juan.edad = juan.edad + 1;
	print "Edad de Juan: " + juan.edad;
}
""", 0, 0, 0
),
(
	"# ERROR [var ropero = new Personas(nombre, 20);] Personas is not defined",
	False,
"""class Persona {
	init(nombre, edad) {
		this.nombre = nombre;
		this.edad = edad;
		this.color = "rojo";
	}

	saludar() {
		print "Hola, mi nombre es " + this.color;
	}
}

class Estudiante extends Persona {
	init(nombre, edad, grado) {
		super.init(nombre, edad);
		this.grado = grado;
	}

	estudiar() {
		print this.nombre + " esta estudiando en " + this.grado + " grado.";
	}
}

var nombre = "Erick";

var ropero = new Personas(nombre, 20);
var juan = new Estudiante(nombre, 20, 3);
juan.saludar();    // Salida: Hola, mi nombre es Juan
juan.estudiar();   // Salida: Juan esta estudiando en 3 grado

for (var i = 1; i <= 5; i = i + 1) {
	if (i % 2 == 0) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

while (juan.edad < 25) {
	juan.edad = juan.edad + 1;
	print "Edad de Juan: " + juan.edad;
}
""", 0, 0, 0
),
(
	"# ERROR [juan.saludar(nombre);] takes no arguments",
	False,
"""class Persona {
	init(nombre, edad) {
		this.nombre = nombre;
		this.edad = edad;
		this.color = "rojo";
	}

	saludar() {
		print "Hola, mi nombre es " + this.color;
	}
}

class Estudiante extends Persona {
	init(nombre, edad, grado) {
		super.init(nombre, edad);
		this.grado = grado;
	}

	estudiar() {
		print this.nombre + " esta estudiando en " + this.grado + " grado.";
	}
}

var nombre = "Erick";

var ropero = new Persona(nombre, 20);
var juan = new Estudiante(nombre, 20, 3);
juan.saludar(nombre);    // Salida: Hola, mi nombre es Juan
juan.estudiar();   // Salida: Juan esta estudiando en 3 grado

for (var i = 1; i <= 5; i = i + 1) {
	if (i % 2 == 0) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

while (juan.edad < 25) {
	juan.edad = juan.edad + 1;
	print "Edad de Juan: " + juan.edad;
}
""", 0, 0, 0
),
(
	"# ERROR [if (j % 2 == 0)] j is not defined",
	False,
"""class Persona {
	init(nombre, edad) {
		this.nombre = nombre;
		this.edad = edad;
		this.color = "rojo";
	}

	saludar() {
		print "Hola, mi nombre es " + this.color;
	}
}

class Estudiante extends Persona {
	init(nombre, edad, grado) {
		super.init(nombre, edad);
		this.grado = grado;
	}

	estudiar() {
		print this.nombre + " esta estudiando en " + this.grado + " grado.";
	}
}

var nombre = "Erick";

var ropero = new Persona(nombre, 20);
var juan = new Estudiante(nombre, 20, 3);
juan.saludar();    // Salida: Hola, mi nombre es Juan
juan.estudiar();   // Salida: Juan esta estudiando en 3 grado

for (var i = 1; i <= 5; i = i + 1) {
	if (j % 2 == 0) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

while (juan.edad < 25) {
	juan.edad = juan.edad + 1;
	print "Edad de Juan: " + juan.edad;
}
""", 0, 0, 0
),
(
	"# ERROR [if(i % 2)] if expression (i % 2) is not a boolean operation",
	False,
"""class Persona {
	init(nombre, edad) {
		this.nombre = nombre;
		this.edad = edad;
		this.color = "rojo";
	}

	saludar() {
		print "Hola, mi nombre es " + this.color;
	}
}

class Estudiante extends Persona {
	init(nombre, edad, grado) {
		super.init(nombre, edad);
		this.grado = grado;
	}

	estudiar() {
		print this.nombre + " esta estudiando en " + this.grado + " grado.";
	}
}

var nombre = "Erick";

var ropero = new Persona(nombre, 20);
var juan = new Estudiante(nombre, 20, 3);
juan.saludar();    // Salida: Hola, mi nombre es Juan
juan.estudiar();   // Salida: Juan esta estudiando en 3 grado

for (var i = 1; i <= 5; i = i + 1) {
	if (i % 2) {
		print i + " es par";
	} else {
		print i + " es impar";
	}
}

while (juan.edad < 25) {
	juan.edad = juan.edad + 1;
	print "Edad de Juan: " + juan.edad;
}
""", 0, 0, 0
)
	]