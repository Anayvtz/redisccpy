
from enum import Enum

DELIM = "\r\n"

class FirstCh(Enum):
	SIMPLE_STR = "+"
	INTEGER = ":"
	ERR = "-"
	BULK_STR = "$"
	ARR = "*"

class serialize:

	def __init__(self):
		pass

	def simple_str(cmd):
		first = FirstCh.SIMPLE_STR.value
		srlzd = first + cmd + DELIM
		return srlzd;

	def bulk_str(cmd,length):
		first = FirstCh.BULK_STR.value
		srlzd = first + str(length) + DELIM + cmd + DELIM
		return srlzd

	def err(msg):
		first = FirstCh.ERR.value
		srlzd = first + msg + DELIM
		return srlzd;

	def integer(num):
		first = FirstCh.INTEGER.value
		srlzd = first + str(num) + DELIM
		return srlzd;

	def arr(lstarr):
		first = FirstCh.ARR.value
		lstlen = len(lstarr)
		srlzd = first + str(lstlen) + DELIM
		for item in lstarr:
			srlzd += FirstCh.BULK_STR.value + str(len(item)) + DELIM + item + DELIM
		return srlzd
		
class deserialize:
	
	def __init__(self):
		pass
	
	def simple_str(str2dsrlz):
		first = str2dsrlz[0:1]
		if first != FirstCh.SIMPLE_STR.value:
			print("simple_str dsrlzd[0]:"+str(first))
			return ""
		dsrlzd = str2dsrlz[1:len(str2dsrlz)-len(DELIM)]
		return dsrlzd

	def bulk_str(str2dsrlzd):
		first = str2dsrlzd[0:1]
		if first != FirstCh.BULK_STR.value:
			print("bulk_str dsrlzd[0]:"+str(first))
			return ""
		indx = str2dsrlzd.find(DELIM)
		strlen = str2dsrlzd[1:indx]
		ilen = int(strlen)
		token = str2dsrlzd[indx+len(DELIM):indx+len(DELIM)+ilen]
		return token

	def err(str2dsrlzd):
		if str2dsrlzd[0] != FirstCh.ERR.value:
			return ""
		indx = str2dsrlzd.find(DELIM)
		token = str2dsrlzd[1:indx]
		return token

	def integer(str2dsrlzd):
		if str2dsrlzd[0] != FirstCh.INTEGER.value:
			return ""
		indx = str2dsrlzd.find(DELIM)
		token = str2dsrlzd[1:indx]
		return int(token)
		
	def arr(str2dsrlzd):
		first = str2dsrlzd[0:1]
		if first != FirstCh.ARR.value:
			print("arr dsrlzd[0]:"+ str(first) + " firstCh.arr:"+FirstCh.ARR.value)
			return ""
		indx = str2dsrlzd.find(DELIM)
		arrlen = str2dsrlzd[1:indx]
		print ("arr len:"+arrlen+":")
		ilen=int(arrlen)
		lst= []
		for ix in range(ilen):
			indx += len(DELIM) + 1
			endix = str2dsrlzd[indx:len(str2dsrlzd)].find(DELIM)
			print("indx:"+str(indx))
			print("endix:" + str(endix))
			endix += indx
			strlen = str2dsrlzd[indx:endix]
			print ("strlen:"+strlen)
			indx += len(strlen)+len(DELIM)
			ilen = int(strlen)
			token = str2dsrlzd[indx:indx+ilen]
			print("token:"+token)
			lst.append(token)
			indx += ilen
			#indx = str2dsrlzd[indx:len(str2dsrlzd)].find(DELIM)
			print("end of loop indx:"+str(indx))
		return lst
		

class resp:

	def __init__(self):
		pass

	def srlz(self,str2srlz):
		srlzd = serialize.simple_str(str2srlz)
		return srlzd

	def srlz_with_len(self,str2srlz,lenOfstr):
		srlzd = serialize.bulk_str(str2srlz,lenOfstr)
		return srlzd

	def srlz_err(self,errmsg):
		srlzd = serialize.err(errmsg)
		return srlzd

	def srlz_num(self,num):
		srlzd = serialize.integer(num)
		return srlzd

	def srlz_list(self,lst2srlz):
		srlzd = serialize.arr(lst2srlz)
		return srlzd

	def dsrlz_simple(self,str2dsrlz):
		token = deserialize.simple_str(str2dsrlz)
		return token

	def dsrlz_bulk(self,str2dsrlz):
		token = deserialize.bulk_str(str2dsrlz)
		return token

	def dsrlz_err(self,str2dsrlz):
		token = deserialize.err(str2dsrlz)
		return token

	def dsrlz_num(self,str2dsrlz):
		token = deserialize.integer(str2dsrlz)
		return token

	def dsrlz_arr(self,str2dsrlz):
		lst = deserialize.arr(str2dsrlz)
		return lst
