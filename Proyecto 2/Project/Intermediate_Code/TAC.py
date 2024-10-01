from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *

from Analyzer.Symbols import *
from Analyzer.Scope import *

class Tac_Info:
	def __init__(self, ID: str = "", data: Dict[str, Any] = {}):
		self.ID = ID
		self.data = data

class TAC_Generator: #(CompiscriptVisitor):
	def __init__(self):
		self.scope_tracker: Scope_Tracker = None
		self.label_count = -1
		self.temp_count = -1
		self.code = Lace()

	def new_temp(self):
		self.temp_count += 1
		return f"T_{self.temp_count}"
	
	def new_label(self):
		self.label_count += 1
		return f"L_{self.label_count}"

	def declareClass(self, struct: Class):
		temp_id = self.new_temp()
		self.code << NL() << f"// Class:     [{temp_id}] {struct.ID}"
		return Tac_Info(temp_id, {})

	def declareFunction(self, function: Function):
		#temp_id = self.new_temp()
		block_id = self.new_label()
		self.code << NL() << "// Declare Function ["
		if function.member:
			self.code << function.member.ID << "."
		self.code << function.ID << "] {"
		self.code += 1
		self.code << NL() << block_id << ":"
		self.code -= 1
		self.code << NL() << "// }" << NL()
		return Tac_Info(block_id, { "Block ID" : block_id })

	def declareVariable(self, variable: Variable):
		temp_id = self.new_temp()
		#self.code << NL()
		#self.code << f"// Variable:  [{temp_id}] "
		#if variable.member:
		#	self.code << variable.member.ID << "."
		#self.code << variable.ID
		return Tac_Info(temp_id)

	def declareParameter(self, parameter: Function_Parameter):
		temp_id = self.new_temp()
		#self.code << NL()
		#self.code << f"// Parameter:  [{temp_id}] "
		#self.code << parameter.function.ID << "." << parameter.ID
		parameter.tac_data = Tac_Info(temp_id)

	def declareAnonFunction(self, function: Function):
		#temp_id = self.new_temp()
		block_id = self.new_label()
		#self.code << NL()
		#self.code << f"// Anon Function:  [{block_id}] [{block_id}] {function.ID}"
		return Tac_Info(block_id, { "Block ID" : block_id })

	def assignVariable(self, variable: Variable, tac_data : Dict[str, Any]):
		self.code << NL() << "// Assign Variable [" << variable.ID << "] {"
		self.code += 1
		self.code << NL()
		expression = tac_data["expression"]
		if isinstance(tac_data["expression"], list):
			expression = ' '.join(tac_data["expression"])
		self.code << variable.tac_data.ID << ": " << expression
		self.code -= 1
		self.code << NL() << "// }" << NL()

	def callFunction(self, function: Function, call_params: List[Container]):
		self.code << NL() << "// Call Function [" << function.ID << "] {"
		self.code += 1
		self.code << NL()
		for i, param in enumerate(call_params):
			self.code << function.parameters[i].tac_data.ID << ": "
			if param.type == Type.STRING:
				self.code << '"' << param.data << '"' << NL()
			elif param.type in [Type.FLOAT, Type.INT]:
				self.code << param.data << NL()
			else:
				self.code << param.data << NL()
		self.code << "GOTO " << self.scope_tracker.lookupFunction(function.ID, function.member).tac_data.data["Block ID"] << " // "
		if function.member:
			self.code << function.member.ID << "."
		self.code << function.ID
		self.code -= 1
		self.code << NL() << "// }" << NL()

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