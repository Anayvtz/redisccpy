
import resp
import srvr

print(dir(resp))
print(dir(srvr))

def main():

	redissrvr = srvr.redis_srvr()
	redissrvr.activate()

if __name__ == "__main__":
	main()
