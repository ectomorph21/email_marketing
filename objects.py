import smtplib
import csv
import json
from datetime import *
from email.message import EmailMessage
from random import *
import pytz
from pytz import *

LETTERS = ['a','b','c','d','e','f']
DATE = datetime.today()

class MarketingEmail():
    def __init__(self,FROM,address,subject,domain,UNSUBSCRIBE,mailing_list,prev_cus,name,body,signature,footer):
        self.msg = EmailMessage()
        self.msg['From'] = FROM
        self.msg['To'] = address
        self.msg['Subject'] = subject
        self.time_zone = self.get_time_zone()
        self.msg["Date"] = self.time_zone
        self.domain = domain
        self.msg['Message-ID'] = self.format_message_id_header()
        self.unsubscribe = UNSUBSCRIBE
        self.mailing_list = mailing_list
        self.msg['List-Unsubscribe'] = self.format_list_unsubscribe_header()
        self.prev_cus = prev_cus
        self.name = name
        self.body = body
        self.signature = signature
        self.footer = footer
        
    def get_time_zone(self):
        default_time = datetime.now()
        eastern_tzinfo = pytz.timezone("US/Eastern")
        eastern_time = default_time.astimezone(eastern_tzinfo)
        return eastern_time
        
    def format_message_id_header(self):
        message_time = self.time_zone.strftime("%d-%m-%Y-%H-%M-%S%z")
        return f'<{LETTERS[randint(0,5)]}-'+str(randint(1000,9999))+'-'+message_time+f'@{self.domain}>'
        
    def get_greeting(self):
        if int(DATE.strftime('%H')) < 12:
            greet = 'Good morning'
        else:
            greet = 'Good afternoon'
        custom_greet = ['Hi', greet]
        if self.prev_cus != '':
            return custom_greet[randint(0,1)]
        else:
            return greet
        
    def format_list_unsubscribe_header(self):
        return f'<mailto:{self.unsubscribe}?subject=unsubscribe%20{self.mailing_list}%20list>'
        
    def send_test_email(self):
        self.msg.set_content(f"{self.get_greeting()} {self.name},\n\n{self.body}\n\n{self.signature}\n\n{self.footer}")
        with smtplib.SMTP('localhost',1025) as smtp:
            smtp.send_message(self.msg)
            
    def send_live_email(self,SMTP_SERVER,PORT,EMAIL_LOGIN,EMAIL_PASSWORD):
        self.msg.set_content(f"{self.get_greeting()} {self.name},\n\n{self.body}\n\n{self.signature}\n\n{self.footer}")
        with smtplib.SMTP_SSL(SMTP_SERVER,PORT) as smtp:
            smtp.login(EMAIL_LOGIN,EMAIL_PASSWORD)
            smtp.send_message(self.msg)
            
class Customer:
    def __init__(self,customerID=0,company=None,city=None,state=None,industry=None,previous_customer=None,quoted=None,
    website=None,first_name=None,last_name=None,email_address=None,last_contact=None,notes=None):
        self.customerID = customerID
        self.company = company
        self.city = city
        self.state = state
        self.industry = industry
        self.previous_customer = previous_customer
        self.quoted = quoted
        self.website = website
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.last_contact = last_contact
        self.notes = notes
            
