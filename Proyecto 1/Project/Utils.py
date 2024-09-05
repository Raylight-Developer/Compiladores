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

	def remove_by_key(self, key: K):
		if key in self.forward_map:
			value = self.forward_map.pop(key)
			del self.reverse_map[value]
		else:
			raise KeyError("Key not found")

	def remove_by_value(self, value: V):
		if value in self.reverse_map:
			key = self.reverse_map.pop(value)
			del self.forward_map[key]
		else:
			raise KeyError("Value not found")

	def get_value(self, key: K) -> V:
		return self.forward_map.get(key)

	def get_key(self, value: V) -> K:
		return self.reverse_map.get(value)