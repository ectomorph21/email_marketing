from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import create_sqlite_db
import sqlite_db_controller
from objects import *

with open('user_settings.json') as user_setting:
    data = json.load(user_setting)
    for user in data['user']:
        MIN_EMAIL = user['MIN_EMAIL']
        MAX_EMAIL = user['MAX_EMAIL']
        CALL_DATE = timedelta(days=user['EMAIL_INTERVAL'])
        DOMAIN = user['DOMAIN']
        SMTP_SERVER = user['SMTP_SERVER']
        PORT = user['PORT']
        EMAIL_LOGIN = user['EMAIL_LOGIN']
        EMAIL_PASSWORD = user['EMAIL_PASSWORD']
        FROM = user['FROM_HEADER']
        UNSUBSCRIBE = user['UNSUBSCRIBE_EMAIL']
        MAILING_LIST = user['MAILING_LIST']
        SIGNATURE = user['SIGNATURE']
        EMAIL_CHECK = user['BAD_DOMAIN']
        TARGETS = user['TARGET_CUSTOMER']
    for subject in data['subject']:
        SUBJE = subject['existing_customer']
        SUBJQ = subject['quoted_customer']
        SUBJP = subject['prospect']
        SUBJT = subject['target']
        SUBJH = subject['holiday']
    for email in data['email_template']:
        PROSPECT_TEMPLATE = email['PROSPECT']
        PREVIOUS_CUSTOMER_TEMPLATE = email['PREVIOUS_CUSTOMER']
        QUOTED_CUSTOMER_TEMPLATE = email['QUOTED_CUSTOMER']
        HOLIDAY_TEMPLATE = email['HOLIDAY_EMAIL']
    for footer in data['email_footer']:
        FOOTER = footer['FOOTER']
        
DATE = datetime.today()
LIMIT = [randint(MIN_EMAIL,MAX_EMAIL)]
SENT_LIST = []

