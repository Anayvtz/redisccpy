from enum import Enum
import resp
import memdb

class cmds(Enum):
	PING = "PING"
	GET = "GET"
	SET = "SET"
	SETEX = "SETEX"

class commands:

	def __init__(self):
		pass

	def find_cmd(self,cmdstr):
		rsp = resp.resp()
		token = rsp.dsrlz_simple(cmdstr)
		if len(token)==0:
			print("dsrlz_simple returned empty token")
			return ""
		for cmd in cmds:
			if cmdstr[1::len(cmdstr)].find(cmd.name):
				print("simple found cmd:"+cmd.name)
				return cmd.name 
		return ""

	def find_cmd_bulk(self,cmdstr):
		rsp = resp.resp()
		token = rsp.dsrlz_bulk(cmdstr)
		if len(token)==0:
			print("dsrlz_bulk returned empty token")
			return ""
		for cmd in cmds:
			if cmdstr[1::len(cmdstr)].find(cmd.name):
				print("bulk found cmd:"+cmd.name)
				return cmd.name 
		return ""

	def find_cmd_arr(self,cmdstr):
		rsp = resp.resp()
		lst = rsp.dsrlz_arr(cmdstr)
		if len(lst)==0:
			print("dsrlz_arr returned empty token")
			return ""
		for token in lst:
			print("find_cmd_arr token is:"+token)
		for cmd in cmds:
			if lst[0] == cmd.name:
				print("arr found cmd:"+cmd.name)
				return cmd.name 
		return ""

class cmds_srvr(commands):

	def __init__(self):
		pass

	def process_cmd_and_response(self,cmdstr,memdb):
		cmdname=self.find_cmd(cmdstr)
		print("after find_cmd cmdname:"+cmdname)
		if cmdname == "":
			cmdname=self.find_cmd_bulk(cmdstr)
			print("after find_cmd_bulk cmdname:"+cmdname)
			if cmdname == "":
				cmdname=self.find_cmd_arr(cmdstr)
				print("after find_cmd_arr cmdname:"+cmdname)
				if cmdname == "":
					print("cmd not found")
					return ""

		match cmdname:
			case "PING":
				print("PING cmd")
				return self.process_ping_and_response()

			case "GET":
				print("GET cmd")	
				return self.process_get_and_response(cmdstr,memdb)

			case "SET":
				print("SET cmd")
				return self.process_set_and_response(cmdstr,memdb)

			case "SETEX":
				print("SETEX cmd")
				return self.process_setex_and_response(cmdstr,memdb)

		return ""

	def process_ping_and_response(self):
		rsp = resp.resp()
		srlzd = rsp.srlz("PONG");
		print("process_ping_and_response:"+srlzd)
		return srlzd

	def process_set_and_response(self,cmdstr,memdb):
		rsp = resp.resp()
		lst = rsp.dsrlz_arr(cmdstr)
		for item in lst:
			print("item:"+item)
		memdb.insert(lst[1],lst[2])
		srlzd = rsp.srlz("OK")
		return srlzd

	def process_setex_and_response(self,cmdstr,memdb):
		rsp = resp.resp()
		lst = rsp.dsrlz_arr(cmdstr)
		for item in lst:
			print("setex item:"+item)
		memdb.insert_with_expire(lst[1],lst[3],lst[2])
		srlzd = rsp.srlz("OK")
		return srlzd

	def process_get_and_response(self,cmdstr,memdb):
		rsp = resp.resp()
		lst = rsp.dsrlz_arr(cmdstr)
		for item in lst:
			print("get item:"+item)
		getval = memdb.find(str(lst[1]))
		if getval == None:
			print("memdb.find returned None on key:"+lst[1])
			errmsg = "Key "+lst[1]+" not found"
			errrspns = rsp.srlz_err(errmsg)
			return errrspns
		rspns = rsp.srlz(getval)
		return rspns
