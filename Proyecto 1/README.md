Alejandro Martinez - 21430

Samuel Argueta - 211024

# Run

## Dependencies:
```bash
pip install antlr4-python3-runtime
pip install graphviz
pip install PyQt6
```

## Launch:
```bash
python3 Main.py
```

## Compile Compiscript python Files:
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
antlr -Dlanguage=Python3 -visitor -o ../ Compiscript.g4
```