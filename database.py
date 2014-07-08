import sqlite3

db=sqlite3.connect("Task.db")

with db:
	cur=db.cursor()
	cur.execute('DROP TABLE IF EXISTS labusers')
	cur.execute('DROP TABLE IF EXISTS demodetails')
	cur.execute('CREATE TABLE labusers(user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,role INTEGER NOT NULL DEFAULT 0)')
	cur.execute('CREATE TABLE  demodetails(demo_id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,demo_name TEXT NOT NULL,description TEXT NOT NULL,device_details TEXT NOT NULL,status INTEGER DEFAULT 0,duration TEXT NOT NULL)')
	cur.execute('INSERT INTO labusers (name,role) VALUES ("admin",1)') 
	cur.execute('INSERT INTO labusers (name,role) VALUES ("karthik",1)') 
	cur.execute('INSERT INTO demodetails(demo_name,user_id,demo_name,description,device_details,status,duration) VALUES ("admin",1,"new Demo","My Own Description","10.104.59.132 200",1,"123")') 

db.close()	         
