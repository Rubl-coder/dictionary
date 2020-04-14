from socket import *
import os
import time
import signal
import pymysql
import sys

#定义需要的全局变量
DICT_TEXT = './dit.txt'
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

#流程控制
def main():
	#创建数据库连接
	db = pymysql.connect('localhost','root','123','dict')

	#创建套接字
	s = socket()
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	s.bind(ADDR)
	s.listen(3)

	#忽略子进程信号，防止僵尸进程的产生
	signal.signal(signal.SIGCHLD,signal.SIG_IGN)

	while True:
		try:
			c,addr = s.accept()
			print("Connet from",addr)
		except KeyboardInterrupt:
			s.close()
			sys.exit("服务器退出")
		except Exception as e:
			print(e)
			continue

		#创建子进程
		pid = os.fork()
		if pid == 0:
			s.close()
			# print("子进程准备处理请求....")
			# sys.exit(1) # bad file descript 返回到S.accept但是S关闭了
			do_child(c,db)
		else:
			c.close()
			continue

def do_child(c,db):
	#循环接受客户端请求
	while True:
		data = c.recv(1024).decode()
		#print(data)
		print(c.getpeername(),":",data)
		if (not data) or data[0] == 'E':
			c.close()
			sys.exit(0)
		elif data[0] == 'R':
			do_register(c,db,data)
		elif data[0] == 'L':
			do_login(c,db,data)
		elif data[0] == 'Q':
			do_query(c,db,data)
		elif data[0] == 'H':
			do_hist(c,db,data)



def do_login(c,db,data):
	print("登陆操作")
	l = data.split(' ')
	name = l[1]
	password = l[2]
	cursor = db.cursor()
	sel = "select * from user where name='%s' and passwd='%s'"%(name,password)
	cursor.execute(sel)
	r = cursor.fetchone()
	if r == None:
		c.send(b'fail')
	else:
		c.send(b'ok')
	
def do_register(c,db,data):
	print("注册操作")
	l = data.split(' ')
	name = l[1]
	password = l[2]
	sql = 'select * from user where name="%s"'%name
	cur = db.cursor()
	cur.execute(sql)
	r = cur.fetchone()
	if r != None:
		c.send(b'EXISTS')
		return
	#用户不存在插入用户
	sql = 'insert into user(name,passwd) values("%s","%s")'%(name,password)
	try:
		cur.execute(sql)
		db.commit()
	except Exception as e:
		print(e)
		db.rollback()
		c.send(b'fail')
	else:
		c.send(b"ok")
		print("%s注册成功"%name)



	
def do_query(c,db,data):
	print("查询操作")
	l = data.split(' ')
	name = l[1]
	word = l[2]
	cursor = db.cursor()

	def insert_history():
		tm = time.ctime()
		sql = "insert into hist (name,word,time)\
		 values('%s','%s','%s')"%(name,word,tm)
		try:
			cursor.execute(sql)
			db.commit()
		except:
			db.rollback()


	#文本查询
	try:
		f = open(DICT_TEXT)
	except Exception as e:
		c.send(b'fail')
		print(e)
		f.close()
		return
	for line in f:
		tmp = line.split(' ')[0]
		if tmp > word:
			c.send(b'fail')
			f.close()
			return
		elif tmp == word:
			c.send(b'ok')
			time.sleep(0.1)
			c.send(line.encode())
			f.close()
			#如果在外部定义，平 调用则需要传参
			insert_history()#在内部调用作为do_query的局部变量可以使用name word
			return
	c.send(b'fail') #zzz的情况
	f.close()



def do_hist(c,db,data):
	print("历史记录")
	l = data.split(' ')
	name = l[1]
	cur = db.cursor()

	sql = "select * from hist where name='%s'" %name
	cur.execute(sql)
	#db.commit()
	r = cur.fetchall()
	#print(r)
	if not r:
		c.send(b'fail')
		return
	else:
		c.send(b'ok')
	for i in r:
		time.sleep(0.1)
		msg = "%s   %s   %s"%(i[1],i[2],i[3])
		#print(msg)
		c.send(msg.encode())
	time.sleep(0.1)
	c.send(b'##')

if __name__ == '__main__':
	main()


