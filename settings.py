from sqlite_db_controller import *

USER_DATA = {
'min_email':'minimum emails to be sent',
'max_email':'maximum emails to be sent',
'email_interval':'email interval in days',
'time_zone':'your local time zone',
'domain':'your domain (i.e. facebook.com)',
'smtp_server':'smtp server (i.e. mail.facebook.com)',
'port':'port (i.e. 465 or 587)',
'email_login':'your email login',
'email_password':'your email password',
'from_header':'from header (i.e. John Doe - John Doe Inc <john@johndoeinc.com)',
'unsubscribe_email':'email you want unsubscribe emails to be directed to',
'mailing_list':'mailing list - database and other tables will be tied to this variable',
'first_name':'your first name',
'last_name':'your last name',
'phone':'your phone number'
}

CUSTOMER_FIELDS = ['customerID','company','city','state','status','first_name','last_name',
'email_address','last_contact','notes']

SUBJECT_FIELDS = ['subjectID','subject_customer','subject']

EMAILBODY_FIELDS = ['emailbodyID','email_body_customer','emailbody']

FOOTER_FIELDS = ['footerID','headline','feature1','feature2','feature3','feature4','feature5',
'feature6','feature7','feature8']

TIME_ZONES = ['US/Arizona', 'US/Central', 'US/Eastern', 'US/Hawaii', 'US/Mountain', 'US/Pacific']

CUSTOMER_STATUS = ['prospect','quoted','customer','target','partner','removed']

SUBJECT_CUSTOMER = ['prospect','quoted','customer','target','partner','holiday']

#user data pulled from SQLite DB, some defaults are in place, but change with user data
MIN_EMAIL = 1
MAX_EMAIL = 1
EMAIL_INTERVAL = 30
TIME_ZONE = 'US/Eastern'
DOMAIN = ''
SMTP_SERVER = ''
PORT = 465
EMAIL_LOGIN = ''
EMAIL_PASSWORD = ''
FROM = ''
UNSUBSCRIBE = ''
MAILING_LIST = ''
SIGNATURE = []
#list to check for bad domains and remaining email subjects, templates & footers
EMAIL_CHECK = []
PROSPECT_SUBJECTS = []
QUOTED_SUBJECTS = []
CUSTOMER_SUBJECTS = []
TARGET_SUBJECTS = []
PARTNER_SUBJECTS = []
HOLIDAY_SUBJECTS = []
ALL_SUBJECTS = []
PROSPECT_TEMPLATES = []
QUOTED_TEMPLATES= []
CUSTOMER_TEMPLATES = []
TARGET_TEMPLATES = []
PARTNER_TEMPLATES = []
HOLIDAY_TEMPLATES = []
ALL_TEMPLATES = []
FOOTER = []
#Additional variables required for emails        
CALL_DATE = timedelta(days=EMAIL_INTERVAL)        
#DATE = datetime.today()
LIMIT = []
SENT_LIST = []
