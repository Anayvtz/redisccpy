
import timer_wheel
from multiprocessing import Condition

INITIAL_CAPACITY = 1024

class hash_node:
	
	def __init__(self,key,value):
		self.key = key
		self.value = value
		self.next = None

class hash_table:
	
	def __init__(self):
		self.capacity = INITIAL_CAPACITY
		self.size = 0
		self.buckets = [None]*self.capacity

	def hash_key(self,key):
		hk = hash(key)
		hk = hk % self.capacity
		return hk

	def insert(self,key,value):
		self.size += 1
		indx = self.hash_key(key)
		node = self.buckets[indx]
		if node is None:
			self.buckets[indx] = hash_node(key,value)	
			return True
		prev = node
		while node is not None and node.key!=key:
			prev = node
			node = node.next
		if node is None:
			prev.next = hash_node(key,value)
		else:
			node.value = value
		return True

	def find(self,key):
		indx = self.hash_key(key)
		node = self.buckets[indx]
		if node is None:
			return None
		while node is not None and node.key != key:
			node = node.next
		if node is None:
			return None
		else:
			return node.value

	def remove(self,key):
		print("about to remove from hash key:"+key)
		indx = self.hash_key(key)
		node = self.buckets[indx]
		prev = None
		while node is not None and node.key != key:
			prev = node
			node = node.next
		if node is None:
			print("key:"+key+" not found. didnt remove")
			return None
		else:
			self.size -= 1
			result = node.value
			if prev is None:
				print("in remove from hash. prev is None. remove first")
				if node.next is not None:
					self.buckets[indx] = node.next
				else:
					self.buckets[indx] = hash_node(None,None)
			else:
				print("ABOUT to RMV key:"+key)
				prev.next = prev.next.next
			return result


class memdb(hash_table):
	def __init__(self):
		super().__init__()
		self.tmrw = timer_wheel.timer_wheel(self)

	def insert_with_expire(self,key,value,expiresec):
		self.insert(key,value)
		self.tmrw.insert(key,expiresec)

