from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import sqlite_db_controller
from sqlite_db_controller import *
import settings
from settings import *

def get_date():
    """Get date for email functions"""
    DATE = datetime.today()
    return DATE

def view_all_customers():
    """View all customers in DB"""
    customers = sqlite_db_controller.get_customers()
    if customers == None:
        pass
    else:
        result = "%5s%60s%10s%20s%45s%15s%30s\n" % ("ID","Company","Status","Name","Email","Last contact","Notes")
        for c in customers:
            result += "%5s%60s%10s%20s%45s%15s%30s\n" % (c.customerID,c.company,c.status,c.first_name,c.email_address,
            c.last_contact,c.notes)
        c_display = Toplevel()
        c_display.title('All customers')
        c_display.geometry('1360x738')
        display_customers = Text(c_display,width=1360,height=738,wrap='none')
        ys = ttk.Scrollbar(c_display,orient='vertical',command=display_customers.yview)
        xs = ttk.Scrollbar(c_display,orient='horizontal',command=display_customers.xview)
        display_customers['yscrollcommand'] = ys.set
        display_customers['xscrollcommand'] = xs.set
        display_customers.grid(column=0,row=0)
        ys.grid(column=1,row=0,sticky=(N,S))
        xs.grid(column=0,row=1,sticky='we')
        display_customers.insert(1.0,result)
        c_display.grid_columnconfigure(0,weight=1)
        c_display.grid_rowconfigure(0,weight=1)

def view_next_bulk(build):
    """View next bulk emails based on build variable passed"""
    customers = sqlite_db_controller.get_random_customers()
    if customers == None:
        pass
    else:
        count = 0
        result = ""
        send_list = []
        for c in customers:
            if c.status == f'{build}' and c.email_address != '' and c.last_contact != '':
                row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                time_delta = get_date() - row_date
                email_check = c.email_address.rsplit('@')
                if time_delta >= settings.CALL_DATE and count < settings.LIMIT[0]:
                    if email_check[1] in settings.EMAIL_CHECK:
                        result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\n***Use alternate email***\n\n"
                    else:
                        result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nDays since contact: {(time_delta.total_seconds()/86400):.0f} days\nNotes: {c.notes}\n\n"
                        count += 1
                        send_list.append(c)
                elif count >= settings.LIMIT[0]:
                    break
                else:
                    continue
        c_display = Toplevel()
        c_display.title(f'Next {settings.LIMIT[0]} customer to email')
        c_display.geometry('500x300-75-75')
        display_customers = Text(c_display,width=500,height=300)
        ys = ttk.Scrollbar(c_display,orient='vertical',command=display_customers.yview)
        display_customers['yscrollcommand'] = ys.set
        display_customers.grid(column=0,row=0)
        ys.grid(column=1,row=0,sticky=(N,S))
        display_customers.insert(1.0,result)
        c_display.grid_columnconfigure(0,weight=1)
        c_display.grid_rowconfigure(0,weight=1)
        button = ttk.Button(c_display,text=f'Send test emails',
        command=lambda:[send_bulk_email('test',send_list)])
        button.grid()
        button = ttk.Button(c_display,text=f'Send live emails',
        command=lambda:[send_bulk_email('live',send_list),c_display.destroy()])
        button.grid()
        button = ttk.Button(c_display,text=f'Close & exit',command=lambda:c_display.destroy())
        button.grid()
        
