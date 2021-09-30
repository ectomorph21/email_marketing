import sys
import os
import sqlite3
import csv
from datetime import *
from tkinter import filedialog, messagebox
import tkinter
from tkinter import *
from contextlib import closing
from objects import *
from load_settings import *
import load_settings
from settings import *
import settings

conn = None
DATE = datetime.today()

def locate_file():
    """Locate SQLite DB file"""
    sqlite_file = filedialog.askopenfilename(filetypes=[("SQLITE",'*.sqlite'),("DB",'*.db')])
    if sqlite_file == () or sqlite_file == "":
        messagebox.showinfo(message='No file selected',detail='Possible solution: create new user')
    else:
        connect(sqlite_file)

def upload_csv(csv_file):
    """Add customers from csv file"""
    try:
        if conn == None:
            messagebox.showerror(message='No db connection.',detail='Connect and retry.')
        else:
            with closing(conn.cursor()) as c:
                c.execute("""DROP TABLE IF EXISTS Customer""")
                c.execute("""CREATE TABLE IF NOT EXISTS Customer(customerID INTEGER PRIMARY KEY
                             REFERENCES User(mailing_list),company TEXT,city TEXT,state TEXT,status TEXT,
                             first_name TEXT,last_name TEXT,email_address TEXT,last_contact TEXT,notes TEXT)""")
                with open(csv_file, newline='') as f:
                    reader = csv.DictReader(f)
                    count = 1
                    for row in reader:
                        c.execute("INSERT INTO Customer VALUES(?,?,?,?,?,?,?,?,?,?)",(count,row['Company'],
                        row['City'],row['State'],row['Status'],row['First name'],row['Last name'],
                        row['Email'],row['Last contact'],row['Notes']))
                        count += 1
                    conn.commit()
    except Exception as e:
        messagebox.showerror(message='System error encountered',detail=f'{e}')

def connect(db_name):
    """Connect to DB"""
    try:
        global conn
        if not conn:
            if sys.platform == "win32":
                conn = sqlite3.connect(db_name)
#                print('windows')
            else:
                conn = sqlite3.connect(db_name)
#                print('linux')
            conn.row_factory = sqlite3.Row
        messagebox.showinfo(message='Connected to:',detail=f'{db_name}')
        load_settings.load_settings()
    except Exception as e:
        messagebox.showerror(message='System error encountered',detail=f'{e}')

def close():
    """Close database connection"""
    if conn:
        conn.close()
#    print('db closed')

def get_user():
    """Obtain user data"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        query = '''SELECT *
                   FROM User'''
        with closing(conn.cursor()) as c:
            c.execute(query)
            result = c.fetchone()
            if result == None:
                return None
            else:
                return result
            
def update_user(*args):
    """Update user data"""
    try:
        count = 0
        for k,v in settings.USER_DATA.items():
            if k == 'min_email' or k == 'max_email' or k == 'email_interval' or k == 'port':
                int_convert = int(args[count].strip('\n'))
                sql = f'''UPDATE User
                          SET {k} = ?
                          WHERE mailing_list = ?'''
                with closing(conn.cursor()) as c:
                    c.execute(sql,(int_convert,args[11].strip('\n')))
                    conn.commit()
            else:
               sql = f'''UPDATE User
                  SET {k} = ?
                  WHERE mailing_list = ?'''
               with closing(conn.cursor()) as c:
                   c.execute(sql,(args[count].strip('\n'),args[11].strip('\n')))
                   conn.commit()
            count += 1
        load_settings.clear_settings()        
        load_settings.load_settings()
    except Exception as e:
         messagebox.showerror(message='System error encountered',detail=f'{e}')
                
def get_customers():
    """Query all customers in database"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        query = '''SELECT *
                   FROM Customer
                   ORDER BY company'''
#                   ORDER BY last_contact'''
        with closing(conn.cursor()) as c:
            c.execute(query)
            results = c.fetchall()
        customers = []
        for row in results:
            customers.append(make_customers(row))
        return customers
        
