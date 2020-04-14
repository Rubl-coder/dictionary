from socket import *
import sys
import getpass

#创建网络连接
def main():
	if len(sys.argv) < 3:
		print("argv is erro")
		return
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	ADDR = (HOST,PORT)
	s = socket()
	try:
		s.connect((HOST,PORT))
	except Exception as e:
		print(e)
		return
	while True:
		print('''
			==============Welcome================
			----- 1.注册    2.登陆        3.退出---
			''')
		try:
			cmd = int(input("输入选项>>"))
		except Exception as e:
			print("命令错误！")
			continue
		if cmd not in [1,2,3]:
			print("请输入正确的命令！")
			sys.stdin.flush()#清除缓冲区
			continue
		elif cmd == 1:
			r = do_register(s)
			if r == 0:
				print("注册成功")
			elif r == 1:
				print("用户存在")
			else:
				print("注册失败")
		elif cmd == 2:
			name = do_login(s)
			if name:
				print("登陆成功")
				login(s,name)
			else:
				print("密码或用户名错误，请检查是否正确")
		elif cmd == 3:
			s.send(b'E')
			sys.exit("谢谢使用")

def do_register(s):
	while True:
		name = input("User:")
		password = getpass.getpass()
		password1 = getpass.getpass("Again:")

		if (' ' in name) or (' ' in password):
			print("用户名或者密码不允许有空格")
			continue
		if password != password1:
			print("二次输入密码不一致，重新输入")
			continue
		msg = 'R {} {}'.format(name,password)
		#发送消息
		s.send(msg.encode())
		#等待回复
		#print("000000000")
		data = s.recv(128).decode()
		#print("---------")
		if data == 'ok':
			return 0
		elif data == 'EXISTS':
			return 1
		else:
			return 2
def do_login(s):
	name = input("user:")
	password = getpass.getpass()
	msg = 'L {} {}'.format(name,password)
	s.send(msg.encode())

	#等待回复消息
	data = s.recv(124).decode()
	if data == 'ok':
		return name
	else:
		return 
def login(s,name):
	while True:
		print('''
			==========查询界面========
			1.查询      2.历史记录   3.退出
			''')
		try:
			cmd = int(input("输入选项>>"))
		except Exception as e:
			print("命令错误！")
			continue
		if cmd not in [1,2,3]:
			print("请输入正确的命令！")
			sys.stdin.flush()#清除缓冲区
			continue
		elif cmd == 1:
			do_query(s,name)
		elif cmd == 2:
			do_hist(s,name)
		elif cmd == 3:
			return

def do_query(s,name):
	while True:
		word = input("请输入你要查询的单词:")
		if word == '#':
			#print("-----")
			break
			#print("111111")
		meg = 'Q {} {}'.format(name,word)
		s.send(meg.encode())
		data = s.recv(124).decode()
		if data == 'ok':
			data = s.recv(1024).decode()
			print(data)
		else:
			print("没有此单词")



def do_hist(s,name):
	msg = 'H {}'.format(name)
	s.send(msg.encode())
	data = s.recv(124).decode()
	print(data)
	if data == 'ok':
		while True:
			data = s.recv(1024).decode()
			if data == '##':
				break
			print(data)
	else:
		print("没有历史记录")


if __name__ == '__main__':
	main()