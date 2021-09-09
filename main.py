from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
from pytz import *
import create_sqlite_db
import sqlite_db_controller
from objects import *
import settings
from settings import *
from email_controller import *
import email_controller

class MainGUI:
    def __init__(self, root):
        """Main tkinter window"""
        self.GITHUB_PAGE = 'https://github.com/ectomorph21/email_marketing'
        self.WEBSITE = 'https://www.randmssolutions.com/'
#        print(root.state())
#        print(root.wm_maxsize())
        root.title("Email Marketing")
        root.resizable(FALSE,FALSE)
        welcome_frame = ttk.Frame(root)
        welcome_frame.grid(column=0,row=0)
        s = ttk.Style()
        s.theme_use('alt')
        s.configure('Caution.TButton',font='helvetica 12',foreground='red',padding=3)
        s.configure('Action.TButton',font='helvetica 12',foreground='green',padding=3)
        #db buttons
        connect_db = ttk.Button(welcome_frame,text='Connect to DB',
        command=lambda:sqlite_db_controller.locate_file())
        connect_db.grid(column=1,row=1,rowspan=2,sticky=(N,S,E,W))
        close_db = ttk.Button(welcome_frame,text='Close DB',
        command=lambda:self.close_db())
        close_db.grid(column=1,row=3,rowspan=2,sticky=(N,S,E,W))
        create_user = ttk.Button(welcome_frame,text='Create User',
        command=lambda:create_sqlite_db.Enter_User_Data())
        create_user.grid(column=2,row=1,rowspan=2,sticky=(N,S,E,W))
        update_user = ttk.Button(welcome_frame,text='Update User',
        command=lambda:self.update_user())
        update_user.grid(column=2,row=3,rowspan=2,sticky=(N,S,E,W))
        upload_customers = ttk.Button(welcome_frame,text='Upload customers',
        command=lambda:self.upload_customers())
        upload_customers.grid(column=3,row=1,sticky=(N,S,E,W))
        create_customer = ttk.Button(welcome_frame,text='Create customer',
        command=lambda:sqlite_db_controller.create_customer())
        create_customer.grid(column=3,row=2,sticky=(N,S,E,W))
        update_customer = ttk.Button(welcome_frame,text='Update customer',
        command=lambda:self.update_customer())
        update_customer.grid(column=3,row=3,sticky=(N,S,E,W))
        delete_customer = ttk.Button(welcome_frame,text='Delete customer',
        command=lambda:self.delete_customer())
        delete_customer.grid(column=3,row=4,sticky=(N,S,E,W))
        view_subjects = ttk.Button(welcome_frame,text='View subjects',
        command=lambda:self.view_subjects())
        view_subjects.grid(column=4,row=1,sticky=(N,S,E,W))
        create_subject = ttk.Button(welcome_frame,text='Create subject',
        command=lambda:sqlite_db_controller.create_subject())
        create_subject.grid(column=4,row=2,sticky=(N,S,E,W))
        update_subject = ttk.Button(welcome_frame,text='Update subject',
        command=lambda:sqlite_db_controller.update_subject())
        update_subject.grid(column=4,row=3,sticky=(N,S,E,W))
        delete_subject = ttk.Button(welcome_frame,text='Delete subject',
        command=lambda:self.delete_subject())
        delete_subject.grid(column=4,row=4,sticky=(N,S,E,W))
        view_templates = ttk.Button(welcome_frame,text='View templates',
        command=lambda:self.view_templates())
        view_templates.grid(column=5,row=1,sticky=(N,S,E,W))
        create_template = ttk.Button(welcome_frame,text='Create template',
        command=lambda:sqlite_db_controller.create_template())
        create_template.grid(column=5,row=2,sticky=(N,S,E,W))
        update_template = ttk.Button(welcome_frame,text='Update template',
        command=lambda:sqlite_db_controller.update_template())
        update_template.grid(column=5,row=3,sticky=(N,S,E,W))
        delete_template = ttk.Button(welcome_frame,text='Delete template',
        command=lambda:self.delete_template())
        delete_template.grid(column=5,row=4,sticky=(N,S,E,W))
        view_footers = ttk.Button(welcome_frame,text='View footers',
        command=lambda:self.view_footers())
        view_footers.grid(column=6,row=1,sticky=(N,S,E,W))
        create_footer = ttk.Button(welcome_frame,text='Create footer',
        command=lambda:sqlite_db_controller.create_footer())
        create_footer.grid(column=6,row=2,sticky=(N,S,E,W))
        update_footer = ttk.Button(welcome_frame,text='Update footer',
        command=lambda:self.update_footer())
        update_footer.grid(column=6,row=3,sticky=(N,S,E,W))
        delete_footer = ttk.Button(welcome_frame, text='Delete footer',
        command=lambda:self.delete_footer())
        delete_footer.grid(column=6,row=4,sticky=(N,S,E,W))
        view_bad_domains = ttk.Button(welcome_frame,text='View bad domains',
        command=lambda:self.view_bad_domains())
        view_bad_domains.grid(column=7,row=1,sticky=(N,S,E,W))
        add_bad_domain = ttk.Button(welcome_frame,text='Add bad domain',
        command=lambda:sqlite_db_controller.add_bad_domain())
        add_bad_domain.grid(column=7,row=2,sticky=(N,S,E,W))
        delete_bad_domain = ttk.Button(welcome_frame,text='Delete bad domain',
        command=lambda:self.delete_bad_domain())
        delete_bad_domain.grid(column=7,row=3,sticky=(N,S,E,W))
        export_csv = ttk.Button(welcome_frame, text='Export customers',
        command=lambda:sqlite_db_controller.export_csv())
        export_csv.grid(column=7,row=4,sticky=(N,S,E,W))
        #customer views and action buttons
        view_all_button = ttk.Button(welcome_frame, text='View all customers',style='Action.TButton',
        command=lambda:email_controller.view_all_customers())
        view_all_button.grid(column=1,row=5,rowspan=2,sticky=(N,S,E,W))
        random_email = ttk.Button(welcome_frame, text='View random',style='Action.TButton',
        command=lambda:email_controller.random_email())
        random_email.grid(column=2,row=5,rowspan=2,sticky=(N,S,E,W))
        view_prospects = ttk.Button(welcome_frame, text='View prospects',style='Action.TButton',
        command=lambda:email_controller.view_next_bulk('prospect'))
        view_prospects.grid(column=3,row=5,sticky=(N,S,E,W))
        view_targets = ttk.Button(welcome_frame, text='View targets',style='Action.TButton',
        command=lambda:email_controller.view_next_bulk('target'))
        view_targets.grid(column=4,row=5,sticky=(N,S,E,W))
        view_quoted = ttk.Button(welcome_frame, text='View quoted',style='Action.TButton',
        command=lambda:email_controller.view_next_bulk('quoted'))
        view_quoted.grid(column=5,row=5,sticky=(N,S,E,W))
        view_customers = ttk.Button(welcome_frame, text='View customers',style='Action.TButton',
        command=lambda:email_controller.view_next_bulk('customer'))
        view_customers.grid(column=6,row=5,sticky=(N,S,E,W))
        view_partners = ttk.Button(welcome_frame, text='View partners',style='Action.TButton',
        command=lambda:email_controller.view_next_bulk('partner'))
        view_partners.grid(column=7,row=5,sticky=(N,S,E,W))
        single_prospect = ttk.Button(welcome_frame, text='Single prospect',style='Action.TButton',
        command=lambda:email_controller.view_next_single('prospect'))
        single_prospect.grid(column=3,row=6,sticky=(N,S,E,W))
        single_target = ttk.Button(welcome_frame, text='Single target',style='Action.TButton',
        command=lambda:email_controller.view_next_single('target'))
        single_target.grid(column=4,row=6,sticky=(N,S,E,W))
        single_quoted = ttk.Button(welcome_frame, text='Single quoted',style='Action.TButton',
        command=lambda:email_controller.view_next_single('quoted'))
        single_quoted.grid(column=5,row=6,sticky=(N,S,E,W))
        single_customer = ttk.Button(welcome_frame, text='Single customer',style='Action.TButton',
        command=lambda:email_controller.view_next_single('customer'))
        single_customer.grid(column=6,row=6,sticky=(N,S,E,W))
        single_partner = ttk.Button(welcome_frame, text='Single partner',style='Action.TButton',
        command=lambda:email_controller.view_next_single('partner'))
        single_partner.grid(column=7,row=6,sticky=(N,S,E,W))
        holiday_button = ttk.Button(welcome_frame,text='Holiday message',style='Action.TButton',
        command=lambda:email_controller.view_holiday_email('customer'))
        holiday_button.grid(column=6,row=7,sticky=(N,S,E,W))
        info_button = ttk.Button(welcome_frame,text='Info',
        command=lambda:self.About_Software())
        info_button.grid(column=7,row=7,sticky=(N,S,E,W))