def get_random_customers():
    """Query all customers in database in random order"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        order_var = settings.CUSTOMER_FIELDS[randint(0,len(settings.CUSTOMER_FIELDS)-1)]
        query = f'''SELECT *
                   FROM Customer
                   ORDER BY {order_var}'''
        with closing(conn.cursor()) as c:
            c.execute(query)
            results = c.fetchall()
        customers = []
        for row in results:
            customers.append(make_customers(row))
        return customers
    
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
        messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def create_customer():
    """Create new customer"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            customerID = IntVar()
            company = StringVar()
            city = StringVar()
            state = StringVar()
            status = StringVar()
            first_name = StringVar()
            last_name = StringVar()
            email_address = StringVar()
            last_contact = StringVar()
            notes = StringVar()
            user_selection = [customerID,company,city,state,first_name,last_name,email_address,last_contact,notes]
            user_entry = Toplevel()
            user_entry.title("Enter new customer information")
            frame = ttk.Frame(user_entry)
            frame.grid(column=0,row=0)
            user_entry.grid_columnconfigure(0,weight=1)
            user_entry.grid_rowconfigure(0,weight=1)
            row_count = 1
            for value in settings.CUSTOMER_FIELDS:
                if value == 'status':
                    label = ttk.Label(frame, text=f'{value}')
                    label.grid(column=1,row=row_count)
                    cbox = ttk.Combobox(frame,textvariable=status,values=settings.CUSTOMER_STATUS)
                    cbox.state(["readonly"])
                    cbox.grid(column=2,row=row_count)
                else:
                    label = ttk.Label(frame, text=f'{value}')
                    label.grid(column=1,row=row_count)
                    entry = ttk.Entry(frame,justify='center',textvariable=user_selection.pop(0))
                    entry.grid(column=2,row=row_count)
                row_count += 1
            button = ttk.Button(frame,text=f'Submit',
            command=lambda:[add_customer(customerID.get(),
            company.get(),city.get(),state.get(),status.get(),first_name.get(),
            last_name.get(),email_address.get(),last_contact.get(),notes.get()),user_entry.destroy()])
            button.grid(column=1,row=(row_count+1),columnspan=4)    
        except Exception as e:
            messagebox.showerror(message='Error encountered',detail=f'{e}')
    
def add_customer(*args):
    """Insert new customer into Customer table"""
    try:
        with closing(conn.cursor()) as c:
            c.execute("INSERT INTO Customer VALUES(?,?,?,?,?,?,?,?,?,?)",(args[0],args[1],
            args[2],args[3],args[4],args[5],args[6],
            args[7],args[8],args[9]))
            conn.commit()
    except Exception as e:
        messagebox.showerror(message='Error encountered',detail=f'{e}')
            
def update_customer(*args):
    """Update customer data based on customerID"""
    try:
        confirm_prompt = messagebox.askyesno(message=f'Are you sure you wish to make this change to customerID {args[0]}?')
        if confirm_prompt == True:
            customer_id = int(args[0].strip('\n'))
            count = 1
            for d in range(9):
                sql = f'''UPDATE Customer
                         SET {settings.CUSTOMER_FIELDS[count]} = ?
                         WHERE customerID = ?'''
                with closing(conn.cursor()) as c:
                    c.execute(sql,(args[count].strip('\n'),customer_id))
                    conn.commit()
                count += 1
        else:
            messagebox.showinfo(message='DB change cancelled.')
    except Exception as e:
        messagebox.showerror(message='System error encountered',detail=f'{e}')
            
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
                    c.execute(sql,(customerID,))
                    conn.commit()
            else:
                messagebox.showinfo(message='DB change cancelled.')
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def get_subjects():
    """Query all subjects in database"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            query = '''SELECT *
                   FROM Subject'''
#                   ORDER BY subjectID
            with closing(conn.cursor()) as c:
                c.execute(query)
                results = c.fetchall()
            subjects = []
            for row in results:
                subjects.append(make_subjects(row))
            return subjects
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def create_subject():
    """Create new subject"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            subjectID = IntVar()
            customer = StringVar()
            subject = StringVar()
            user_entry = Toplevel()
            user_entry.title("Enter new subject information")
            frame = ttk.Frame(user_entry)
            frame.grid(column=0,row=0)
            user_entry.grid_columnconfigure(0,weight=1)
            user_entry.grid_rowconfigure(0,weight=1)
            label = ttk.Label(frame,text='subjectID').grid()
            subject_id = ttk.Entry(frame,justify='center',textvariable=subjectID)
            subject_id.grid()
            label = ttk.Label(frame,text='customer').grid()
            cbox = ttk.Combobox(frame,textvariable=customer,values=settings.SUBJECT_CUSTOMER)
            cbox.state(["readonly"])
            cbox.grid()
            label = ttk.Label(frame,text='subject').grid()
            subject = Entry(frame,width=20)
            subject.grid()
            button = ttk.Button(frame,text=f'Submit',
            command=lambda:[add_subject(subjectID.get(),customer.get(),
            subject.get()),user_entry.destroy()])
            button.grid()
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def add_subject(*args):
    """Insert new subject into Subject table"""
    try:
        with closing(conn.cursor()) as c:
            c.execute("INSERT INTO Subject VALUES(?,?,?)",(args[0],args[1],args[2]))
            conn.commit()
        load_settings.clear_settings()
        load_settings.load_settings()
    except Exception as e:
        messagebox.showerror(message='Error encountered',detail=f'{e}')
        
