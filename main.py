from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import create_sqlite_db
import sqlite_db_controller
from objects import *
import alt_main

with open('user_settings.json') as user_setting:
    """Import settings and templates from json file"""
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
        SIGNATURE = user['SIGNATURE1']
        EMAIL_CHECK = user['BAD_DOMAINS']
        TARGETS = user['TARGET_CUSTOMERS']
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
        """Main tkinter window"""
        self.DB_CHECK = None
        self.GITHUB_PAGE = 'https://github.com/ectomorph21/email_marketing'
        self.WEBSITE = 'https://www.randmssolutions.com/'
        root.title("Email Marketing")
        welcome_frame = ttk.Frame(root)
        welcome_frame.grid(column=0,row=0)
        s = ttk.Style()
        s.theme_use('alt')
        s.configure('Caution.TButton',font='helvetica 12',foreground='red',padding=3)
        s.configure('Action.TButton',font='helvetica 12',foreground='green',padding=3)
        welcome_frame.grid(column=0,row=0)
        #db and about buttons
        connect_db = ttk.Button(welcome_frame, text='Connect to DB',
        command=lambda:self.find_db_file()).grid(column=1,row=1,sticky=(N,S,E,W))
        create_db_button = ttk.Button(welcome_frame,text=f'Create SQLite DB',
        command=lambda:self.list_db()).grid(column=2,row=1,sticky=(N,S,E,W))
        export_db_csv = ttk.Button(welcome_frame,text=f'Export DB to CSV',
        command=self.export_db).grid(column=3,row=1,sticky=(N,S,E,W))
        close_db = ttk.Button(welcome_frame, text='Close DB',command=self.close_db).grid(column=4,row=1,sticky=(N,S,E,W))
        create_button = ttk.Button(welcome_frame,text='Create customer',
        command=lambda:messagebox.showinfo(message='Function in development')).grid(column=1,
        row=2,sticky=(N,S,E,W))
        change_button = ttk.Button(welcome_frame,text='Update customer',
        command=self.Update_Customer).grid(column=2,row=2,sticky=(N,S,E,W))
        delete_button = ttk.Button(welcome_frame,text='Delete customer',
        command=self.delete_customer).grid(column=3,
        row=2,sticky=(N,S,E,W))
        about_button = ttk.Button(welcome_frame,text='About',
        command=self.About_Software).grid(column=4,row=2,sticky=(N,S,E,W))
        #view and send buttons
        view_all_button = ttk.Button(welcome_frame,text='View all customers',style='Action.TButton',
        command=self.View_All).grid(column=1,row=3,columnspan=4,sticky=(N,S,E,W))
        view_prospects_button = ttk.Button(welcome_frame,text='View next prospects',style='Action.TButton',
        command=self.View_Prospects).grid(column=1,row=4,columnspan=2,sticky=(N,S,E,W))
        send_prospects_button = ttk.Button(welcome_frame,text='Send email to prospects',style='Caution.TButton',
        command=self.send_prospect_email).grid(column=3,row=4,columnspan=2,sticky=(N,S,E,W))
        view_quoted_button = ttk.Button(welcome_frame,text='View next quoted',style='Action.TButton',
        command=self.View_Quoted).grid(column=1,row=5,columnspan=2,sticky=(N,S,E,W))
        send_quoted_button = ttk.Button(welcome_frame,text='Send email to quoted',style='Caution.TButton',
        command=self.send_quoted_email).grid(column=3,row=5,columnspan=2,sticky=(N,S,E,W))
        view_clients_button = ttk.Button(welcome_frame,text='View next clients',style='Action.TButton',
        command=self.View_Clients).grid(column=1,row=6,columnspan=2,sticky=(N,S,E,W))
        send_clients_button = ttk.Button(welcome_frame,text='Send email to clients',style='Caution.TButton',
        command=self.send_client_email).grid(column=3,row=6,columnspan=2,sticky=(N,S,E,W))
        holiday_test_button = ttk.Button(welcome_frame,text='Send test holiday email',style='Action.TButton',
        command=self.send_holiday_test).grid(column=1,row=7,columnspan=2,sticky=(N,S,E,W))
        send_holiday_button = ttk.Button(welcome_frame,text='Send holiday email',style='Caution.TButton',
        command=self.send_holiday_email).grid(column=3,row=7,columnspan=2,sticky=(N,S,E,W))
        root.protocol("WM_DELETE_WINDOW", self.close_db)

    def About_Software(self):
        """Software information with Github and website links"""
        messagebox.showinfo(title="About",message=f"Thank you for using this software.",detail=f"More information can be found at the following links:\n\n{self.GITHUB_PAGE}\n\n{self.WEBSITE}")
    
    def find_db_file(self):
        """method to select and connect to existing DB"""
        db_list = Tk()
        db_list.geometry("175x175")
        db_list.title('Select database')
        self.DB_CHECK = StringVar(db_list)
        for x in MAILING_LIST:
            rb = ttk.Radiobutton(db_list,text=f'{x} db',variable=self.DB_CHECK,value=f'{x}',
            command=self.select_db).pack()
        close_button = ttk.Button(db_list,text='select',command=lambda:db_list.destroy()).pack()
        
    def select_db(self):
        """Select database method tied to find_db_file method"""
        db_name = self.DB_CHECK.get()
        if db_name == MAILING_LIST[0]:
            sqlite_db_controller.find_db_file(db_name)
        else:
            alt_main.Alt_Email(db_name)
            root.iconify()

    def list_db(self):
        """Method for selection of DB to create or overwrite"""
        db_select = Tk()
        db_select.geometry("175x175")
        db_select.title('Select database')
        self.DB_CREATE = StringVar(db_select)
        for x in MAILING_LIST:
            rb = ttk.Radiobutton(db_select,text=f'{x} db',variable=self.DB_CREATE,value=f'{x}',
            command=self.create_db).pack()
        close_button = ttk.Button(db_select,text='select',command=lambda:db_select.destroy()).pack()
        
    def create_db(self):
        """Method to create new or overwrite existing DB. Tied to list_db"""
        db_name = self.DB_CREATE.get()
        csv_file = filedialog.askopenfilename(filetypes=[("CSV",'*.csv')])
        if csv_file == () or csv_file == "":
            messagebox.showerror(message='You must select a csv file to utilize this option.')
        else:
            upload_csv = messagebox.askyesno(message='Are you sure you want to upload csv file and overwrite existing SQLite database or create new db if none exist?',icon='question',title='Upload')
            if upload_csv == True:
                create_sqlite_db.Create_Database(csv_file,db_name)
            else:
                messagebox.showinfo(message='Operation cancelled. No DB created.')
        
    def export_db(self):
        """Method to export DB to csv file"""
        if self.DB_CHECK == None:
            messagebox.showerror(message="You must connect to an existing DB.'")
        else:
            sqlite_db_controller.export_db_csv(self.DB_CHECK.get())
            
    def close_db(self):
        """Close SQLite DB connection."""
        sqlite_db_controller.close()
        messagebox.showinfo(message='DB closed. Program will be closed.')
        root.destroy()
        
    def Update_Customer(self):
        """Update customer by ID"""
        self.CUSTOMER_ID = IntVar()
        user_entry = Toplevel()
        user_entry.title('Enter customerID')
        label = ttk.Label(user_entry, text='Enter customerID:').pack()
        entry = ttk.Entry(user_entry,justify='center',width=5,textvariable=self.CUSTOMER_ID).pack()
        button = ttk.Button(user_entry,text=f'Submit',command=lambda:[self.print_customer(),
        user_entry.destroy()]).pack()
        
    def print_customer(self):
        """This is where single customer information will be displayed for updates"""
        customer = sqlite_db_controller.get_byCustomerID(self.CUSTOMER_ID.get())
        if customer == None:
            messagebox.showerror(message='no customer with that ID exist in DB')
        else:
            self.NEW_DATA = StringVar()
            data = customer.keys()
            count = 0
            result = ""
            for c in customer:
                result += f'{data[count]}: {c}\n'
                count += 1
            c_info = Toplevel()
            c_info.title(f'Customer# {self.CUSTOMER_ID.get()} info')
            c_info.geometry('500x500')
            display_customer = Text(c_info,width=500,height=500)
            ys = ttk.Scrollbar(c_info,orient='vertical',command=display_customer.yview)
            display_customer['yscrollcommand'] = ys.set
            display_customer.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_customer.insert(1.0,result)
            c_info.grid_columnconfigure(0, weight = 1)
            c_info.grid_rowconfigure(0, weight = 1)
            display_customer['state'] = 'disabled'
            label = ttk.Label(c_info, text='Select row you want to update:').grid()
            choicesvar = StringVar(value=data)
            lbox = Listbox(c_info,listvariable=choicesvar,selectmode="single")
            lbox.grid()
            label = ttk.Label(c_info, text='Enter new data:').grid()
            entry = ttk.Entry(c_info,justify='center',textvariable=self.NEW_DATA).grid()
            button = ttk.Button(c_info,text=f'Submit',
            command=lambda:[sqlite_db_controller.update_customer(lbox.get(lbox.curselection()),
            self.NEW_DATA.get(),self.CUSTOMER_ID.get()),c_info.destroy()]).grid()
            
    def delete_customer(self):
        """Where customer will be selected for deletion by customerID"""
        self.CUSTOMER_ID = IntVar()
        user_entry = Toplevel()
        user_entry.title('Enter customerID')
        label = ttk.Label(user_entry, text='Enter customerID:').pack()
        entry = ttk.Entry(user_entry,justify='center',width=5,textvariable=self.CUSTOMER_ID).pack()
        button = ttk.Button(user_entry,text=f'Submit',command=lambda:[sqlite_db_controller.delete_customer(self.CUSTOMER_ID.get()),user_entry.destroy()]).pack()
        
    def View_All(self):
        """View all customers in DB"""
        self.customers = sqlite_db_controller.get_customers()
        if self.customers == None:
            pass
        else:
            result = "%5s%40s%20s%30s%15s%30s\n" % ("ID","Company","Name","Email","Last contact","Notes")
            for c in self.customers:
                result += "%5s%40s%20s%30s%15s%30s\n" % (c.customerID,c.company,c.first_name,c.email_address,
                c.last_contact,c.notes)
            c_display = Toplevel()
            c_display.title('All customers')
            c_display.geometry('1300x700')
            display_customers = Text(c_display,width=1300,height=700)
            ys = ttk.Scrollbar(c_display,orient='vertical',command=display_customers.yview)
            display_customers['yscrollcommand'] = ys.set
            display_customers.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_customers.insert(1.0,result)
            c_display.grid_columnconfigure(0, weight = 1)
            c_display.grid_rowconfigure(0, weight = 1)
            display_customers['state'] = 'disabled'
        
    def View_Prospects(self):
        """View next prospects to send emails based on LIMIT value"""
        self.customers = sqlite_db_controller.get_customers()
        if self.customers == None:
            pass
        else:
            count = 0
            result = ""
            for c in self.customers:
                if c.previous_customer == '' and c.quoted == '' and c.last_contact != '' and c.notes == '':
                    row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                    time_delta = DATE - row_date
                    email_check = c.email_address.rsplit('@')
                    if time_delta >= CALL_DATE and count < LIMIT[0]:
                        count += 1
                        if email_check[1] in EMAIL_CHECK:
                            result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nIndustry: {c.industry}\n***Use alternate email***\n\n"
                        else:
                            result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nDays since contact: {(time_delta.total_seconds()/86400):.0f} days\n\n"
                    elif count >= LIMIT[0]:
                        break
                    else:
                        continue
            c_display = Toplevel()
            c_display.title(f'Next {LIMIT[0]} prospects to email')
            c_display.geometry('500x300-75-75')
            display_customers = Text(c_display,width=500,height=300)
            ys = ttk.Scrollbar(c_display,orient='vertical',command=display_customers.yview)
            display_customers['yscrollcommand'] = ys.set
            display_customers.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_customers.insert(1.0,result)
            c_display.grid_columnconfigure(0, weight = 1)
            c_display.grid_rowconfigure(0, weight = 1)
            display_customers['state'] = 'disabled'
            test_prompt = messagebox.askyesno(message='Would you like to send test emails?')
            if test_prompt == True:
                self.send_prospect_test()
            else:
                pass
            
    def send_prospect_test(self):
        """To send test emails to prospects"""
        try:
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
                            if i_type in TARGETS:
                                var = SUBJP + SUBJT
                                subject = var[randint(0,len(var)-1)]
                            else:
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
        except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.',
            detail='You probably are not connected to debug server.')
        
    def send_prospect_email(self):
        """Send live emails to prospects"""
        try:
            confirm_send = messagebox.askyesno(message='Are you sure you want to send live emails?',
            icon='question',title='Confirm send')
            self.customers = sqlite_db_controller.get_customers()
            if confirm_send == True and self.customers != None:
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
                                if i_type in TARGETS:
                                    var = SUBJP + SUBJT
                                    subject = var[randint(0,len(var)-1)]
                                else:
                                    subject = SUBJP[randint(0,len(SUBJP)-1)]
                                body = PROSPECT_TEMPLATE[randint(0,len(PROSPECT_TEMPLATE)-1)].replace("Company",customer)
                                footer = FOOTER[randint(0,len(FOOTER)-1)]
                                live_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK.get(),
                                prev_cus,name,body,SIGNATURE,footer)
                                live_email.send_live_email(SMTP_SERVER,PORT,EMAIL_LOGIN,EMAIL_PASSWORD)
                                SENT_LIST.append(address)
                        elif count >= LIMIT[0]:
                            break
                        else:
                            continue
                messagebox.showinfo(message=f'{LIMIT[0]} Emails sent. Check mail server for delivery.')
                LIMIT.clear()
                LIMIT.append(randint(MIN_EMAIL,MAX_EMAIL))
                sqlite_db_controller.update_last_contact(SENT_LIST)
                SENT_LIST.clear()
            else:
                pass
        except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.')
            
    def View_Quoted(self):
        """View next quoted customers to send emails based on LIMIT value"""
        self.customers = sqlite_db_controller.get_customers()
        if self.customers == None:
            pass
        else:
            count = 0
            result = ""
            for c in self.customers:
                if c.quoted != '' and c.last_contact != '' and c.notes == '':
                    row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                    time_delta = DATE - row_date
                    email_check = c.email_address.rsplit('@')
                    if time_delta >= CALL_DATE and count < LIMIT[0]:
                        count += 1
                        if email_check[1] in EMAIL_CHECK:
                            result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nIndustry: {c.industry}\n***Use alternate email***\n\n"
                        else:
                            result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nDays since contact: {(time_delta.total_seconds()/86400):.0f} days\n\n"
                    elif count >= LIMIT[0]:
                        break
                    else:
                        continue
            c_display = Toplevel()
            c_display.title(f'Next {LIMIT[0]} quoted customers to email')
            c_display.geometry('500x300-75-75')
            display_customers = Text(c_display,width=500,height=300)
            ys = ttk.Scrollbar(c_display,orient='vertical',command=display_customers.yview)
            display_customers['yscrollcommand'] = ys.set
            display_customers.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_customers.insert(1.0,result)
            c_display.grid_columnconfigure(0, weight = 1)
            c_display.grid_rowconfigure(0, weight = 1)
            display_customers['state'] = 'disabled'
            test_prompt = messagebox.askyesno(message='Would you like to send test emails?')
            if test_prompt == True:
                self.send_quoted_test()
            else:
                pass
        
    def send_quoted_test(self):
        """To send test emails to quoted customers"""
        try:
            count = 0
            for c in self.customers:
                if c.quoted != '' and c.last_contact != '' and c.notes == '':
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
                            subject = SUBJQ[randint(0,len(SUBJQ)-1)]
                            body = QUOTED_CUSTOMER_TEMPLATE[randint(0,len(QUOTED_CUSTOMER_TEMPLATE)-1)].replace("Company",customer)
                            footer = FOOTER[randint(0,len(FOOTER)-1)]
                            test_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK.get(),
                            prev_cus,name,body,SIGNATURE,footer)
                            test_email.send_test_email()
                    elif count >= LIMIT[0]:
                        break
                    else:
                        continue
            messagebox.showinfo(message='Test emails sent. Check terminal printout for format.')
        except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.',
            detail='You probably are not connected to debug server.')
        
    def send_quoted_email(self):
        """Send live emails to quoted customers"""
        try:
            confirm_send = messagebox.askyesno(message='Are you sure you want to send live emails?',
            icon='question',title='Confirm send')
            self.customers = sqlite_db_controller.get_customers()
            if confirm_send == True and self.customers != None:
                count = 0
                for c in self.customers:
                    if c.quoted != '' and c.last_contact != '' and c.notes == '':
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
                                subject = SUBJQ[randint(0,len(SUBJQ)-1)]
                                body = QUOTED_CUSTOMER_TEMPLATE[randint(0,len(QUOTED_CUSTOMER_TEMPLATE)-1)].replace("Company",customer)
                                footer = FOOTER[randint(0,len(FOOTER)-1)]
                                live_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK.get(),
                                prev_cus,name,body,SIGNATURE,footer)
                                live_email.send_live_email(SMTP_SERVER,PORT,EMAIL_LOGIN,EMAIL_PASSWORD)
                                SENT_LIST.append(address)
                        elif count >= LIMIT[0]:
                            break
                        else:
                            continue
                messagebox.showinfo(message=f'{LIMIT[0]} Emails sent. Check mail server for delivery.')
                LIMIT.clear()
                LIMIT.append(randint(MIN_EMAIL,MAX_EMAIL))
                sqlite_db_controller.update_last_contact(SENT_LIST)
                SENT_LIST.clear()
            else:
                pass
        except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.')
            
    def View_Clients(self):
        """View next previous customers to send emails based on LIMIT value"""
        self.customers = sqlite_db_controller.get_customers()
        if self.customers == None:
            pass
        else:
            count = 0
            result = ""
            for c in self.customers:
                if c.previous_customer != '' and c.last_contact != '' and c.notes == '':
                    row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                    time_delta = DATE - row_date
                    email_check = c.email_address.rsplit('@')
                    if time_delta >= CALL_DATE and count < LIMIT[0]:
                        count += 1
                        if email_check[1] in EMAIL_CHECK:
                            result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nIndustry: {c.industry}\n***Use alternate email***\n\n"
                        else:
                            result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nDays since contact: {(time_delta.total_seconds()/86400):.0f} days\n\n"
                    elif count >= LIMIT[0]:
                        break
                    else:
                        continue
            c_display = Toplevel()
            c_display.title(f'Next {LIMIT[0]} previous customers to email')
            c_display.geometry('500x300-75-75')
            display_customers = Text(c_display,width=500,height=300)
            ys = ttk.Scrollbar(c_display,orient='vertical',command=display_customers.yview)
            display_customers['yscrollcommand'] = ys.set
            display_customers.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_customers.insert(1.0,result)
            c_display.grid_columnconfigure(0, weight = 1)
            c_display.grid_rowconfigure(0, weight = 1)
            display_customers['state'] = 'disabled'
            test_prompt = messagebox.askyesno(message='Would you like to send test emails?')
            if test_prompt == True:
                self.send_client_test()
            else:
                pass
        
    def send_client_test(self):
        """To send test emails to previous customers"""
        try:
            count = 0
            for c in self.customers:
                if c.previous_customer != '' and c.last_contact != '' and c.notes == '':
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
                            subject = SUBJE[randint(0,len(SUBJE)-1)]
                            body = PREVIOUS_CUSTOMER_TEMPLATE[randint(0,len(PREVIOUS_CUSTOMER_TEMPLATE)-1)].replace("Company",customer)
                            footer = FOOTER[randint(0,len(FOOTER)-1)]
                            test_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK.get(),
                            prev_cus,name,body,SIGNATURE,footer)
                            test_email.send_test_email()
                    elif count >= LIMIT[0]:
                        break
                    else:
                        continue
            messagebox.showinfo(message='Test emails sent. Check terminal printout for format.')
        except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.',
            detail='You probably are not connected to debug server.')
        
    def send_client_email(self):
        """Send live emails to previous customers"""
        try:
            confirm_send = messagebox.askyesno(message='Are you sure you want to send live emails?',
            icon='question',title='Confirm send')
            self.customers = sqlite_db_controller.get_customers()
            if confirm_send == True and self.customers != None:
                count = 0
                for c in self.customers:
                    if c.previous_customer != '' and c.last_contact != '' and c.notes == '':
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
                                subject = SUBJE[randint(0,len(SUBJE)-1)]
                                body = PREVIOUS_CUSTOMER_TEMPLATE[randint(0,len(PREVIOUS_CUSTOMER_TEMPLATE)-1)].replace("Company",customer)
                                footer = FOOTER[randint(0,len(FOOTER)-1)]
                                live_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK.get(),
                                prev_cus,name,body,SIGNATURE,footer)
                                live_email.send_live_email(SMTP_SERVER,PORT,EMAIL_LOGIN,EMAIL_PASSWORD)
                                SENT_LIST.append(address)
                        elif count >= LIMIT[0]:
                            break
                        else:
                            continue
                messagebox.showinfo(message=f'{LIMIT[0]} Emails sent. Check mail server for delivery.')
                LIMIT.clear()
                LIMIT.append(randint(MIN_EMAIL,MAX_EMAIL))
                sqlite_db_controller.update_last_contact(SENT_LIST)
                SENT_LIST.clear()
            else:
                pass
        except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.')
        
    def send_holiday_test(self):
        """To send test holiday emails to previous customers"""
        try:
            self.customers = sqlite_db_controller.get_customers()
            if self.customers == None:
                pass
            else:
                count = 0
                for c in self.customers:
                    if c.previous_customer != '' and c.last_contact != '' and c.notes == '':
                        email_check = c.email_address.rsplit('@')
                        if count < LIMIT[0]:
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
                                subject = SUBJH
                                body = HOLIDAY_TEMPLATE.replace("Company",customer)
                                footer = ''
                                test_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK.get(),
                                prev_cus,name,body,SIGNATURE,footer)
                                test_email.send_test_email()
                        elif count >= LIMIT[0]:
                            break
                        else:
                            continue
                messagebox.showinfo(message=f'{LIMIT[0]} Test emails sent. Check terminal printout for format.')
        except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.',
            detail='You probably are not connected to debug server.')
        
    def send_holiday_email(self):
        """Send holiday emails to previous customers"""
        try:
            confirm_send = messagebox.askyesno(message='Are you sure you want to send live emails?',
            icon='question',title='Confirm send')
            self.customers = sqlite_db_controller.get_customers()
            if confirm_send == True and self.customers != None:
                count = 0
                for c in self.customers:
                    if c.previous_customer != '' and c.last_contact != '' and c.notes == '':
                        email_check = c.email_address.rsplit('@')
                        if count < LIMIT[0]:
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
                                subject = SUBJH
                                body = HOLIDAY_TEMPLATE.replace("Company",customer)
                                footer = ''
                                live_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK.get(),
                                prev_cus,name,body,SIGNATURE,footer)
                                live_email.send_live_email(SMTP_SERVER,PORT,EMAIL_LOGIN,EMAIL_PASSWORD)
                                SENT_LIST.append(address)
                        elif count >= LIMIT[0]:
                            break
                        else:
                            continue
                messagebox.showinfo(message=f'{LIMIT[0]} Emails sent. Check mail server for delivery.')
                LIMIT.clear()
                LIMIT.append(randint(MIN_EMAIL,MAX_EMAIL))
                sqlite_db_controller.update_last_contact(SENT_LIST)
                SENT_LIST.clear()
            else:
                pass
        except Exception as e:
            messagebox.showerror(message=f'System error encountered {e}.')
            
root = Tk()
EmailMarketing(root)
root.mainloop()