def view_holiday_email(build):
    """Send holiday messages to existing customers"""
    customers = sqlite_db_controller.get_customers()
    if customers == None:
        pass
    else:
        count = 0
        result = ""
        send_list = []
        for c in customers:
            if c.status == f'{build}' and c.email_address != '' and c.last_contact != '':
                row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                time_delta = get_date() - row_date
                email_check = c.email_address.rsplit('@')
                if count < settings.LIMIT[0]:
                    if email_check[1] in settings.EMAIL_CHECK:
                        result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\n***Use alternate email***\n\n"
                    else:
                        result += f"Company: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nDays since contact: {(time_delta.total_seconds()/86400):.0f} days\nNotes: {c.notes}\n\n"
                        count += 1
                        send_list.append(c)
                elif count >= settings.LIMIT[0]:
                    break
                else:
                    continue
        c_display = Toplevel()
        c_display.title(f'Next {settings.LIMIT[0]} customer to email')
        c_display.geometry('500x300-75-75')
        display_customers = Text(c_display,width=500,height=300)
        ys = ttk.Scrollbar(c_display,orient='vertical',command=display_customers.yview)
        display_customers['yscrollcommand'] = ys.set
        display_customers.grid(column=0,row=0)
        ys.grid(column=1,row=0,sticky=(N,S))
        display_customers.insert(1.0,result)
        c_display.grid_columnconfigure(0,weight=1)
        c_display.grid_rowconfigure(0,weight=1)
        button = ttk.Button(c_display,text=f'Send test holiday message',
        command=lambda:[send_holiday_message('test',send_list)])
        button.grid()
        button = ttk.Button(c_display,text=f'Send live holiday message',
        command=lambda:[send_holiday_message('live',send_list),c_display.destroy()])
        button.grid()
        button = ttk.Button(c_display,text=f'Close & exit',command=lambda:c_display.destroy())
        button.grid()
        
def send_bulk_email(build,send_list):
    """Build and send bulk messages"""
    try:
        for c in send_list:
            if c.status == 'prospect':
                subject = settings.PROSPECT_SUBJECTS[randint(0,len(settings.PROSPECT_SUBJECTS)-1)]
                body = settings.PROSPECT_TEMPLATES[randint(0,len(settings.PROSPECT_TEMPLATES)-1)].replace("Company",c.company)
            elif c.status == 'target':
                subject = settings.TARGET_SUBJECTS[randint(0,len(settings.TARGET_SUBJECTS)-1)]
                body = settings.TARGET_TEMPLATES[randint(0,len(settings.TARGET_TEMPLATES)-1)].replace("Company",c.company)
            elif c.status == 'quoted':
                subject = settings.QUOTED_SUBJECTS[randint(0,len(settings.QUOTED_SUBJECTS)-1)]
                body = settings.QUOTED_TEMPLATES[randint(0,len(settings.QUOTED_TEMPLATES)-1)].replace("Company",c.company)
            elif c.status == 'customer':
                subject = settings.CUSTOMER_SUBJECTS[randint(0,len(settings.CUSTOMER_SUBJECTS)-1)]
                body = settings.CUSTOMER_TEMPLATES[randint(0,len(settings.CUSTOMER_TEMPLATES)-1)].replace("Company",c.company)
            else:
                subject = settings.PARTNER_SUBJECTS[randint(0,len(settings.PARTNER_SUBJECTS)-1)]
                body = settings.PARTNER_TEMPLATES[randint(0,len(settings.PARTNER_TEMPLATES)-1)].replace("Company",c.company)
            if build == 'test':
                test_email = MarketingEmail(c.email_address,subject,c.first_name,c.status,body)
                test_email.send_test_email()
            else:
                live_email = MarketingEmail(c.email_address,subject,c.first_name,c.status,body)
                live_email.send_live_email()
                settings.SENT_LIST.append(c.email_address)
        if build == 'live':
            settings.LIMIT.clear()
            settings.LIMIT.append(randint(settings.MIN_EMAIL,settings.MAX_EMAIL))
            sqlite_db_controller.update_last_contact(settings.SENT_LIST)
            settings.SENT_LIST.clear()
            messagebox.showinfo(message=f'{settings.LIMIT[0]} Emails sent.',detail='Check mail server for delivery.')
        else:
            messagebox.showinfo(message='Test emails sent.',detail='Check terminal printout for format.')
    except Exception as e:
        messagebox.showerror(message='System error encountered.',detail=f'{e}')
        