def update_subject():
    """Update subject by subjectID"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            subjectID = IntVar()
            customer = StringVar()
            subject = StringVar()
            new_data = StringVar()
            user_entry = Toplevel()
            user_entry.title("Update subject information")
            frame = ttk.Frame(user_entry)
            frame.grid(column=0,row=0)
            user_entry.grid_columnconfigure(0,weight=1)
            user_entry.grid_rowconfigure(0,weight=1)
            label = ttk.Label(frame, text='subjectID').grid()
            subject_id = ttk.Entry(frame,justify='center',textvariable=subjectID)
            subject_id.grid()
            label = ttk.Label(frame,text='customer').grid()
            cbox = ttk.Combobox(frame,textvariable=customer,values=settings.SUBJECT_CUSTOMER)
            cbox.grid()
            label = ttk.Label(frame,text='subject').grid()
            subject = Entry(frame,width=20)
            subject.grid()
            button = ttk.Button(frame,text=f'Submit',
            command=lambda:[change_subject(subjectID.get(),customer.get(),subject.get())
            ,user_entry.destroy()])
            button.grid()
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def change_subject(*args):
    """SQL statement to update subject by subjectID"""
    try:
        count = 1
        for d in range(2):
            sql = f'''UPDATE Subject
                     SET {settings.SUBJECT_FIELDS[count]} = ?
                     WHERE subjectID = ?'''
            with closing(conn.cursor()) as c:
                c.execute(sql,(args[count],args[0]))
                conn.commit()
            count += 1
        load_settings.clear_settings()
        load_settings.load_settings()
    except Exception as e:
        messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def delete_subject(subject_id):
    """Delete subject by ID"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            sql = '''DELETE FROM Subject
                     WHERE subjectID = ?'''
            with closing(conn.cursor()) as c:
                c.execute(sql,(subject_id,))
                conn.commit()
            load_settings.clear_settings()
            load_settings.load_settings()
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def get_templates():
    """Query all email body templates"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            query = '''SELECT *
                   FROM EmailBody'''
#                   ORDER BY emailbodyID
            with closing(conn.cursor()) as c:
                c.execute(query)
                results = c.fetchall()
            templates = []
            for row in results:
                templates.append(make_templates(row))
            return templates
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def create_template():
    """Create new email body template"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            emailbodyID = IntVar()
            customer = StringVar()
            user_entry = Toplevel()
            user_entry.title("Enter new template information")
            frame = ttk.Frame(user_entry)
            frame.grid(column=0,row=0)
            user_entry.grid_columnconfigure(0,weight=1)
            user_entry.grid_rowconfigure(0,weight=1)
            label = ttk.Label(frame,text='EmailID').grid()
            entry = ttk.Entry(frame,justify='center',textvariable=emailbodyID)
            entry.grid()
            label = ttk.Label(frame,text='type').grid()
            cbox = ttk.Combobox(frame,textvariable=customer,values=settings.SUBJECT_CUSTOMER)
            cbox.state(["readonly"])
            cbox.grid()
            label = ttk.Label(frame,text='body')
            body = Text(frame,width=50,height=4)
            body.grid()
            button = ttk.Button(frame,text=f'Submit',
            command=lambda:[add_template(emailbodyID.get(),customer.get(),body.get(1.0,'end'))
            ,user_entry.destroy()])
            button.grid()
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def add_template(*args):
    """Insert new email body into EmailBody table"""
    try:
        with closing(conn.cursor()) as c:
            c.execute("INSERT INTO EmailBody VALUES(?,?,?)",(args[0],args[1],args[2].strip('\n')))
            conn.commit()
        load_settings.clear_settings()
        load_settings.load_settings()
    except Exception as e:
        messagebox.showerror(message='Error encountered',detail=f'{e}')
        
def update_template():
    """Update email body template by ID"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            emailbodyID = IntVar()
            customer = StringVar()
            user_entry = Toplevel()
            user_entry.title("Enter new template information")
            frame = ttk.Frame(user_entry)
            frame.grid(column=0,row=0)
            user_entry.grid_columnconfigure(0,weight=1)
            user_entry.grid_rowconfigure(0,weight=1)
            label = ttk.Label(frame,text='EmailID').grid()
            entry = ttk.Entry(frame,justify='center',textvariable=emailbodyID)
            entry.grid()
            label = ttk.Label(frame,text='type').grid()
            cbox = ttk.Combobox(frame,textvariable=customer,values=settings.SUBJECT_CUSTOMER)
            cbox.grid()
            label = ttk.Label(frame,text='body')
            body = Text(frame,width=75,height=10)
            body.grid()
            button = ttk.Button(frame,text=f'Submit',
            command=lambda:[change_template(emailbodyID.get(),customer.get(),body.get(1.0,'end'))
            ,user_entry.destroy()])
            button.grid()
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def change_template(*args):
    """SQL statement to update email body template by ID"""
    try:
        count = 1
        for d in range(2):
            sql = f'''UPDATE EmailBody
                     SET {settings.EMAILBODY_FIELDS[count]} = ?
                     WHERE emailbodyID = ?'''
            with closing(conn.cursor()) as c:
                c.execute(sql,(args[count].strip('\n'),args[0]))
                conn.commit()
            count += 1
        load_settings.clear_settings()
        load_settings.load_settings()
    except Exception as e:
        messagebox.showerror(message='System error encountered',detail=f'{e}')
    
def delete_template(emailbody_id):
    """Delete email template body by ID"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            sql = '''DELETE FROM EmailBody
                     WHERE emailbodyID = ?'''
            with closing(conn.cursor()) as c:
                c.execute(sql,(emailbody_id,))
                conn.commit()
            load_settings.clear_settings()
            load_settings.load_settings()
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def get_footers():
    """Query all email footer templates"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            query = '''SELECT *
                   FROM Footer'''
            with closing(conn.cursor()) as c:
                c.execute(query)
                results = c.fetchall()
            footers = []
            for row in results:
                footers.append(make_footers(row))
            return footers
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def create_footer():
    """Create new footer"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            footerID = IntVar()
            headline = StringVar()
            feature1 = StringVar()
            feature2 = StringVar()
            feature3 = StringVar()
            feature4 = StringVar()
            feature5 = StringVar()
            feature6 = StringVar()
            feature7 = StringVar()
            feature8 = StringVar()
            user_selection = [footerID,headline,feature1,feature2,feature3,feature4,feature5,feature6,
            feature7,feature8]
            user_entry = Toplevel()
            user_entry.title("Enter new footer information")
            frame = ttk.Frame(user_entry)
            frame.grid(column=0,row=0)
            user_entry.grid_columnconfigure(0,weight=1)
            user_entry.grid_rowconfigure(0,weight=1)
            row_count = 1
            for value in settings.FOOTER_FIELDS:
                label = ttk.Label(frame, text=f'{value}')
                label.grid(column=1,row=row_count)
                entry = ttk.Entry(frame,justify='center',textvariable=user_selection.pop(0))
                entry.grid(column=2,row=row_count)
                row_count += 1
            button = ttk.Button(frame,text=f'Submit',
            command=lambda:[add_footer(footerID.get(),
            headline.get(),feature1.get(),feature2.get(),feature3.get(),
            feature4.get(),feature5.get(),feature6.get(),feature7.get(),
            feature8.get()),user_entry.destroy()])
            button.grid(column=1,row=(row_count+1),columnspan=4)
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def add_footer(*args):
    """Insert new footer into Footer table"""
    try:
        with closing(conn.cursor()) as c:
            c.execute("INSERT INTO Footer VALUES(?,?,?,?,?,?,?,?,?,?)",(args[0],args[1],args[2],args[3],args[4],
            args[5],args[6],args[7],args[8],args[9]))
            conn.commit()
        load_settings.clear_settings()
        load_settings.load_settings()
    except Exception as e:
        messagebox.showerror(message='Error encountered',detail=f'{e}')
        
def update_footer(*args):
    """Update single footer column data based on footerID"""
    try:
        footer_id = int(args[0].strip('\n'))
        count = 1
        for d in range(9):
            sql = f'''UPDATE Footer
                      SET {settings.FOOTER_FIELDS[count]} = ?
                      WHERE footerID = ?'''
            with closing(conn.cursor()) as c:
                c.execute(sql,(args[count].strip('\n'),footer_id))
                conn.commit()
            count += 1
        load_settings.clear_settings()
        load_settings.load_settings()
    except Exception as e:
        messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def delete_footer(footer_id):
    """Delete footer by ID"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            sql = '''DELETE FROM Footer
                     WHERE footerID = ?'''
            with closing(conn.cursor()) as c:
                c.execute(sql,(footer_id,))
                conn.commit()
            load_settings.clear_settings()
            load_settings.load_settings()
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def get_bad_domains():
    """Query all bad domains"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            query = '''SELECT *
                   FROM EmailCheck'''
            with closing(conn.cursor()) as c:
                c.execute(query)
                results = c.fetchall()
            bad_domains = []
            for row in results:
                bad_domains.append(make_bad_domains(row))
            return bad_domains
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def add_bad_domain():
    """Add new bad domain into EmailCheck table"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            emailcheckID = IntVar()
            domain = StringVar()
            user_entry = Toplevel()
            user_entry.title("Enter new bad domain")
            user_entry.geometry('300x300')
            frame = ttk.Frame(user_entry, width=300, height=300)
            frame.grid(column=0,row=0)
            user_entry.grid_columnconfigure(0,weight=1)
            user_entry.grid_rowconfigure(0,weight=1)
            label = ttk.Label(frame, text='enter emailcheckID').grid()
            entry = ttk.Entry(frame,justify='center',textvariable=emailcheckID).grid()
            label = ttk.Label(frame, text='enter bad domain').grid()
            entry = ttk.Entry(frame,justify='center',textvariable=domain).grid()
            button = ttk.Button(frame,text=f'Submit',
            command=lambda:[insert_bad_domain(emailcheckID.get(),domain.get()),user_entry.destroy()])
            button.grid()
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
def insert_bad_domain(*args):
    """SQL to insert new bad domain"""
    try:
        with closing(conn.cursor()) as c:
            c.execute("INSERT INTO EmailCheck VALUES(?,?)",(args[0],args[1]))
            conn.commit()
        load_settings.clear_settings()
        load_settings.load_settings()
    except Exception as e:
        messagebox.showerror(message='Error encountered',detail=f'{e}')
        
def delete_emailcheck(emailcheck_id):
    """Delete bad domain by ID"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            sql = '''DELETE FROM EmailCheck
                     WHERE emailcheckID = ?'''
            with closing(conn.cursor()) as c:
                c.execute(sql,(emailcheck_id,))
                conn.commit()
            load_settings.clear_settings()
            load_settings.load_settings()
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
            
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
            
def get_byFooterID(footerID):
    """Get single footer by ID"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        query = '''SELECT *
                   FROM Footer
                   WHERE footerID = ?'''
        with closing(conn.cursor()) as c:
            c.execute(query,(footerID,))
            result = c.fetchone()
        if result == None:
            return None
        else:
            return result

def make_customers(row):
    """Make rows for get_customers function"""
    return Customer(row["customerID"],row["company"],row["city"],row["state"],row["status"],row["first_name"],
    row["last_name"],row["email_address"],row["last_contact"],row["notes"])   
    
def make_subjects(row):
    """Make rows for get_subjects function"""
    return Subject(row["subjectID"],row["subject_customer"],row["subject"])
    
def make_templates(row):
    """Make rows for get_templates function"""
    return EmailBody(row["emailbodyID"],row["email_body_customer"],row["emailbody"])
    
def make_footers(row):
    """Make rows for get_footers function"""
    return Footer(row["footerID"],row["headline"],row["feature1"],row["feature2"],row["feature3"],
    row["feature4"],row["feature5"],row["feature6"],row["feature7"],row["feature8"])
    
def make_bad_domains(row):
    """Make rows for get_bad_domains function"""
    return EmailCheck(row["emailcheckID"],row["domain"])
    
def export_csv():
    """Export customer table from database"""
    if conn == None:
        messagebox.showerror(message='No db connection. Connect and retry.')
    else:
        try:
            customers = get_customers()
            date = DATE.strftime("%m-%d-%y")
            save_as = filedialog.asksaveasfilename(defaultextension="csv",filetypes=[("CSV",'*.csv')],
            initialfile=f"{settings.MAILING_LIST}_customer_table_dump{date}.csv")
            with open(save_as,'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Company','City','State','Status','First name','Last name','Email','Last contact','Notes'])
                for c in customers:
                    writer.writerow([c.company,c.city,c.state,c.status,c.first_name,c.last_name,
                    c.email_address,c.last_contact,c.notes])
        except Exception as e:
            messagebox.showerror(message='System error encountered',detail=f'{e}')
