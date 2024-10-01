from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *

from Analyzer.Symbols import *
from Analyzer.Scope import *

from .Classes import *

class Tac_Info:
	def __init__(self, ID: str = "", data: Dict[str, Any] = {}):
		self.ID = ID
		self.data = data

class TAC_Generator():
	def __init__(self, scope_tracker: Scope_Tracker = None):
		super().__init__()
		self.scope_tracker = scope_tracker
		self.label_count = -1
		self.temp_count = -1
		self.code = Lace()
		self.tac_info: Dict[Union[Function, Variable, Class, Function_Parameter], Tac_Info] = {}
		
		self.flags = {
			"visit_instantiation": 0,
			"visit_assignment": 0,
			"visit_comparison": 0,
			"visit_expression": 0,
			"visit_parameters": 0,
			"visit_arguments": 0,
			"visit_equality" : 0,
			"visit_function": 0,
			"visit_variable": 0,
			"visit_primary": 0,
			"visit_factor": 0,
			"visit_array": 0,
			"visit_super": 0,
			"visit_unary": 0,
			"visit_call": 0,
			"visit_term": 0,
			"visit_and": 0,
			"visit_or": 0,
		}

	def new_temp(self):
		self.temp_count += 1
		return f"T_{self.temp_count}"
	
	def new_label(self):
		self.label_count += 1
		return f"L_{self.label_count}"

	def declareClass(self, struct: Class):
		temp_id = self.new_temp()
		self.code << NL() << f"// Class:     [{temp_id}] {struct.ID}"
		self.tac_info[struct] = Tac_Info(temp_id, {})

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
		self.tac_info[function] =  Tac_Info(block_id, { "Block ID" : block_id, "Block" : f"{function.data} // FUNCTION CODE" })

	def declareVariable(self, variable: Variable):
		temp_id = self.new_temp()
		#self.code << NL()
		#self.code << f"// Variable:  [{temp_id}] "
		#if variable.member:
		#	self.code << variable.member.ID << "."
		#self.code << variable.ID
		self.tac_info[variable] =  Tac_Info(temp_id)

	def declareParameter(self, parameter: Function_Parameter):
		temp_id = self.new_temp()
		#self.code << NL()
		#self.code << f"// Parameter:  [{temp_id}] "
		#self.code << parameter.function.ID << "." << parameter.ID
		self.tac_info[parameter] = Tac_Info(temp_id)

	def declareAnonFunction(self, function: Function):
		#temp_id = self.new_temp()
		block_id = self.new_label()
		#self.code << NL()
		#self.code << f"// Anon Function:  [{block_id}] [{block_id}] {function.ID}"
		self.tac_info[function] = Tac_Info(block_id, { "Block" : block_id })

	def assignVariable(self, variable: Variable):
		self.code << NL() << "// Assign Variable [" << variable.ID << "] {"
		self.code += 1
		self.code << NL()
		#expression = self.visit(variable.ctx.expression())
		expression = variable.ctx.expression().getText()
		self.code << self.tac_info[variable].ID << ": " << expression
		self.code -= 1
		self.code << NL() << "// }" << NL()

	def callFunction(self, function: Function, call_params: List[Container]):
		self.code << NL() << "// Call Function ["
		if function.member:
			if function.member.parent:
				self.code << "Super<" << function.member.parent.ID << ">."
			else:
				self.code << function.member.ID << "."
		self.code << function.ID << "] {"
		self.code += 1
		self.code << NL()
		for i, param in enumerate(call_params):
			self.code << self.tac_info[function.parameters[i]].ID << ": "
			if param.type == Type.STRING:
				self.code << '"' << param.data << '"' << NL()
			elif param.type in [Type.FLOAT, Type.INT]:
				self.code << param.data << NL()
			else:
				self.code << param.data << NL()
		self.code << self.tac_info[self.scope_tracker.lookupFunction(function.ID, function.member)].data["Block"]
		self.code -= 1
		self.code << NL() << "// }" << NL()

	def generate_if(self, if_expr: List[str] = [], if_condition: str = "", if_body: List[str] = [], else_body: List[str] = []):
		if_label = self.new_label()
		end_label = self.new_label()

		self.code << NL() << "\n".join(if_expr)
		self.code << NL()
		self.code << NL() << f"IF ({if_condition}) GO_TO {if_label}"
		self.code += 1
		self.code << NL() << "\n".join(else_body)
		self.code -= 1
		self.code << NL() << f"GO_TO {end_label}"
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
		self.code << NL() << f"IF ({while_condition}) GO_TO {end_label}"
		self.code += 1
		self.code << NL() << "\n".join(while_body)
		self.code << NL() << while_update << " // Update While Condition"
		self.code -= 1
		self.code << NL() << f"GO_TO {loop_start_label}"
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
		self.code << NL() << f"IF ({for_condition}) GO_TO {end_label}"
		self.code << NL()
		self.code << NL() << "\n".join(for_body)
		self.code << NL() << for_update << " // Update For Condition"
		self.code << NL()
		self.code << NL() << f"GO_TO {loop_start_label}"
		self.code -= 1
		self.code << NL()
		self.code << NL() << f"{end_label}:"