
import resp
import srvr

print(dir(resp))
print(dir(srvr))

def main():
	print("hello World");
	rsp = resp.resp()
	srlzd = rsp.srlz("PING")
	print(srlzd)
	dsrlz = rsp.dsrlz_simple(srlzd)
	print(dsrlz)
	srlzd = rsp.srlz_with_len("PING",4)
	print(srlzd)
	dsrlz = rsp.dsrlz_bulk(srlzd)
	print(dsrlz)
	srlzd = rsp.srlz_err("Error Message")
	print(srlzd)
	dsrlz = rsp.dsrlz_err(srlzd)
	print(dsrlz)
	srlzd = rsp.srlz_num(5)
	print(srlzd)
	dsrlz_num = rsp.dsrlz_num(srlzd)
	print(dsrlz_num)
	srlzd = rsp.srlz_list(["Shame","on","you"])
	print(srlzd)
	dsrlz_lst = rsp.dsrlz_arr(srlzd)
	for item in dsrlz_lst:
		print(item)

	redissrvr = srvr.redis_srvr()
	redissrvr.activate()

if __name__ == "__main__":
	main()
