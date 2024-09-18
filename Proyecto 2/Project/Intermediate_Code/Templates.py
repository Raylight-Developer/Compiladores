from CompiScript.CompiscriptVisitor import CompiscriptVisitor
from CompiScript.CompiscriptParser import CompiscriptParser
from CompiScript.CompiscriptLexer import CompiscriptLexer

from Include import *
from Lace import *

from GUI.Symbol_Table import *
from GUI.Logger import *

from Analyzer.Symbols import *
from Analyzer.Scope import *

class Intermediate_Code_Generator(CompiscriptVisitor):
	def __init__(self):
		self.label_count = -1
		self.temp_count = -1
		self.code = []

	def new_temp(self):
		self.temp_count += 1
		return f"T_{self.temp_count}"
	
	def new_label(self):
		self.label_count += 1
		return f"L_{self.label_count}"

	def generate_if(self):
		pass

	def generate_while(self):
		pass

	def generate_for(self):
		pass