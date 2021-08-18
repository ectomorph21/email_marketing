import csv
import sqlite3

def Create_Database(csv_file,db_name):
    conn = sqlite3.connect(f"{db_name}_customer_db.sqlite")
    c = conn.cursor()
    #drop table statements
    c.execute("""DROP TABLE IF EXISTS Customer""")
#    c.execute("""DROP TABLE IF EXISTS User_Setting""")
#    c.execute("""DROP TABLE IF EXISTS Email_Template""")
    #create table statements
#    c.execute("""CREATE TABLE IF NOT EXISTS User_Setting(userID INTEGER PRIMARY KEY AUTOINCREMENT,first_name TEXT ,last_name TEXT,organization TEXT,email_address TEXT,email_login TEXT, email_password TEXT, smtp_server TEXT, domain TEXT, email_interval INTEGER, email_limit INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS Customer(customerID INTEGER PRIMARY KEY AUTOINCREMENT,company TEXT,city TEXT,state TEXT,industry TEXT,previous_customer TEXT,quoted TEXT,website TEXT,first_name TEXT,last_name TEXT,email_address TEXT,last_contact TEXT,notes TEXT)""")
#    c.execute("""CREATE TABLE IF NOT EXISTS Email_Template(templateID INTEGER PRIMARY KEY AUTOINCREMENT,subject TEXT ,unsubscribe_list TEXT,body BLOB)""")
    #insert data into table statements
#    c.execute("""INSERT INTO User_Setting VALUES(1,'John','Doe','John Doe Inc.','john@johndoeinc.com','login','password','mail.johndoeinc.com','johndoeinc.com',90,10)""")
#    c.execute("""INSERT INTO Email_Template VALUES(1,'Test Email','Email list','This is only an email template. Will have to test it.')""")
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        count = 1
        for row in reader:
            c.execute("INSERT INTO Customer VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(count,row['Company'],row['City'],row['State'],row['Industry'],row['Previous customer'],row['Quoted'],row['Website'],row['First name'],row['Last name'],row['Email'],row['Last contact'],row['Notes']))
            count += 1
    conn.commit()
    conn.close()

