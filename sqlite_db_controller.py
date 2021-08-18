import sys
import os
import sqlite3
import csv
from datetime import *
from tkinter import messagebox
from contextlib import closing
from objects import *
#from customer_objects import *
#from email_objects import *

conn = None
DATE = datetime.today()

def find_db_file(db_name):
    if sys.platform == "win32":
        target_file = f"{db_name}_customer_db.sqlite"
        file_check = os.path.exists(target_file)
    else:
        CWD = os.getcwd()
        target_file = CWD + f"/{db_name}_customer_db.sqlite"
        file_check = os.path.exists(target_file)
    if file_check == True:
        connect(target_file)
    else:
        messagebox.showerror(message=f'{target_file} does not exist')

def connect(db_name):
    global conn
    if not conn:
        if sys.platform == "win32":
            conn = sqlite3.connect(db_name)
            print('windows')
        else:
            conn = sqlite3.connect(db_name)
#            print('linux')
        conn.row_factory = sqlite3.Row
    print('db connected')

def close():
    if conn:
        conn.close()
    print('db closed')
        
def get_customers():
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        query = '''SELECT *
                   FROM Customer
                   ORDER BY last_contact'''
        with closing(conn.cursor()) as c:
            c.execute(query)
            results = c.fetchall()
        customers = []
        for row in results:
#            print(row.keys())
            customers.append(make_customers(row))
        return customers
    
def make_customers(row):
    return Customer(row["customerID"],row["company"],row["city"],row["state"],row["industry"],
    row["previous_customer"],row["quoted"],row["website"],row["first_name"],row["last_name"],
    row["email_address"],row["last_contact"],row["notes"])
    
def update_last_contact(SENT_LIST):
    date = DATE.strftime("%m/%d/%y")
    for e in SENT_LIST:
        sql = '''UPDATE Customer
                 SET last_contact = ?
                 WHERE email_address = ?'''
        with closing(conn.cursor()) as c:
            c.execute(sql,(date,e))
            conn.commit()

def export_db_csv(db_name):
    customers = get_customers()
    with open(f"{db_name}_db_dump.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company','City','State','Industry','Previous customer','Quoted','Website',
        'First name','Last name','Email','Last contact','Notes'])
        for c in customers:
            writer.writerow([c.company,c.city,c.state,c.industry,c.previous_customer,c.quoted,c.website,c.first_name,
            c.last_name,c.email_address,c.last_contact,c.notes])
            

