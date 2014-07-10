import sqlite3

db=sqlite3.connect("Task.db")

with db:
	cur=db.cursor()
	##  Creating fresh tables 
	cur.execute('DROP TABLE IF EXISTS demo_user_table')
	cur.execute('DROP TABLE IF EXISTS demodetails')
	cur.execute('DROP TABLE IF EXISTS lab_history')
	cur.execute('CREATE TABLE demo_user_table(userid TEXT NOT NULL,demoname TEXT,role INTEGER NOT NULL DEFAULT 0,demo_status INTEGER NOT NULL DEFAULT 0,duration TEXT)')
	cur.execute('CREATE TABLE  demodetails(demoid INTEGER,demoname TEXT NOT NULL,description TEXT NOT NULL,device_details TEXT NOT NULL,status  INTEGER NOT NULL DEFAULT 0)')

	# Here duration represents the time on when it was booked
	cur.execute('CREATE TABLE lab_history(userid TEXT NOT NULL,demoname TEXT, booked_time TEXT , status INTEGER)') 
	## Creating Fresh entries to the tables 

	cur.execute('INSERT INTO demo_user_table (userid,demoname,role,demo_status,duration) VALUES ("admin"," newDemo2",1,1,"100")') 
	cur.execute('INSERT INTO demo_user_table (userid,demoname,role,demo_status,duration) VALUES ("kartl","newDemo1",0,1,"200")') 
	cur.execute('INSERT INTO demo_user_table (userid,demoname,role,demo_status,duration) VALUES ("prakash","newDemo3 ",0,1,"100")') 
	cur.execute('INSERT INTO demodetails(demoid,demoname,description,device_details,status) VALUES (1,"newDemo1","My Own Description","10.104.59.132 200",1)') 
	cur.execute('INSERT INTO demodetails(demoid,demoname,description,device_details,status) VALUES (2,"newDemo2","My Own Description1","10.104.59.133 201",1)') 
	cur.execute('INSERT INTO demodetails(demoid,demoname,description,device_details,status) VALUES (3,"newDemo3","My Own Description2","10.104.59.134 202",1)') 
	cur.execute('INSERT INTO demodetails(demoid,demoname,description,device_details,status) VALUES (4,"newDemo4","My Own Description3","10.104.59.135 203",0)') 

	cur.execute('INSERT INTO lab_history(userid,demoname,booked_time,status) VALUES ("admin","newDemo2",CURRENT_DATE,1)')
	cur.execute('INSERT INTO lab_history(userid,demoname,booked_time,status) VALUES ("kartl","newDemo1",CURRENT_DATE,1)')
	cur.execute('INSERT INTO lab_history(userid,demoname,booked_time,status) VALUES ("prakash","newDemo3",CURRENT_DATE,1)') 

db.close()	         
