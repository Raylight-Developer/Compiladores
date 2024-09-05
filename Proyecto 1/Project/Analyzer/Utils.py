from Include import *

K = TypeVar('K')
V = TypeVar('V')
class BiMap(Generic[K, V]):
	def __init__(self):
		self.forward_map: Dict[K, V] = {}
		self.reverse_map: Dict[V, K] = {}

	def add(self, key: K, value: V):
		self.forward_map[key] = value
		self.reverse_map[value] = key

	def removeByKey(self, key: K):
		if key in self.forward_map:
			value = self.forward_map.pop(key)
			del self.reverse_map[value]
		else:
			raise KeyError("Key not found")

	def removeByVal(self, value: V):
		if value in self.reverse_map:
			key = self.reverse_map.pop(value)
			del self.forward_map[key]
		else:
			raise KeyError("Value not found")

	def getVal(self, key: K) -> V:
		return self.forward_map.get(key)

	def getKey(self, value: V) -> K:
		return self.reverse_map.get(value)

	def keyExists(self, key: K):
		return key in self.reverse_map

	def valExists(self, val: V):
		return val in self.forward_map