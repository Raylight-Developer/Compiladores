Alejandro Martinez - 21430

Samuel Argueta - 211024

```bash
docker build --rm . -t proyecto
```
```bash
docker run --name proyecto-1 --rm -ti -v "${PWD}/program:/program" proyecto
```
```bash
docker attach proyecto-1
```
```bash
antlr -Dlanguage=Python3 -visitor Compiscript.g4
```