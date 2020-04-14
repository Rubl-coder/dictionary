from socket import *
import os
import pymysql
import traceback

s = socket(AF_INET,SOCK_STREAM)
s.setsockopt(SOL_SOCKRT,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen()

def handler(c):
	data = c.recv(1024)
	if data == 'C ':
		chashi()
	elif data == 'H ':
		hist()
	elif data == 'D':
		pass
	elif data == '##':
		pass
pid = os.fork()
if pid < 0:
	print("创建进程失败")
elif pid == 0:
	handler(c)
else:
	while True:
		try:
			c, addr = s.accept()
		except KeyboardInterrupt:
			print("服务端退出")
		except Exception:
			traceback.print_exc()
			continue



