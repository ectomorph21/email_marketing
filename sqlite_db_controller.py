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
            
"""    
def get_tasks():
    query = '''SELECT *
               FROM Task'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()
    tasks = []
    for row in results:
        tasks.append(make_tasks(row))
    return tasks
    
def make_tasks(row):
    return Task(row["taskID"], row["customer_name"], row["job_description"], row["price_charged"], row["estimated_hours"])
    
def get_completed_tasks():
    query = '''SELECT Task.taskID, customer_name, job_description, price_charged, estimated_hours
               FROM Task JOIN Assignment
                      ON Task.taskID = Assignment.taskID
               WHERE Assignment.completed = 1'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()
    if results == None:
        return None
    else:
        tasks = []
        for row in results:
            tasks.append(make_tasks(row))
        return tasks

def get_incomplete_tasks():
    query = '''SELECT Task.taskID, customer_name, job_description, price_charged, estimated_hours
               FROM Task JOIN Assignment
                      ON Task.taskID = Assignment.taskID
               WHERE Assignment.completed = 0'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()
    if results == None:
        return None
    else:
        tasks = []
        for row in results:
            tasks.append(make_tasks(row))
        return tasks
        
def get_employees():
    query = '''SELECT *
               FROM Employee'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()
    employees = []
    for row in results:
        employees.append(make_employees(row))
    return employees

def make_employees(row):
    return Employee(row["employeeID"], row["first_name"], row["last_name"], row["phone_number"], row["email_address"])
    
def get_employee_tasks(employeeID):
    query = '''SELECT Task.taskID, customer_name, job_description, price_charged, estimated_hours
               FROM Task JOIN Assignment
                      ON Task.taskID = Assignment.taskID
               WHERE Assignment.employeeID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (employeeID,))
        results = c.fetchall()
    if results == None:
        return None
    else:
        tasks = []
        for row in results:
            tasks.append(make_tasks(row))
        return tasks
        
def add_task(task):
    sql = '''INSERT INTO Task (taskID, customer_name, job_description, price_charged, estimated_hours) 
             VALUES (?, ?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (task[0], task[1], task[2], task[3], task[4]))
        conn.commit()
        
def add_assignment(assignment):
    sql = '''INSERT INTO Assignment (assignmentID, employeeID, taskID, completed) 
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (assignment[0], assignment[1], assignment[2], assignment[3]))
        conn.commit()
    
def get_assignments():
    query = '''SELECT *
               FROM Assignment'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()
    assignments = []
    for row in results:
        assignments.append(make_assignment(row))
    return assignments

def make_assignment(row):
    return Assignment(row["assignmentID"], row["employeeID"], row["taskID"], row["completed"])
    
def change_assignment(values):
    sql = '''UPDATE Assignment
             SET completed = ?
             WHERE AssignmentID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (values[0], values[1]))
        conn.commit()
"""
