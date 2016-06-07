#coding:utf-8
import sqlite3 , time , urllib2
from flask import Request 
from app_package import app
#import app_package	
#数据库保存access_token
#每次 检测超过7100秒后 插入数据库 , 读取时选择倒序取一个...
def create_db():
	conn = sqlite3.connect('sqlite.db')
	sql_create_table =  '''
create table if not exists access_token (id INTEGER PRIMARY KEY AUTOINCREMENT , at text , time int(20));
	'''
	conn.execute(sql_create_table)
	conn.commit()
	return conn
def insert_at():
	conn = create_db()
	sql_insert =  '''
insert into access_token(at , time) values(? , ?);
	'''
	ti = time.time()
	conn.execute(sql_insert , (getat() , ti))
	conn.commit()
	return conn


def select_at():
	conn = create_db()
	sql_select = {"get_at":"select at from access_token order by id desc limit 1  ;" , 
			    "get_time":"select time from access_token order by id desc  limit 1 ;"}
	time_in_db = conn.execute(sql_select.get('get_time'))
	tt = 0
	for row in time_in_db:
		tt = int(row[0])
	now = time.time()
	if now-tt>7100:
		insert_at()
		return select_at()
	else:
		old_at = conn.execute(sql_select.get('get_at'))
		for row in old_at:
			return row

# 获取access_token
def getat():
	appid = app.config['APPID']
	secret = app.config['SECRET']
	url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(appid , secret)
	req = urllib2.Request(url)
	res = eval(urllib2.urlopen(req).read())
	access_token = res['access_token']
	return access_token

if __name__ == '__main__':
	print select_at()