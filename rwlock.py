
from threading import Lock, Condition 
import threading

class rwlock:
	def __init__(self):
		self.rcount = 0
		self.wcount = 0
		self.rlock = threading.Lock()
		self.wlock = threading.Lock()
		self.rcv = threading.Condition(self.rlock)
		self.wcv = threading.Condition(self.wlock)

	def rdr_lock(self):
		self.rlock.acquire()
		self.rcount += 1
		while self.wcount > 0:
			self.rcv.wait()
		self.rlock.release()

	def rdr_unlock(self):
		self.rlock.acquire()
		self.rcount -= 1
		if self.wcount > 0:
			self.wcv.notify_all()
		self.rlock.release()

	def wrtr_lock(self):
		self.wlock.acquire()
		self.wcount += 1
		while self.rcount > 0 or self.wcount > 1:
			self.wcv.wait()
		self.wlock.release()

	def wrtr_unlock(self):
		self.wlock.acquire()
		self.wcount -= 1
		if self.rcount > 0:
			m_rcv.notify_all()
		elif self.wcount > 0:
			m_wcv.notify_all()
		self.wlock.release()
