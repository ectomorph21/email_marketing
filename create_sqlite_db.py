import csv
import sqlite3

def Create_Database(csv_file,db_name):
    """Creates customer database"""
    conn = sqlite3.connect(f"{db_name}_customer_db.sqlite")
    c = conn.cursor()
    #drop table statements
    c.execute("""DROP TABLE IF EXISTS Customer""")
    #create table statements
    c.execute("""CREATE TABLE IF NOT EXISTS Customer(customerID INTEGER PRIMARY KEY AUTOINCREMENT,company TEXT,city TEXT,state TEXT,industry TEXT,previous_customer TEXT,quoted TEXT,website TEXT,first_name TEXT,last_name TEXT,email_address TEXT,last_contact TEXT,notes TEXT)""")
    #insert data into table statements
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        count = 1
        for row in reader:
            c.execute("INSERT INTO Customer VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(count,row['Company'],row['City'],row['State'],row['Industry'],row['Previous customer'],row['Quoted'],row['Website'],row['First name'],row['Last name'],row['Email'],row['Last contact'],row['Notes']))
            count += 1
    conn.commit()
    conn.close()
