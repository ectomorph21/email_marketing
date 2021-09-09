import csv
import sqlite3
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import pytz
from pytz import *
import settings
from settings import *

def Enter_User_Data():
    """Enter user data"""
    min_email = IntVar()
    max_email = IntVar()
    email_interval = IntVar()
    time_zone = StringVar()
    domain = StringVar()
    smtp_server = StringVar()
    port = IntVar()
    email_login = StringVar()
    email_password = StringVar()
    from_header = StringVar()
    unsubscribe_email = StringVar()
    mailing_list = StringVar()
    first_name = StringVar()
    last_name = StringVar()
    phone = StringVar()
    user_selection = [min_email,max_email,email_interval,time_zone,domain,smtp_server,port,email_login,email_password,
    from_header,unsubscribe_email,mailing_list,first_name,last_name,phone]
    user_entry = Toplevel()
    user_entry.title("Enter new user information")
    frame = ttk.Frame(user_entry)
    frame.grid(column=0,row=0)
    user_entry.grid_columnconfigure(0,weight=1)
    user_entry.grid_rowconfigure(0,weight=1)
    row_count = 1
    for key,value in settings.USER_DATA.items():
        if key == 'time_zone':
            label = ttk.Label(frame, text=f'{value}')
            label.grid(column=1,row=row_count)
            cbox = ttk.Combobox(frame,textvariable=user_selection.pop(0),values=settings.TIME_ZONES)
            cbox.grid(column=2,row=row_count)
        else:
            label = ttk.Label(frame, text=f'{value}')
            label.grid(column=1,row=row_count)
            entry = ttk.Entry(frame,justify='center',textvariable=user_selection.pop(0))
            entry.grid(column=2,row=row_count)
        row_count += 1
    button = ttk.Button(frame,text=f'Submit',
    command=lambda:[Create_User(min_email.get(),max_email.get(),email_interval.get(),time_zone.get(),
    domain.get(),smtp_server.get(),port.get(),email_login.get(),email_password.get(),
    from_header.get(),unsubscribe_email.get(),mailing_list.get(),first_name.get(),
    last_name.get(),phone.get()),user_entry.destroy()])
    button.grid(column=1,row=(row_count+1),columnspan=4)

def Create_User(*args):
    """Creates user and empty tables"""
    try:
        empty_field = False
        count = 0
        for x in args:
            if args[count] == '':
                empty_field = True
            count += 1
        if empty_field == False:
            confirm = messagebox.askyesno(message='Confirm user creation.',
            detail='This will create new SQLite database associated with first and last name and mailing list entered. Recommend you back up customer data with export csv function.',icon='warning')
            if confirm == True:
                conn = sqlite3.connect(f"{args[12]}_{args[13]}_{args[11]}_db.sqlite")
                c = conn.cursor()
                #drop tables
                c.execute("""DROP TABLE IF EXISTS User""")
                c.execute("""DROP TABLE IF EXISTS Customer""")
                c.execute("""DROP TABLE IF EXISTS Subject""")
                c.execute("""DROP TABLE IF EXISTS EmailBody""")
                c.execute("""DROP TABLE IF EXISTS Footer""")
                c.execute("""DROP TABLE IF EXISTS EmailCheck""")
                #create table statements
                c.execute("""CREATE TABLE IF NOT EXISTS User(
                             min_email INTEGER,max_email INTEGER,email_interval INTEGER,time_zone TEXT,
                             domain TEXT,smtp_server TEXT,port INTEGER,email_login TEXT,email_password TEXT,
                             from_header TEXT,unsubscribe_email TEXT,mailing_list TEXT PRIMARY KEY,first_name TEXT,
                             last_name TEXT,phone TEXT)""")
                c.execute("""CREATE TABLE IF NOT EXISTS Customer(customerID INTEGER PRIMARY KEY
                             REFERENCES User(mailing_list),company TEXT,city TEXT,state TEXT,status TEXT,
                             first_name TEXT,last_name TEXT,email_address TEXT,last_contact TEXT,notes TEXT)""")
                c.execute("""CREATE TABLE IF NOT EXISTS Subject(subjectID INTEGER PRIMARY KEY
                             REFERENCES User(mailing_list),subject_customer TEXT,subject TEXT)""")
                c.execute("""CREATE TABLE IF NOT EXISTS EmailBody(emailbodyID INTEGER PRIMARY KEY
                             REFERENCES User(mailing_list),email_body_customer TEXT,emailbody TEXT)""")
                c.execute("""CREATE TABLE IF NOT EXISTS Footer(footerID INTEGER PRIMARY KEY
                             REFERENCES User(mailing_list),headline TEXT,feature1 TEXT,feature2 TEXT,
                             feature3 TEXT,feature4 TEXT,feature5 TEXT,feature6 TEXT,feature7 TEXT,feature8 TEXT)""")
                c.execute("""CREATE TABLE IF NOT EXISTS EmailCheck(emailcheckID INTEGER PRIMARY KEY,
                             domain TEXT)""")
                #insert into User table
                c.execute("INSERT INTO User VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(args[0],args[1],args[2],
                args[3],args[4],args[5],args[6],args[7],args[8],args[9],args[10],args[11],args[12],args[13],
                args[14]))
                c.execute("""INSERT INTO EmailCheck VALUES(1,'hotmail.com')""")
                conn.commit()
                conn.close()
            else:
                messagebox.showinfo(message='Transaction cancelled',detail='No user created')
        else:
            messagebox.showwarning(message='All fields must be complete in order to proceed.',icon='warning')
    except Exception as e:
        messagebox.showerror(message='Error occurred.',
        detail='{e}')
        
