import smtplib
import csv
from datetime import *
from email.message import EmailMessage
from random import *
import pytz
from pytz import *
from tkinter import messagebox
import settings
from settings import *

LETTERS = ['a','b','c','d','e','f']

class MarketingEmail():
    def __init__(self,address,subject,name,status,body):
        """Custom email class"""
        self.DATE = datetime.today()
        self.msg = EmailMessage()
        self.msg['From'] = settings.FROM
        self.msg['To'] = address
        self.msg['Subject'] = subject
        self.time_zone = self.get_time_zone()
        self.msg["Date"] = self.time_zone
        self.domain = settings.DOMAIN
        self.msg['Message-ID'] = self.format_message_id_header()
        self.unsubscribe = settings.UNSUBSCRIBE
        self.mailing_list = settings.MAILING_LIST
        self.msg['List-Unsubscribe'] = self.format_list_unsubscribe_header()
        self.name = name
        self.status = status
        self.body = body
        self.signature = self.get_signature()
        self.footer = ""
        #msg.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=file_name)
        
    def get_time_zone(self):
        """Time zone conversion for proper date header format"""
        default_time = datetime.now()
        tz_info = pytz.timezone(settings.TIME_ZONE)
        time_zone = default_time.astimezone(tz_info)
        return time_zone
        
    def format_message_id_header(self):
        """Formatting for message-id header"""
        message_time = self.time_zone.strftime("%d-%m-%Y-%H-%M-%S%z")
        return f'<{LETTERS[randint(0,5)]}-'+str(randint(1000,9999))+'-'+message_time+f'@{self.domain}>'
        
    def get_greeting(self):
        """Get greeting depending on time of day or customer status"""
        if int(self.DATE.strftime('%H')) < 12:
            greet = 'Good morning'
        else:
            greet = 'Good afternoon'
        custom_greet = ['Hi', greet]
        if self.status == 'customer' or self.status == 'partner':
            return custom_greet[randint(0,1)]
        else:
            return greet
        
    def format_list_unsubscribe_header(self):
        """Format for List-Unsubscribe header"""
        return f'<mailto:{self.unsubscribe}?subject=unsubscribe%20{self.mailing_list}%20list>'
        
    def get_signature(self):
        """Build signature from first, last and phone"""
        signature = ''
        signature += settings.SIGNATURE[0]+' '+settings.SIGNATURE[1]+'\n'
        signature += settings.SIGNATURE[2]+'\n'
        return signature
        
    def get_footer(self,build):
        """Build footer"""
        if settings.FOOTER == []:
            return ''
        elif build == 'bulk':
            footer = settings.FOOTER[randint(0,len(settings.FOOTER)-1)]
            string_var = ''
            string_var += footer.headline+'\n'
            string_var += footer.feature1+'\n'
            string_var += footer.feature2+'\n'
            string_var += footer.feature3+'\n'
            string_var += footer.feature4+'\n'
            string_var += footer.feature5+'\n'
            string_var += footer.feature6+'\n'
            string_var += footer.feature7+'\n'
            string_var += footer.feature8
            return string_var
        else:
            string_var = ''
            for f in settings.FOOTER:
                if f.headline == build:
                    footer = f
                    string_var += footer.headline+'\n'
                    string_var += footer.feature1+'\n'
                    string_var += footer.feature2+'\n'
                    string_var += footer.feature3+'\n'
                    string_var += footer.feature4+'\n'
                    string_var += footer.feature5+'\n'
                    string_var += footer.feature6+'\n'
                    string_var += footer.feature7+'\n'
                    string_var += footer.feature8
                    return string_var
        
    def send_test_email(self,build):
        """Method to send test emails on debug server"""
        if build == '':
            self.msg.set_content(f"{self.get_greeting()} {self.name},\n\n{self.body}\n\n{self.signature}\n{self.footer}")
        else:
            self.msg.set_content(f"{self.get_greeting()} {self.name},\n\n{self.body}\n\n{self.signature}\n{self.get_footer(build)}")
        with smtplib.SMTP('localhost',1025) as smtp:
            smtp.send_message(self.msg)
            
    def send_live_email(self,build):
        """Method to send live emails"""
        if build == '':
            self.msg.set_content(f"{self.get_greeting()} {self.name},\n\n{self.body}\n\n{self.signature}\n{self.footer}")
        else:
            self.msg.set_content(f"{self.get_greeting()} {self.name},\n\n{self.body}\n\n{self.signature}\n{self.get_footer(build)}")
        with smtplib.SMTP_SSL(settings.SMTP_SERVER,settings.PORT) as smtp:
            smtp.login(settings.EMAIL_LOGIN,settings.EMAIL_PASSWORD)
#            print(self.msg)#for testing live format
            smtp.send_message(self.msg)
    
class User:
    def __init__(self,min_email=None,max_email=None,email_interval=None,time_zone=None,domain=None,
    smtp_server=None,port=None,email_login=None,email_password=None,from_header=None,unsubscribe_email=None,
    mailing_list=None,first_name=None,last_name=None,phone=None):
        """User objects"""
        self.min_email = min_email
        self.max_email = max_email
        self.email_interval = email_interval
        self.time_zone = time_zone
        self.domain = domain
        self.smtp_server = smtp_server
        self.port = port
        self.email_login = email_login
        self.email_password = email_login
        self.from_header = from_header
        self.unsubscribe_email = unsubscribe_email
        self.mailing_list = mailing_list
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone            

class Customer:
    def __init__(self,customerID=0,company=None,city=None,state=None,status=None,
    first_name=None,last_name=None,email_address=None,last_contact=None,notes=None):
        """Customer objects"""
        self.customerID = customerID
        self.company = company
        self.city = city
        self.state = state
        self.status = status
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.last_contact = last_contact
        self.notes = notes
        
class Subject:
    def __init__(self,subjectID=0,subject_customer=None,subject=None):
        """Subject objects"""
        self.subjectID = subjectID
        self.subject_customer = subject_customer
        self.subject = subject
        
class EmailBody:
    def __init__(self,emailbodyID=0,email_body_customer=None,emailbody=None):
        """Email body objects"""
        self.emailbodyID = emailbodyID
        self.email_body_customer = email_body_customer
        self.emailbody = emailbody
        
class Footer:
    def __init__(self,footerID=0,headline=None,feature1=None,feature2=None,feature3=None,feature4=None,
    feature5=None,feature6=None,feature7=None,feature8=None):
        """Email footer objects"""
        self.footerID = footerID
        self.headline = headline
        self.feature1 = feature1
        self.feature2 = feature2
        self.feature3 = feature3
        self.feature4 = feature4
        self.feature5 = feature5
        self.feature6 = feature6
        self.feature7 = feature7
        self.feature8 = feature8
        
class EmailCheck:
    def __init__(self,emailcheckID=0,domain=None):
        """Email check objects for domain exclusion"""
        self.emailcheckID = emailcheckID
        self.domain = domain
       