#        test_button = ttk.Button(welcome_frame, text='Test',
#        command=lambda:self.test_func())
#        test_button.grid(column=7,row=8,sticky=(N,S,E,W))
        self.canvas = Canvas(welcome_frame,width=600,height=400)
        self.canvas.grid(column=1,row=11,columnspan=4)
        self.myimg = PhotoImage(file='newLogo.gif',height=386,width=500)
        self.canvas.create_image(295,200,image=self.myimg,anchor='center')
        root.protocol("WM_DELETE_WINDOW", self.close_db)
        
    def About_Software(self):
        """Software information with Github and website links"""
        messagebox.showinfo(title="About",message=f"Thank you for using this software.",detail=f"More information can be found at the following links:\n\n{self.GITHUB_PAGE}\n\n{self.WEBSITE}")
        
#    def test_func(self):
#        print('test')
#        print(settings.ALL_SUBJECTS)

    def close_db(self):
        """Close SQLite DB connection."""
        sqlite_db_controller.close()
        messagebox.showinfo(message='DB closed.',detail='Program will be closed.')
        root.destroy()
        
    def update_user(self):
        """update user method"""
        try:
            user_data = sqlite_db_controller.get_user()
            if user_data == None:
                pass
            else:
                data = user_data.keys()
                user_info = Toplevel()
                user_info.title('User info')
                user_info.resizable(FALSE,FALSE)
                frame = ttk.Frame(user_info)
                frame.grid(column=0,row=0)
                display_user = Canvas(frame,height=675)
                display_user.grid(column=0,row=0)
                #scrollbar
                scrollbar = ttk.Scrollbar(frame,orient=VERTICAL,command=display_user.yview)
                scrollbar.grid(column=1,row=0,sticky=(NS))
                #configure canvas
                display_user.configure(yscrollcommand=scrollbar.set)
                display_user.bind('<Configure>',
                lambda e:display_user.configure(scrollregion=display_user.bbox("all")))
                #content frame
                content_frame = ttk.Frame(display_user,padding=(30,0,0,0))
                #add window to canvas
                display_user.create_window((0,0),window=content_frame)
                time_zone = StringVar()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                min_entry = Text(content_frame,width=5,height=1)
                min_entry.grid()
                min_entry.insert(1.0,user_data[0])
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                max_entry = Text(content_frame,width=5,height=1)
                max_entry.insert(1.0,user_data[1])
                max_entry.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                interval = Text(content_frame,width=5,height=1)
                interval.insert(1.0,user_data[2])
                interval.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                cbox = ttk.Combobox(content_frame,textvariable=time_zone,values=settings.TIME_ZONES)
                cbox.grid()
                cbox.set(user_data[3])
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                domain = Text(content_frame,width=30,height=1)
                domain.insert(1.0,user_data[4])
                domain.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                smtp = Text(content_frame,width=30,height=1)
                smtp.insert(1.0,user_data[5])
                smtp.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                port = Text(content_frame,width=5,height=1)
                port.insert(1.0,user_data[6])
                port.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                login = Text(content_frame,width=30,height=1)
                login.insert(1.0,user_data[7])
                login.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                password = Text(content_frame,width=30,height=1)
                password.insert(1.0,user_data[8])
                password.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                header = Text(content_frame,width=40,height=1)
                header.insert(1.0,user_data[9])
                header.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                unsub = Text(content_frame,width=30,height=1)
                unsub.insert(1.0,user_data[10])
                unsub.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                mail_list = Text(content_frame,width=15,height=1)
                mail_list.insert(1.0,user_data[11])
                mail_list.grid()
                mail_list['state'] = 'disabled'
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                first = Text(content_frame,width=15,height=1)
                first.insert(1.0,user_data[12])
                first.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                last = Text(content_frame,width=20,height=1)
                last.insert(1.0,user_data[13])
                last.grid()
                label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
                phone = Text(content_frame,width=15,height=1)
                phone.insert(1.0,user_data[14])
                phone.grid()
                button = ttk.Button(content_frame,text='update',
                command=lambda:[sqlite_db_controller.update_user(min_entry.get(1.0,'end'),max_entry.get(1.0,'end'),
                interval.get(1.0,'end'),time_zone.get(),domain.get(1.0,'end'),smtp.get(1.0,'end'),port.get(1.0,'end'),
                login.get(1.0,'end'),password.get(1.0,'end'),header.get(1.0,'end'),unsub.get(1.0,'end'),
                mail_list.get(1.0,'end'),first.get(1.0,'end'),last.get(1.0,'end'),phone.get(1.0,'end'))
                ,user_info.destroy()])
                button.grid()
        except Exception as e:
            messagebox.showerror(message='Error encountered.',
            detail=f'{e}')
        
    def upload_customers(self):
        """Method to upload customer data from csv file"""
        csv_file = filedialog.askopenfilename(filetypes=[("CSV",'*.csv')])
        if csv_file == () or csv_file == "":
            messagebox.showerror(message='You must select a csv file to utilize this option.')
        else:
            upload_csv = messagebox.askyesno(message='Are you sure you want to upload csv file?',
            detail='This will overwrite current customer data.',icon='question',title='Upload')
            if upload_csv == True:
                sqlite_db_controller.upload_csv(csv_file)
            else:
                messagebox.showinfo(message='Operation cancelled.',detail='No customers added.')
        
    def update_customer(self):
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
            data = customer.keys()
            customer_info = Toplevel()
            customer_info.title(f'Customer# {customer[0]} info')
            customer_info.resizable(FALSE,FALSE)
            frame = ttk.Frame(customer_info)
            frame.grid(column=0,row=0)
            display_customer = Canvas(frame,height=500)
            display_customer.grid(column=0,row=0)
            #scrollbar
            scrollbar = ttk.Scrollbar(frame,orient=VERTICAL,command=display_customer.yview)
            scrollbar.grid(column=1,row=0,sticky=(NS))
            #configure canvas
            display_customer.configure(yscrollcommand=scrollbar.set)
            display_customer.bind('<Configure>',
            lambda e:display_customer.configure(scrollregion=display_customer.bbox("all")))
            #content frame
            content_frame = ttk.Frame(display_customer,padding=(30,0,0,0))
            #add window to canvas
            display_customer.create_window((0,0),window=content_frame)
            status = StringVar()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            customer_id = Text(content_frame,width=6,height=1)
            customer_id.grid()
            customer_id.insert(1.0,customer[0])
            customer_id['state'] = 'disabled'
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            company = Text(content_frame,width=20,height=1)
            company.insert(1.0,customer[1])
            company.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            city = Text(content_frame,width=15,height=1)
            city.insert(1.0,customer[2])
            city.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            state = Text(content_frame,width=3,height=1)
            state.insert(1.0,customer[3])
            state.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            cbox = ttk.Combobox(content_frame,textvariable=status,values=settings.CUSTOMER_STATUS)
            cbox.grid()
            cbox.set(customer[4])
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            first = Text(content_frame,width=15,height=1)
            first.insert(1.0,customer[5])
            first.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            last = Text(content_frame,width=15,height=1)
            last.insert(1.0,customer[6])
            last.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            email = Text(content_frame,width=30,height=1)
            email.insert(1.0,customer[7])
            email.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            contact = Text(content_frame,width=10,height=1)
            contact.insert(1.0,customer[8])
            contact.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            notes = Text(content_frame,width=30,height=1)
            notes.insert(1.0,customer[9])
            notes.grid()
            button = ttk.Button(content_frame,text='update',
            command=lambda:[sqlite_db_controller.update_customer(customer_id.get(1.0,'end'),company.get(1.0,'end'),
            city.get(1.0,'end'),state.get(1.0,'end'),status.get(),first.get(1.0,'end'),last.get(1.0,'end'),
            email.get(1.0,'end'),contact.get(1.0,'end'),notes.get(1.0,'end')),customer_info.destroy()])
            button.grid()
        
    def delete_customer(self):
        """Where customer will be selected for deletion by customerID"""
        self.CUSTOMER_ID = IntVar()
        user_entry = Toplevel()
        user_entry.title('Enter customerID')
        label = ttk.Label(user_entry, text='Enter customerID:').pack()
        entry = ttk.Entry(user_entry,justify='center',width=5,textvariable=self.CUSTOMER_ID).pack()
        button = ttk.Button(user_entry,text=f'Submit',
        command=lambda:[sqlite_db_controller.delete_customer(self.CUSTOMER_ID.get()),user_entry.destroy()]).pack()
        
    def view_subjects(self):
        """View subjects in DB"""
        subjects = sqlite_db_controller.get_subjects()
        if subjects == None:
            pass
        else:
            result = ""
            for s in subjects:
                result += f"subjectID: {s.subjectID}\nCustomer: {s.subject_customer}\nSubject: {s.subject}\n\n"
            subject_display = Toplevel()
            subject_display.title('All subjects')
            subject_display.geometry('500x300-75-75')
            display_subjects = Text(subject_display,width=500,height=300)
            ys = ttk.Scrollbar(subject_display,orient='vertical',command=display_subjects.yview)
            display_subjects['yscrollcommand'] = ys.set
            display_subjects.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_subjects.insert(1.0,result)
            subject_display.grid_columnconfigure(0,weight=1)
            subject_display.grid_rowconfigure(0,weight=1)
        
    def delete_subject(self):
        """Delete subject by subjectID"""
        subject_id = IntVar()
        user_entry = Toplevel()
        user_entry.title('Enter subjectID')
        label = ttk.Label(user_entry, text='Enter subjectID:').pack()
        entry = ttk.Entry(user_entry,justify='center',width=5,textvariable=subject_id).pack()
        button = ttk.Button(user_entry,text=f'Submit',
        command=lambda:[sqlite_db_controller.delete_subject(subject_id.get()),user_entry.destroy()]).pack()
        
    def view_templates(self):
        """View email templates in DB"""
        templates = sqlite_db_controller.get_templates()
        if templates == None:
            pass
        else:
            result = ""
            for t in templates:
                result += f"emailbodyID: {t.emailbodyID}\nCustomer: {t.email_body_customer}\nEmail: {t.emailbody}\n\n"
            template_display = Toplevel()
            template_display.title('All email templates')
            template_display.geometry('1360x738')
            display_templates = Text(template_display,width=1360,height=738)
            ys = ttk.Scrollbar(template_display,orient='vertical',command=display_templates.yview)
            display_templates['yscrollcommand'] = ys.set
            display_templates.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_templates.insert(1.0,result)
            template_display.grid_columnconfigure(0,weight=1)
            template_display.grid_rowconfigure(0,weight=1)
        
    def delete_template(self):
        """Delete email template"""
        emailbody_id = IntVar()
        user_entry = Toplevel()
        user_entry.title('Enter emailbodyID')
        label = ttk.Label(user_entry, text='Enter emailbodyID:').pack()
        entry = ttk.Entry(user_entry,justify='center',width=5,textvariable=emailbody_id).pack()
        button = ttk.Button(user_entry,text=f'Submit',
        command=lambda:[sqlite_db_controller.delete_template(emailbody_id.get()),user_entry.destroy()]).pack()
        
    def view_footers(self):
        """View email footer templates in DB"""
        footers = sqlite_db_controller.get_footers()
        if footers == None:
            pass
        else:
            result = ""
            for f in footers:
                result += f"footerID: {f.footerID}\nHeadline: {f.headline}\nline1: {f.feature1}\nline2: {f.feature2}\nline3: {f.feature3}\nline4: {f.feature4}\nline5: {f.feature5}\nline6: {f.feature6}\nline7: {f.feature7}\nline8: {f.feature8}\n\n"
            footer_display = Toplevel()
            footer_display.title('All footer templates')
            footer_display.geometry('500x300-75-75')
            display_footers = Text(footer_display,width=500,height=300)
            ys = ttk.Scrollbar(footer_display,orient='vertical',command=display_footers.yview)
            display_footers['yscrollcommand'] = ys.set
            display_footers.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_footers.insert(1.0,result)
            footer_display.grid_columnconfigure(0,weight=1)
            footer_display.grid_rowconfigure(0,weight=1)
        
    def update_footer(self):
        """Update email footer template in DB"""
        self.FOOTER_ID = IntVar()
        user_entry = Toplevel()
        user_entry.title('Enter footerID')
        label = ttk.Label(user_entry, text='Enter footerID:').pack()
        entry = ttk.Entry(user_entry,justify='center',width=5,textvariable=self.FOOTER_ID).pack()
        button = ttk.Button(user_entry,text=f'Submit',command=lambda:[self.print_footer(),
        user_entry.destroy()]).pack()
        
    def print_footer(self):
        """This is where single footer information will be displayed for updates"""
        footer = sqlite_db_controller.get_byFooterID(self.FOOTER_ID.get())
        if footer == None:
            messagebox.showerror(message='no footer with that ID exist in DB')
        else:
            self.NEW_DATA = StringVar()
            data = footer.keys()
            f_info = Toplevel()
            f_info.title(f'Footer# {self.FOOTER_ID.get()} info')
            f_info.resizable(FALSE,FALSE)
            frame = ttk.Frame(f_info)
            frame.grid(column=0,row=0)
            display_footer = Canvas(frame,height=500)
            display_footer.grid(column=0,row=0)
            #scrollbar
            scrollbar = ttk.Scrollbar(frame,orient=VERTICAL,command=display_footer.yview)
            scrollbar.grid(column=1,row=0,sticky=(NS))
            #configure canvas
            display_footer.configure(yscrollcommand=scrollbar.set)
            display_footer.bind('<Configure>',
            lambda e:display_footer.configure(scrollregion=display_footer.bbox("all")))
            #content frame
            content_frame = ttk.Frame(display_footer,padding=(30,0,0,0))
            #add window to canvas
            display_footer.create_window((0,0),window=content_frame)
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            footer_id = Text(content_frame,width=3,height=1)
            footer_id.grid()
            footer_id.insert(1.0,footer[0])
            footer_id['state'] = 'disabled'
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            headline = Text(content_frame,width=30,height=1)
            headline.insert(1.0,footer[1])
            headline.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            feature1 = Text(content_frame,width=30,height=1)
            feature1.insert(1.0,footer[2])
            feature1.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            feature2 = Text(content_frame,width=30,height=1)
            feature2.insert(1.0,footer[3])
            feature2.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            feature3 = Text(content_frame,width=30,height=1)
            feature3.insert(1.0,footer[4])
            feature3.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            feature4 = Text(content_frame,width=30,height=1)
            feature4.insert(1.0,footer[5])
            feature4.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            feature5 = Text(content_frame,width=30,height=1)
            feature5.insert(1.0,footer[6])
            feature5.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            feature6 = Text(content_frame,width=30,height=1)
            feature6.insert(1.0,footer[7])
            feature6.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            feature7 = Text(content_frame,width=30,height=1)
            feature7.insert(1.0,footer[8])
            feature7.grid()
            label = ttk.Label(content_frame,text=f'{data.pop(0)}').grid()
            feature8 = Text(content_frame,width=30,height=1)
            feature8.insert(1.0,footer[9])
            feature8.grid()
            button = ttk.Button(content_frame,text='update',
            command=lambda:[sqlite_db_controller.update_footer(footer_id.get(1.0,'end'),headline.get(1.0,'end'),
            feature1.get(1.0,'end'),feature2.get(1.0,'end'),feature3.get(1.0,'end'),feature4.get(1.0,'end'),
            feature5.get(1.0,'end'),feature6.get(1.0,'end'),feature7.get(1.0,'end'),feature8.get(1.0,'end')),
            f_info.destroy()])
            button.grid()
        
    def delete_footer(self):
        """Delete email footer template"""
        footer_id = IntVar()
        user_entry = Toplevel()
        user_entry.title('Enter footerID')
        label = ttk.Label(user_entry, text='Enter footerID:').pack()
        entry = ttk.Entry(user_entry,justify='center',width=5,textvariable=footer_id).pack()
        button = ttk.Button(user_entry,text=f'Submit',
        command=lambda:[sqlite_db_controller.delete_footer(footer_id.get()),user_entry.destroy()]).pack()
        
    def view_bad_domains(self):
        """View bad domains in DB"""
        bad_domains = sqlite_db_controller.get_bad_domains()
        if bad_domains == None:
            pass
        else:
            result = ""
            for bd in bad_domains:
                result += f"emailcheckID: {bd.emailcheckID}\ndomain: {bd.domain}\n\n"
            bd_display = Toplevel()
            bd_display.title('Bad email domains')
            bd_display.geometry('500x300-75-75')
            display_bad_domains = Text(bd_display,width=500,height=300)
            ys = ttk.Scrollbar(bd_display,orient='vertical',command=display_bad_domains.yview)
            display_bad_domains['yscrollcommand'] = ys.set
            display_bad_domains.grid(column=0,row=0)
            ys.grid(column=1,row=0,sticky=(N,S))
            display_bad_domains.insert(1.0,result)
            bd_display.grid_columnconfigure(0,weight=1)
            bd_display.grid_rowconfigure(0,weight=1)
        
    def delete_bad_domain(self):
        """Delete bad domain"""
        emailcheck_id = IntVar()
        user_entry = Toplevel()
        user_entry.title('Enter emailcheckID')
        label = ttk.Label(user_entry, text='Enter emailcheckID:').pack()
        entry = ttk.Entry(user_entry,justify='center',width=5,textvariable=emailcheck_id).pack()
        button = ttk.Button(user_entry,text=f'Submit',
        command=lambda:[sqlite_db_controller.delete_emailcheck(emailcheck_id.get()),user_entry.destroy()]).pack()
    
root = Tk()
MainGUI(root)
root.mainloop()
