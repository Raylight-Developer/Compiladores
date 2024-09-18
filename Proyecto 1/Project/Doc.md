# Run

## Dependencies:
```bash
pip install antlr4-python3-runtime
pip install graphviz
pip install PyQt6
```

## Launch:
#### IDE Compiler:
```bash
python3 Main.py
```
#### Pre-Made Tests:
```bash
python3 Test.py
```
Arguments:
```python
--render=BOOL: Union [ True | False ] # (Optional) Whether to Save The Syntax Tree(s) to a png.

Example: "python3 Test.py --render=False"
```
# Architecture
The [Semantic Analyzer](Semantic_Analyzer.py) Is the implementation of the ANTLR Visitor class. It contains all relevant data to track scopes, build maps and eventulally generate the [Symbol Table](Symbol_Table.py).

The [Main](Main.py) file contains the GUI initialization. The GUI itself contains:
* A Text Editor with Syntax Highlighting to input the code.
* A Log with all relevant information to the backend and what the compiler is doing.
* Three symbol tables for Functions, Variables and Classes contained in different tabs.
* The String Tree Output of the Generated Syntax

On compilation, the code will be submitted and preprocessed with the [Compiscript Lexer](CompiscriptLexer.py), which then passes through the [Compiscript Parser](CompiscriptParser.py) to generate the [Syntax Tree](Output/Syntax-Graph.png). This Syntax Tree then passes to the [Semantic Analyzer](Semantic_Analyzer.py) which visits every node, generating all the aformentioned data to finally be displayed on the GUI.

### The [Semantic Analyzers](Semantic_Analyzer.py) Variables:
``` python
inside_loop: bool # To Track Scope
inside_block_fun_if: bool # To Track Scope

global_variables: Dict[str, ParserRuleContext] # To Track Scopes
local_variables: Dict[str, ParserRuleContext] # To Track Scopes
declared_functions: Set[str] # To Track Functions

table_functions : Symbol_Table  # To Add Symbols and also track current scope
table_variables : Symbol_Table  # To Add Symbols and also track current scope
table_classes   : Symbol_Table  # To Add Symbols and also track current scope

log = log                       # To log and debug
```


# CompiScript and Semantic Analisis Examples
For all examples, Run:
* `python Test.py`

Inputs:
* [Unit Tests](Tests/Small_Tests.py)
* [Comprehensive Tests](Tests/Large_Tests.py)

Example Outputs:
## Success
![alt text](Images/image-1.png)
## Success
![alt text](Images/image-2.png)
## Success (With Warning For Failure)
![alt text](Images/image-3.png)
## Failure
![alt text](Images/image-4.png)