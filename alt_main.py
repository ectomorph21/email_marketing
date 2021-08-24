from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import create_sqlite_db
import sqlite_db_controller
from objects import *

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
        SIGNATURE = user['SIGNATURE2']
        EMAIL_CHECK = user['BAD_DOMAINS']
        TARGETS = user['TARGET_CUSTOMERS']
    for subject in data['alternate_subject']:
        SUBJC = subject['customer']
        SUBJSAS = subject['partner']
        SUBJP = subject['previous_customer']
        SUBJH = subject['holiday']
    for email in data['alternate_email']:
        CUSTOMER_TEMPLATE = email['buyer_seller']
        PARTNER_TEMPLATE = email['showing_agent']
        PREVIOUS_PARTNER_TEMPLATE = email['previous']
        HOLIDAY_TEMPLATE = email['holiday']
    for footer in data['alternate_footer']:
        FOOTER1 = footer['customer']
        FOOTER2 = footer['partner']
        
DATE = datetime.today()
LIMIT = [randint(MIN_EMAIL,MAX_EMAIL)]
SENT_LIST = []

class Alt_Email:
    def __init__(self,db_name):
        """Alternate Main tkinter window"""
        self.DB_CHECK = db_name
        self.alternate_window = Toplevel()
        self.alternate_window.title(f"{db_name.upper()} Email")
        welcome_frame = ttk.Frame(self.alternate_window)
        welcome_frame.grid(column=0,row=0)
        s = ttk.Style()
        s.theme_use('alt')
        s.configure('Caution.TButton',font='helvetica 12',foreground='red',padding=3)
        s.configure('Action.TButton',font='helvetica 12',foreground='green',padding=3)
        welcome_frame.grid(column=0,row=0)
        #db buttons
        connect_db = ttk.Button(welcome_frame, text='Connect to DB',
        command=lambda:self.find_db_file()).grid(column=1,row=1,sticky=(N,S,E,W))
        create_db_button = ttk.Button(welcome_frame,text=f'Create SQLite DB',
        command=lambda:self.list_db()).grid(column=2,row=1,sticky=(N,S,E,W))
        export_db_csv = ttk.Button(welcome_frame,text=f'Export DB to CSV',
        command=self.export_db).grid(column=3,row=1,columnspan=2,sticky=(N,S,E,W))
        #view and send buttons
        view_customers_button = ttk.Button(welcome_frame,text='View next customers',style='Action.TButton',
        command=self.View_Customers).grid(column=1,row=2,columnspan=2,sticky=(N,S,E,W))
        send_prospects_button = ttk.Button(welcome_frame,text='Send email to customers',style='Caution.TButton',
        command=self.send_customer_email).grid(column=3,row=2,columnspan=2,sticky=(N,S,E,W))
        view_partners_button = ttk.Button(welcome_frame,text='View next partners',style='Action.TButton',
        command=self.View_Partners).grid(column=1,row=3,columnspan=2,sticky=(N,S,E,W))
        send_partners_button = ttk.Button(welcome_frame,text='Send email to partners',style='Caution.TButton',
        command=self.send_partner_email).grid(column=3,row=3,columnspan=2,sticky=(N,S,E,W))
        holiday_test_button = ttk.Button(welcome_frame,text='Send test holiday email',style='Action.TButton',
        command=self.send_holiday_test).grid(column=1,row=5,columnspan=2,sticky=(N,S,E,W))
        send_holiday_button = ttk.Button(welcome_frame,text='Send holiday email',style='Caution.TButton',
        command=self.send_holiday_email).grid(column=3,row=5,columnspan=2,sticky=(N,S,E,W))
        self.alternate_window.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        """Executes when window is closed"""
        messagebox.showinfo(message=f'{self.DB_CHECK.upper()} controller closed. Recommend close main window.')
        self.alternate_window.destroy()
    
    def find_db_file(self):
        """method to select and connect to existing DB"""
        db_list = Tk()
        db_list.geometry("175x175")
        db_list.title('Select database')
        rb = ttk.Radiobutton(db_list,text=f'{self.DB_CHECK} db',variable=self.DB_CHECK,value=f'{self.DB_CHECK}',
        command=self.select_db).pack()
        close_button = ttk.Button(db_list,text='select',command=lambda:db_list.destroy()).pack()
        
    def select_db(self):
        """Select database method tied to find_db_file method"""
        db_name = self.DB_CHECK
        sqlite_db_controller.find_db_file(db_name)
        
    def list_db(self):
        """Method for selection of DB to create or overwrite"""
        db_select = Tk()
        db_select.geometry("175x175")
        db_select.title('Select database')
        rb = ttk.Radiobutton(db_select,text=f'{self.DB_CHECK} db',variable=self.DB_CHECK,value=f'{self.DB_CHECK}',
        command=self.create_db).pack()
        close_button = ttk.Button(db_select,text='select',command=lambda:db_select.destroy()).pack()
        
    def create_db(self):
        """Method to create new or overwrite existing DB. Tied to list_db"""
        csv_file = filedialog.askopenfilename(filetypes=[("CSV",'*.csv')])
        if csv_file == () or csv_file == "":
            messagebox.showerror(message='You must select a csv file to utilize this option.')
        else:
            upload_csv = messagebox.askyesno(message='Are you sure you want to upload csv file and overwrite existing SQLite database or create new db if none exist?',icon='question',title='Upload')
            if upload_csv == True:
                create_sqlite_db.Create_Database(csv_file,self.DB_CHECK)
            else:
                messagebox.showinfo(message='Operation cancelled. No DB created.')
        
    def export_db(self):
        """Method to export DB to csv file"""
        if self.DB_CHECK == None:
            messagebox.showerror(message="You must connect to an existing DB.'")
        else:
            sqlite_db_controller.export_db_csv(self.DB_CHECK)
            
    def View_Customers(self):
        """View next customers to send emails based on LIMIT value"""
        self.customers = sqlite_db_controller.get_customers()
        if self.customers == None:
            pass
        else:
            count = 0
            result = ""
            for c in self.customers:
                if c.industry.upper() == 'CUSTOMER' and c.last_contact != '' and c.notes == '':
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
            c_display.title(f'Next {LIMIT[0]} customers to email')
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
                self.send_customer_test()
            else:
                pass
            
    def send_customer_test(self):
        """To send test emails to customers"""
        try:
            count = 0
            for c in self.customers:
                if c.industry.upper() == 'CUSTOMER' and c.last_contact != '' and c.notes == '':
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
                            subject = SUBJC[randint(0,len(SUBJC)-1)]
                            body = CUSTOMER_TEMPLATE[randint(0,len(CUSTOMER_TEMPLATE)-1)]
                            footer = FOOTER1[randint(0,len(FOOTER1)-1)]
                            test_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK,
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
        
    def send_customer_email(self):
        """Send live emails to customers"""
        try:
            confirm_send = messagebox.askyesno(message='Are you sure you want to send live emails?',
            icon='question',title='Confirm send')
            self.customers = sqlite_db_controller.get_customers()
            if confirm_send == True and self.customers != None:
                count = 0
                for c in self.customers:
                    if c.industry.upper() == 'CUSTOMER' and c.last_contact != '' and c.notes == '':
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
                                subject = SUBJC[randint(0,len(SUBJC)-1)]
                                body = CUSTOMER_TEMPLATE[randint(0,len(CUSTOMER_TEMPLATE)-1)]
                                footer = FOOTER1[randint(0,len(FOOTER1)-1)]
                                live_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK,
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
            
    def View_Partners(self):
        """View next partners to send emails based on LIMIT value"""
        self.customers = sqlite_db_controller.get_customers()
        if self.customers == None:
            pass
        else:
            count = 0
            result = ""
            for c in self.customers:
                if c.industry.upper() == 'PARTNER' and c.last_contact != '' and c.notes == '':
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
            c_display.title(f'Next {LIMIT[0]} partners to email')
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
                self.send_partner_test()
            else:
                pass
        
    def send_partner_test(self):
        """To send test emails to partners"""
        try:
            count = 0
            for c in self.customers:
                if c.industry.upper() == 'PARTNER' and c.last_contact != '' and c.notes == '':
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
                            if prev_cus.upper() == 'X':
                                subject = SUBJP[randint(0,len(SUBJP)-1)]
                                body = PREVIOUS_PARTNER_TEMPLATE[randint(0,len(PREVIOUS_PARTNER_TEMPLATE)-1)]
                            else:
                                subject = SUBJSAS[randint(0,len(SUBJSAS)-1)]
                                body = PARTNER_TEMPLATE[randint(0,len(PARTNER_TEMPLATE)-1)]
                            footer = FOOTER2[randint(0,len(FOOTER2)-1)]
                            test_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK,
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
        
    def send_partner_email(self):
        """Send live emails to partners"""
        try:
            confirm_send = messagebox.askyesno(message='Are you sure you want to send live emails?',
            icon='question',title='Confirm send')
            self.customers = sqlite_db_controller.get_customers()
            if confirm_send == True and self.customers != None:
                count = 0
                for c in self.customers:
                    if c.industry.upper() == 'PARTNER' and c.last_contact != '' and c.notes == '':
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
                                if prev_cus.upper() == 'X':
                                    subject = SUBJP[randint(0,len(SUBJP)-1)]
                                    body = PREVIOUS_PARTNER_TEMPLATE[randint(0,len(PREVIOUS_PARTNER_TEMPLATE)-1)]
                                else:
                                    subject = SUBJSAS[randint(0,len(SUBJSAS)-1)]
                                    body = PARTNER_TEMPLATE[randint(0,len(PARTNER_TEMPLATE)-1)]
                                footer = FOOTER2[randint(0,len(FOOTER2)-1)]
                                live_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK,
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
                                body = HOLIDAY_TEMPLATE
                                footer = ''
                                test_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK,
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
                                body = HOLIDAY_TEMPLATE
                                footer = ''
                                live_email = MarketingEmail(FROM,address,subject,DOMAIN,UNSUBSCRIBE,self.DB_CHECK,
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
