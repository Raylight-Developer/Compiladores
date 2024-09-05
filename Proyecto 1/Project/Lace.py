from io import StringIO

class Lace:
	def __init__(self):
		self.data = StringIO()
		self.current_tab = 0

	def __lshift__(self, val):
		if isinstance(val, S):
			count = val.count
			while count > 0:
				self.data.write(" ")
				count -= 1
		elif isinstance(val, NL):
			count = val.count
			tabs = self.current_tab
			while count > 0:
				self.data.write("\n")
				count -= 1
			if val.count > 0:
				while tabs > 0:
					self.data.write(self.character)
					tabs -= 1
		elif isinstance(val, TAB):
			count = self.current_tab + val.count
			while count > 0:
				self.data.write("\t")
				count -= 1
		elif isinstance(val, CHR):
			count = val.count
			while count > 0:
				self.data.write(self.character)
				count -= 1
		elif isinstance(val, DEL):
			temp_data = self.data.getvalue()
			self.data = StringIO()
			if val.count < len(temp_data):
				self.data.write(temp_data[val.count:])
		elif isinstance(val, POP):
			temp_data = self.data.getvalue()
			self.data = StringIO()
			if val.count < len(temp_data):
				self.data.write(temp_data[:len(temp_data) - 1 - val.count])
		elif isinstance(val, Lace):
			self.data.write(val.data.getvalue())
		elif isinstance(val, str):
			self.data.write(val)
		elif isinstance(val, StringIO):
			self.data.write(val.getvalue())
		elif isinstance(val, bool):
			self.data.write("true" if val else "false")
		return self

	def __rshift__(self, value):
		return self

	def __iadd__(self, value):
		self.current_tab += value
		return self

	def __isub__(self, value):
		self.current_tab -= value
		return self

	def __post_inc__(self):
		self.current_tab += 1
		return self

	def __post_dec__(self):
		self.current_tab -= 1
		return self

	def clear(self):
		self.data = StringIO()
		self.current_tab = 0
		return self

	def __str__(self):
		return self.data.getvalue()

class S:
	def __init__(self, count = 1):
		self.count = count

class NL:
	def __init__(self, count = 1):
		self.count = count

class TAB:
	def __init__(self, count = 1):
		self.count = count

class CHR:
	def __init__(self, count = 1):
		self.count = count

class DEL:
	def __init__(self, count = 1):
		self.count = count

class POP:
	def __init__(self, count = 1):
		self.count = count