def send_holiday_message(build,send_list):
    """Build and send holiday message"""
    try:
        for c in send_list:
            subject = settings.HOLIDAY_SUBJECTS[randint(0,len(settings.HOLIDAY_SUBJECTS)-1)]
            body = settings.HOLIDAY_TEMPLATES[randint(0,len(settings.HOLIDAY_TEMPLATES)-1)].replace("Company",c.company)
            if build == 'test':
                test_email = MarketingEmail(c.email_address,subject,c.first_name,c.status,body)
                test_email.send_test_email()
            else:
                live_email = MarketingEmail(c.email_address,subject,c.first_name,c.status,body)
                live_email.send_live_email()
                settings.SENT_LIST.append(c.email_address)
        if build == 'live':
            settings.LIMIT.clear()
            settings.LIMIT.append(randint(settings.MIN_EMAIL,settings.MAX_EMAIL))
            sqlite_db_controller.update_last_contact(settings.SENT_LIST)
            settings.SENT_LIST.clear()
            messagebox.showinfo(message=f'{settings.LIMIT[0]} Emails sent.',detail='Check mail server for delivery.')
        else:
            messagebox.showinfo(message='Test emails sent.',detail='Check terminal printout for format.')
    except Exception as e:
        messagebox.showerror(message='System error encountered.',detail=f'{e}')
    
def view_next_single(build):
    """View single email based on build variable passed"""
    customers = sqlite_db_controller.get_random_customers()
    if customers == None:
        pass
    else:
        try:
            count = 1
            result = ""
            for c in customers:
                if c.status == f'{build}' and c.email_address != '' and c.last_contact != '':
                    row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                    time_delta = get_date() - row_date
                    email_check = c.email_address.rsplit('@')
                    if time_delta >= settings.CALL_DATE and count > 0:
                        count -= 1
                        if email_check[1] in settings.EMAIL_CHECK:
                            pass
                        else:
                            result += f"ID: {c.customerID}\nCompany: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nDays since contact: {(time_delta.total_seconds()/86400):.0f} days\nStatus: {c.status}\nNotes: {c.notes}"
                            name = c.first_name
                            status = c.status
                            customer = c.company
                            address = c.email_address
                    else:
                        continue
            c_display = Toplevel()
            c_display.title(f'Next customer to email')
            c_display.geometry('500x300-75-75')
            display_customers = Text(c_display,width=500,height=300)
            ys = ttk.Scrollbar(c_display,orient='vertical',command=display_customers.yview)
            display_customers['yscrollcommand'] = ys.set
            display_customers.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_customers.insert(1.0,result)
            c_display.grid_columnconfigure(0,weight=1)
            c_display.grid_rowconfigure(0,weight=1)
            button = ttk.Button(c_display,text=f'Send test email',
            command=lambda:[build_single_email('test',name,status,customer,address)])
            button.grid()
            button = ttk.Button(c_display,text=f'Send live email',
            command=lambda:[build_single_email('live',name,status,customer,address),c_display.destroy()])
            button.grid()
            button = ttk.Button(c_display,text=f'Close & exit',command=lambda:c_display.destroy())
            button.grid()
        except Exception as e:
            messagebox.showerror(message='System error encountered.',detail=f'{e}')
            
