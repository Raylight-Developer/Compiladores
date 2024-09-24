from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *

from Analyzer.Symbols import *
from Analyzer.Scope import *

class TAC_Generator: #(CompiscriptVisitor):
	def __init__(self):
		self.label_count = -1
		self.temp_count = -1
		self.code = Lace()

	def new_temp(self):
		self.temp_count += 1
		return f"T_{self.temp_count}"
	
	def new_label(self):
		self.label_count += 1
		return f"L_{self.label_count}"

	def declareClass(self, value: Class):
		temp_id = self.new_temp()
		self.code << NL()
		self.code << temp_id << "; // Class: " + value.ID
		return temp_id

	def declareFunction(self, value: Function):
		temp_id = self.new_temp()
		self.code << NL()
		self.code << temp_id << "; // Function: " + value.ID
		return temp_id

	def declareVariable(self, value: Variable):
		temp_id = self.new_temp()
		self.code << NL()
		self.code << temp_id << "; // Variable: " + value.ID
		return temp_id

	def generate_if(self, if_expr: List[str] = [], if_condition: str = "", if_body: List[str] = [], else_body: List[str] = []):
		if_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(if_expr)
		self.code << NL()
		self.code << NL() << f"IF ({if_condition}) GOTO {if_label}"
		self.code += 1
		self.code << NL() << "\n".join(else_body)
		self.code -= 1
		self.code << NL() << f"GOTO {end_label}"
		self.code << NL()
		self.code << NL() << f"{if_label}:"
		self.code += 1
		self.code << NL() << "\n".join(if_body)
		self.code -= 1
		self.code << NL()
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"

	def generate_while(self, while_expr: List[str] = [], while_condition: str = "", while_update: str = "", while_body: List[str] = []):
		loop_start_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(while_expr)
		self.code << NL()
		self.code << NL() << f"{loop_start_label}:"
		self.code += 1
		self.code << NL() << f"IF ({while_condition}) GOTO {end_label}"
		self.code += 1
		self.code << NL() << "\n".join(while_body)
		self.code << NL() << while_update << " // Update While Condition"
		self.code -= 1
		self.code << NL() << f"GOTO {loop_start_label}"
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"

	def generate_for(self, for_expr: List[str] = [], for_condition: str = "", for_update: str = "", for_body: List[str] = []):
		loop_start_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(for_expr)
		self.code << NL()
		self.code << NL() << f"{loop_start_label}:"
		self.code += 1
		self.code << NL() << f"IF ({for_condition}) GOTO {end_label}"
		self.code << NL()
		self.code << NL() << "\n".join(for_body)
		self.code << NL() << for_update << " // Update For Condition"
		self.code << NL()
		self.code << NL() << f"GOTO {loop_start_label}"
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"