class EmailMarketing:
    def __init__(self, root):
        root.title("Email Marketing")
        s = ttk.Style()
        s.theme_use('alt')
        s.configure('Caution.TButton',font='helvetica 12',foreground='red',padding=3)
        s.configure('Action.TButton',font='helvetica 12',foreground='green',padding=3)
        welcome_frame = ttk.Frame(root,width=500,height=300).grid(column=3,row=4)
        connect_db = ttk.Button(welcome_frame, text='Connect to db',style='Action.TButton',
        command=lambda:self.find_db_file()).grid(column=0,row=0,sticky=(N,S,E,W))
        create_db_button = ttk.Button(welcome_frame,text=f'Create SQLite DB',style='Caution.TButton',
        command=lambda:self.list_db()).grid(column=0,row=1,sticky=(N,S,E,W))
        view_prospects_button = ttk.Button(welcome_frame,text=f'View next prospects',style='Action.TButton',
        command=self.View_Prospects).grid(column=0,row=2,sticky=(N,S,E,W))
        export_db_csv = ttk.Button(welcome_frame,text=f'Export DB to CSV',style='Caution.TButton',
        command=lambda:sqlite_db_controller.export_db_csv(self.DB_CHECK.get())).grid(column=1,row=1,sticky=(N,S,E,W))
        send_prospects_button = ttk.Button(welcome_frame,text=f'Send email to prospects',style='Action.TButton',
        command=self.send_prospect_email).grid(column=1,row=2,sticky=(N,S,E,W))
        close_db = ttk.Button(welcome_frame, text='Close db',style='Action.TButton',command=self.close_db).grid(column=0,row=3,sticky=(E,W))
        
    def find_db_file(self):
        db_list = Tk()
        db_list.geometry("175x175")
        db_list.title('Select database')
        self.DB_CHECK = StringVar(db_list,1)
        for x in MAILING_LIST:
            rb = ttk.Radiobutton(db_list,text=f'{x} db',variable=self.DB_CHECK,value=f'{x}',
            command=self.select_db).pack()
        close_button = ttk.Button(db_list,text='select',command=lambda:db_list.destroy()).pack()
        
    def select_db(self):
        """Select database method tied to find_db_file method"""
        db_name = self.DB_CHECK.get()
        sqlite_db_controller.find_db_file(db_name)
        
    def create_db(self):
        db_name = self.DB_CREATE.get()
        csv_file = filedialog.askopenfilename(filetypes=[("CSV",'*.csv')])
        if csv_file != "":
            upload_csv = messagebox.askyesno(message='Are you sure you want to upload csv file and overwrite existing SQLite database or create new db if none exist?',icon='question',title='Upload')
            if upload_csv == True:
                create_sqlite_db.Create_Database(csv_file,db_name)
            else:
                pass
        else:
            messagebox.showerror(message='You must select a csv file to utilize this option.')
        
    def list_db(self):
        db_select = Tk()
        db_select.geometry("175x175")
        db_select.title('Select database')
        self.DB_CREATE = StringVar(db_select,1)
        for x in MAILING_LIST:
            rb = ttk.Radiobutton(db_select,text=f'{x} db',variable=self.DB_CREATE,value=f'{x}',
            command=self.create_db).pack()
        close_button = ttk.Button(db_select,text='select',command=lambda:db_select.destroy()).pack()
        
    def View_Prospects(self):
        """View next prospects to send emails based on LIMIT value"""
        self.customers = sqlite_db_controller.get_customers()
        if self.customers == None:
            pass
        else:
            count = 0
            result = "%20s%20s%30s%30s%30s\n" % ("Company", "First name", "Email","Days since contact","Notes")
            for c in self.customers:
                if c.previous_customer == '' and c.quoted == '' and c.last_contact != '' and c.notes == '':
                    row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                    time_delta = DATE - row_date
                    email_check = c.email_address.rsplit('@')
                    if time_delta >= CALL_DATE and count < LIMIT[0]:
                        count += 1
                        if email_check[1] in EMAIL_CHECK:
                            result += "%20s%20s%30s%30s%30s\n" % (c.company, c.first_name, c.email_address,c.industry,"***Use alternate email***")
                        else:
                            result += "%20s%20s%30s%30s%30s\n" % (c.company, c.first_name, c.email_address,f'{(time_delta.total_seconds()/86400):.0f} days',"")
                    elif count >= LIMIT[0]:
                        break
                    else:
                        continue
            c_display = Toplevel(root)
            c_display.title(f'Next {LIMIT[0]} prospects to email')
            c_display.geometry('850x600-75-75')
            display_customers = Text(c_display, width=850, height=600)
            display_customers.grid(column=0,row=0)
            display_customers.insert(1.0,result)
            display_customers['state'] = 'disabled'
            test_prompt = messagebox.askyesno(message='Would you like to send test emails?')
            if test_prompt == True:
                self.send_prospect_test()
            else:
                pass
            
    def send_prospect_test(self):
        """To send test emails before live emails"""
        count = 0
        for c in self.customers:
            if c.previous_customer == '' and c.quoted == '' and c.last_contact != '' and c.notes == '':
                row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                time_delta = DATE - row_date
                email_check = c.email_address.rsplit('@')
                if time_delta >= CALL_DATE and count < LIMIT[0]:
                    count += 1
                    if email_check[1] in EMAIL_CHECK:
                        pass
                    else:
                        name = c.first_name
                        customer = c.company
                        i_type = c.industry
                        prev_cus = c.previous_customer
                        quoted = c.quoted
                        website = c.website
                        address = c.email_address
                        subject = SUBJP[randint(0,len(SUBJP)-1)]
                        body = PROSPECT_TEMPLATE[randint(0,len(PROSPECT_TEMPLATE)-1)].replace("Company",customer)
                        footer = FOOTER[randint(0,len(FOOTER)-1)]
                        test_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK.get(),
                        prev_cus,name,body,SIGNATURE,footer)
                        test_email.send_test_email()
                elif count >= LIMIT[0]:
                    break
                else:
                    continue
        messagebox.showinfo(message='Test emails sent. Check terminal printout for format.')
        
    def send_prospect_email(self):
        """Send live emails to prospects"""
        self.customers = sqlite_db_controller.get_customers()
        if self.customers == None:
            pass
        else:
            count = 0
            for c in self.customers:
                if c.previous_customer == '' and c.quoted == '' and c.last_contact != '' and c.notes == '':
                    row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                    time_delta = DATE - row_date
                    email_check = c.email_address.rsplit('@')
                    if time_delta >= CALL_DATE and count < LIMIT[0]:
                        count += 1
                        if email_check[1] in EMAIL_CHECK:
                            pass
                        else:
                            name = c.first_name
                            customer = c.company
                            i_type = c.industry
                            prev_cus = c.previous_customer
                            quoted = c.quoted
                            website = c.website
                            address = c.email_address
                            subject = SUBJP[randint(0,len(SUBJP)-1)]
                            body = PROSPECT_TEMPLATE[randint(0,len(PROSPECT_TEMPLATE)-1)].replace("Company",customer)
                            footer = FOOTER[randint(0,len(FOOTER)-1)]
#                            live_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK.get(),
#                            prev_cus,name,body,SIGNATURE,footer)
#                            live_email.send_live_email(SMTP_SERVER,PORT,EMAIL_LOGIN,EMAIL_PASSWORD)
                            SENT_LIST.append(address)
                    elif count >= LIMIT[0]:
                        break
                    else:
                        continue
            LIMIT.clear()
            LIMIT.append(randint(MIN_EMAIL,MAX_EMAIL))
            sqlite_db_controller.update_last_contact(SENT_LIST)
            SENT_LIST.clear()
            messagebox.showinfo(message='Emails sent. Check mail server for delivery.')

    def close_db(self):
        """Close SQLite DB connection."""
        sqlite_db_controller.close()
        messagebox.showinfo(message='DB closed. You should close program.')

root = Tk()
EmailMarketing(root)
root.mainloop()
