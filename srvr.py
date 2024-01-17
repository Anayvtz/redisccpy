
import socket
import threading
import select
import commands
import memdb

class srvr:

	def __init__(self):
		self.skt = 0

	def open_socket(self):
		self.skt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.skt.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

class redis_srvr(srvr):
	
	def __init__(self):
		self.port = 6379
		self.ip = "127.0.0.1"
		self.memdb = memdb.memdb()

	def bind_socket(self):
		self.skt.bind((self.ip,self.port))

	def listen_socket(self):
		self.skt.listen(0)

	def conn_mgr(self,clntSkt,cltAddr):
		#while True:
		data = clntSkt.recv(1024)
		if not data:
			print("no data recieved")
		#		break
		print ("recv data:" + str(data))

		cmdmgr = commands.cmds_srvr()
		strdata = data.decode()
		print("datastr:"+strdata)
		rspns = cmdmgr.process_cmd_and_response(strdata,self.memdb)
		print("process response:" + rspns)
		if rspns != "":
			clntSkt.send(rspns.encode())
		
	def activate(self):
		self.open_socket()
		self.bind_socket()
		self.listen_socket()
		threads = []

		while True:

			rd_skt,wrt_skt,err_skt = select.select([self.skt],[],[])
			for sock in rd_skt:
				clnt_skt, clnt_addr = self.skt.accept()
				acceptorthr = threading.Thread(target=self.conn_mgr,args=(clnt_skt,clnt_addr))
				acceptorthr.start()
				threads.append(acceptorthr)

		for thr in threads:
			thr.join()
