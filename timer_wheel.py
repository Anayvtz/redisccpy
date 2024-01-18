import threading
import time
from multiprocessing import Condition 
import memdb

class timer_wheel:

	def __init__(self,memdb):
		self.tmrlst = []
		self.memdb = memdb
		self.cv = Condition()
		self.tmrthr = threading.Thread(target=self.manage_timers)
		self.tmrthr.start()

	def __del__(self):
		self.tmrthr.join()

	def insert(self,key,expiresec):
		if len(self.tmrlst) == 0:
			print("timer wheel insert to EMPTY list")
			self.tmrlst.append((key,expiresec))
			with self.cv:
				self.cv.notify_all()
			return
		first_tuple = self.tmrlst[0]
		if expiresec < first_tuple[1]:
			print("timer wheel insert in FRONT of list")
			first_expire = first_tuple[1]
			iexpire = int(first_expire) 
			iexpire -= int(expiresec)
			y = list(first_tuple)
			y[1] = str(iexpire)
			self.tmrlst[0] = tuple(y)
			#first_tuple[1] = str(iexpire)
			self.tmrlst.insert(0,(key,expiresec))
			with self.cv:
				self.cv.notify_all()
			return
		i = 0
		for j,item in enumerate(self.tmrlst):
			if item[1] > expiresec:
				first_expire = item[1]
				iexpire = int(first_expire) 
				iexpire -= int(expiresec)
				y = list(item)
				y[1] = str(iexpire)
				self.tmrlst[j] = tuple(y)	
				#item[1] = str(iexpire)
				break
			else:
				iexpire = int(expiresec)
				iexpire -= int(item[1])
				expiresec = str(iexpire)
			i += 1
		print("timer wheel insert in MIDDLE of listMIDDLE in pos:"+str(i))
		self.tmrlst.insert(i,(key,expiresec))
		with self.cv:
			self.cv.notify_all()


	def is_first_in_list_chg(self,key):
		if self.tmrlst[0][0]!=key:
			return True
		return False
		
	def manage_timers(self):
		while True:

			while len(self.tmrlst) == 0:
				print("wait on CV on empty list")
				with self.cv:
					self.cv.wait()
			print("wakeup from empty list CV. starting handle list")
			first_tuple = self.tmrlst[0]	
			print("tmrlst front key is:"+first_tuple[0])
			next_expire = first_tuple[1]
			now = time.perf_counter()
			expire = now + int(next_expire)
			while time.perf_counter() < expire:
				print("CV wait till expire:" + str(expire))
				with self.cv:
					self.cv.wait_for(lambda: self.is_first_in_list_chg(first_tuple[0]),int(next_expire))
				print("CV WAKEUP from expire:" + str(expire))
				for item in self.tmrlst:
					print("after CV. tmrlst item:"+item[0]+" expire:"+str(item[1]))
				if (self.tmrlst[0]!=first_tuple): 
					print("CV fix expire time head of list")
					first_tuple = self.tmrlst[0]
					next_expire = first_tuple[1]
					expire = time.perf_counter() + int(next_expire)

			print("CV about to memdb.remove of:"+first_tuple[0])
			rmvdval = self.memdb.remove(first_tuple[0])
			if rmvdval is not None:
				print("CV removed val:"+rmvdval)
			self.tmrlst.pop(0)
			print("tmrlst len is:"+str(len(self.tmrlst)))
		
