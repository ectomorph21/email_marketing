import sys
import os
import sqlite3
import csv
from datetime import *
from tkinter import messagebox
from contextlib import closing
from objects import *

conn = None
DATE = datetime.today()

def find_db_file(db_name):
    """To locate and connect to existing database"""
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
    """Connect to DB"""
    global conn
    if not conn:
        if sys.platform == "win32":
            conn = sqlite3.connect(db_name)
        else:
            conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
    messagebox.showinfo(message=f'Connected to {db_name} DB.')

def close():
    """Close database connection"""
    if conn:
        conn.close()
        
def get_customers():
    """Query all customers in database"""
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
            customers.append(make_customers(row))
        return customers
    
def make_customers(row):
    """Make rows for get_customers function"""
    return Customer(row["customerID"],row["company"],row["city"],row["state"],row["industry"],
    row["previous_customer"],row["quoted"],row["website"],row["first_name"],row["last_name"],
    row["email_address"],row["last_contact"],row["notes"])
    
def update_last_contact(SENT_LIST):
    """Update last_contact field following emails being sent"""
    try:
        date = DATE.strftime("%m/%d/%y")
        for e in SENT_LIST:
            sql = '''UPDATE Customer
                     SET last_contact = ?
                     WHERE email_address = ?'''
            with closing(conn.cursor()) as c:
                c.execute(sql,(date,e))
                conn.commit()
    except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.')
            
def update_customer(x,y,z):
    """Update single customer row data based on customerID"""
    try:
        confirm_prompt = messagebox.askyesno(message=f'Are you sure you wish to make this change to customerID {z}?')
        if confirm_prompt == True:
            sql = f'''UPDATE Customer
                     SET {x} = ?
                     WHERE customerID = ?'''
            with closing(conn.cursor()) as c:
                c.execute(sql,(y,z))
                conn.commit()
        else:
            messagebox.showinfo(message='DB change cancelled.')
    except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.')
            
def delete_customer(customerID):
    """Delete customer by customerID"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            confirm_prompt = messagebox.askyesno(message=f'Are you sure you wish to delete customerID {customerID}?')
            if confirm_prompt == True:
                sql = '''DELETE FROM Customer
                         WHERE customerID = ?'''
                with closing(conn.cursor()) as c:
                    c.execute(sql, (customerID,))
                    conn.commit()
            else:
                messagebox.showinfo(message='DB change cancelled.')
        except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.')
            
def get_byCustomerID(customerID):
    """Get single customer by customerID"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        query = '''SELECT *
                   FROM Customer
                   WHERE customerID = ?'''
        with closing(conn.cursor()) as c:
            c.execute(query,(customerID,))
            result = c.fetchone()
        if result == None:
            return None
        else:
            return result

def export_db_csv(db_name):
    """Export database"""
    customers = get_customers()
    date = DATE.strftime("%m-%d-%y")
    with open(f"{db_name}_db_dump{date}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company','City','State','Industry','Previous customer','Quoted','Website',
        'First name','Last name','Email','Last contact','Notes'])
        for c in customers:
            writer.writerow([c.company,c.city,c.state,c.industry,c.previous_customer,c.quoted,c.website,c.first_name,
            c.last_name,c.email_address,c.last_contact,c.notes])
            
