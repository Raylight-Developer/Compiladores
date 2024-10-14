from Include import *

K = TypeVar('K')
V = TypeVar('V')
class BiMap(Generic[K, V]):
	def __init__(self):
		self.map: Dict[K, V] = {}

	def add(self, key: K, value: V):
		self.map[key] = value

	def removeByKey(self, key: K):
		if key in self.map:
			self.map.pop(key)
		else:
			raise KeyError(f"Key {key} not found")

	def removeByVal(self, value: V):
		if value in self.map.values():
			for k, v in self.map.items():
				if v == value:
					self.map.pop(k)
		else:
			raise KeyError(f"Value {value} not found")

	def getVal(self, key: K) -> V:
		if key in self.map.keys():
			return self.map.get(key)
		raise KeyError(f"Key {key} not found")

	def getKey(self, value: V) -> K:
		if value in self.map.values():
			for k, v in self.map.items():
				if v == value:
					return k
			return None
		raise KeyError(f"Value {value} not found")

	def keyExists(self, key: K):
		return key in self.map.keys()

	def valExists(self, val: V):
		return val in self.map.values()
	
	def getKeys(self):
		return self.map.keys()

	def getValues(self):
		return self.map.values()
	
	def __contains__(self, item):
		return item in self.map.keys()
	
from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener(ErrorListener):
	def __init__(self):
		super(MyErrorListener, self).__init__()

	def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
		print(f"Syntax error at line {line}:{column} - {msg}")
		raise Exception(f"Syntax error at line {line}:{column} - {msg}")