def random_email():
    """Send random order single emails"""
    customers = sqlite_db_controller.get_random_customers()
    if customers == None:
        pass
    else:
        try:
            count = 1
            result = ""
            for c in customers:
                if c.status != 'removed' and c.email_address != '' and c.last_contact != '':
                    row_date = datetime.strptime(c.last_contact, "%m/%d/%y")
                    time_delta = get_date() - row_date
                    email_check = c.email_address.rsplit('@')
                    if time_delta >= settings.CALL_DATE and count > 0:
                        count -= 1
                        if email_check[1] in settings.EMAIL_CHECK:
                            pass
                        else:
                            result += f"ID: {c.customerID}\nCompany: {c.company}\nName: {c.first_name}\nEmail: {c.email_address}\nDays since contact: {(time_delta.total_seconds()/86400):.0f} days\nStatus: {c.status}\nNotes: {c.notes}"
                            name = c.first_name
                            status = c.status
                            customer = c.company
                            address = c.email_address
                    else:
                        continue
            c_display = Toplevel()
            c_display.title(f'Next customer to email')
            c_display.geometry('500x300-75-75')
            display_customers = Text(c_display,width=500,height=300)
            ys = ttk.Scrollbar(c_display,orient='vertical',command=display_customers.yview)
            display_customers['yscrollcommand'] = ys.set
            display_customers.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_customers.insert(1.0,result)
            c_display.grid_columnconfigure(0,weight=1)
            c_display.grid_rowconfigure(0,weight=1)
            button = ttk.Button(c_display,text=f'Send test email',
            command=lambda:[build_single_email('test',name,status,customer,address)])
            button.grid()
            button = ttk.Button(c_display,text=f'Send live email',
            command=lambda:[build_single_email('live',name,status,customer,address),c_display.destroy()])
            button.grid()
            button = ttk.Button(c_display,text=f'Close & exit',command=lambda:c_display.destroy())
            button.grid()
        except Exception as e:
            messagebox.showerror(message='System error encountered.',detail=f'{e}')
             
def build_single_email(build,name,status,customer,address):
    """Send single test or live email"""
    try:
        subject = StringVar()
        body = StringVar(value=settings.ALL_TEMPLATES)
        user_entry = Toplevel()
        user_entry.title("Build email")
        user_entry.geometry('1100x700')
        frame = ttk.Frame(user_entry,width=1100, height=700)
        frame.grid(column=0,row=0)
        user_entry.grid_columnconfigure(0,weight=1)
        user_entry.grid_rowconfigure(0,weight=1)
        label = ttk.Label(frame, text='Choose subject',font='Helvetica 12 bold')
        label.grid(sticky=W)
        for s in settings.ALL_SUBJECTS:
            rb = ttk.Radiobutton(frame,compound='left',text=f'{s}',variable=subject,value=f'{s}')
            rb.grid(sticky=W)
        label = ttk.Label(frame,text='Choose email body',font='Helvetica 12 bold')
        label.grid()
        bbox = Listbox(frame,listvariable=body,selectmode="single",width=120,height=10)
        bbox.grid()
        button = ttk.Button(frame,text=f'Submit',
        command=lambda:[listbox_error(bbox.curselection()),send_single_email(build,name,status,customer,address
        ,subject.get(),bbox.get(bbox.curselection())),user_entry.destroy()])
        button.grid()
    except Exception as e:
        messagebox.showerror(message='System error encountered.',detail=f'{e}')
        
def send_single_email(*args):
    """Send single test and live email"""
    try:
        if args[5] == '':
            messagebox.showerror(message='You must select a subject',detail='Please retry.')
        else:
            if args[0] == 'test':
                body = args[6].replace("Company",args[3])
                test_email = MarketingEmail(args[4],args[5],args[1],args[2],body)
                test_email.send_test_email()
                messagebox.showinfo(message='Test emails sent.',detail='Check terminal printout for format.')
            else:
                body = args[6].replace("Company",args[3])
                live_email = MarketingEmail(args[4],args[5],args[1],args[2],body)
                live_email.send_live_email()
                settings.SENT_LIST.append(args[4])
                sqlite_db_controller.update_last_contact(settings.SENT_LIST)
                settings.SENT_LIST.clear()
                messagebox.showinfo(message='Email sent.',detail='Check mail server for delivery.')
    except Exception as e:
        messagebox.showerror(message='System error encountered.',detail=f'{e}')
        
def listbox_error(list_var):
    """Catch empty listboxes"""
    if list_var == ():
        messagebox.showerror(message='You must complete all fields in order to continue.',
        detail='You may also close window to cancel.')
