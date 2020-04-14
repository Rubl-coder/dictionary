import pymysql
import re

db = pymysql.connect('localhost','root','123','dict')
f = open('dit.txt')
cur = db.cursor()
for line in f:
	l = re.split(r'\s+',line)
	#print(l)
	word = l[0]
	#print(word)
	interpret = ' '.join(l[1:])
	#print(interpret)
	sql = 'insert into words (word,interpret) values("%s","%s")'%(word,interpret)
	try:
		cur.execute(sql)
		db.commit()
	except:
		db.rollback()

cur.close()
db.close()