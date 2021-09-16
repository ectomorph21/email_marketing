from random import *
from sqlite_db_controller import *
import sqlite_db_controller
import settings
from settings import *

def load_settings():
    """Load settings when connected to DB, and following create,update or delete functions"""
    user_data = sqlite_db_controller.get_user()
    settings.MIN_EMAIL = user_data[0]
    settings.MAX_EMAIL = user_data[1]
    settings.EMAIL_INTERVAL = user_data[2]
    settings.TIME_ZONE = user_data[3]
    settings.DOMAIN = user_data[4]
    settings.SMTP_SERVER = user_data[5]
    settings.PORT = user_data[6]
    settings.EMAIL_LOGIN = user_data[7]
    settings.EMAIL_PASSWORD = user_data[8]
    settings.FROM = user_data[9]
    settings.UNSUBSCRIBE = user_data[10]
    settings.MAILING_LIST = user_data[11]
    settings.SIGNATURE.append(user_data[12])
    settings.SIGNATURE.append(user_data[13])
    settings.SIGNATURE.append(user_data[14])
    settings.CALL_DATE = timedelta(days=settings.EMAIL_INTERVAL)
    settings.LIMIT.append(randint(settings.MIN_EMAIL,settings.MAX_EMAIL))
    bad_domains = sqlite_db_controller.get_bad_domains()
    for bd in bad_domains:
        settings.EMAIL_CHECK.append(bd.domain)
    subjects = sqlite_db_controller.get_subjects()
    for s in subjects:
        if s.subject_customer == 'prospect':
            settings.PROSPECT_SUBJECTS.append(s.subject)
            settings.ALL_SUBJECTS.append(s.subject)
        elif s.subject_customer == 'quoted':
            settings.QUOTED_SUBJECTS.append(s.subject)
            settings.ALL_SUBJECTS.append(s.subject)
        elif s.subject_customer == 'customer':
            settings.CUSTOMER_SUBJECTS.append(s.subject)
            settings.ALL_SUBJECTS.append(s.subject)
        elif s.subject_customer == 'target':
            settings.TARGET_SUBJECTS.append(s.subject)
            settings.ALL_SUBJECTS.append(s.subject)
        elif s.subject_customer == 'partner':
            settings.PARTNER_SUBJECTS.append(s.subject)
            settings.ALL_SUBJECTS.append(s.subject)
        else:
            settings.HOLIDAY_SUBJECTS.append(s.subject)
    settings.TARGET_SUBJECTS += settings.PROSPECT_SUBJECTS
    templates = sqlite_db_controller.get_templates()
    for t in templates:
        if t.email_body_customer == 'prospect':
            settings.PROSPECT_TEMPLATES.append(t.emailbody)
            settings.ALL_TEMPLATES.append(t.emailbody)
        elif t.email_body_customer == 'quoted':
            settings.QUOTED_TEMPLATES.append(t.emailbody)
            settings.ALL_TEMPLATES.append(t.emailbody)
        elif t.email_body_customer == 'customer':
            settings.CUSTOMER_TEMPLATES.append(t.emailbody)
            settings.ALL_TEMPLATES.append(t.emailbody)
        elif t.email_body_customer == 'target':
            settings.TARGET_TEMPLATES.append(t.emailbody)
            settings.ALL_TEMPLATES.append(t.emailbody)
        elif t.email_body_customer == 'partner':
            settings.PARTNER_TEMPLATES.append(t.emailbody)
            settings.ALL_TEMPLATES.append(t.emailbody)
        else:
            settings.HOLIDAY_TEMPLATES.append(t.emailbody)
    settings.TARGET_TEMPLATES += settings.PROSPECT_TEMPLATES
    footers = sqlite_db_controller.get_footers()
    for f in footers:
        settings.FOOTER.append(f)
        
def clear_settings():
    """Clear settings after create,update or delete functions"""
    settings.SIGNATURE.clear()
    settings.EMAIL_CHECK.clear()
    settings.PROSPECT_SUBJECTS.clear()
    settings.QUOTED_SUBJECTS.clear()
    settings.CUSTOMER_SUBJECTS.clear()
    settings.TARGET_SUBJECTS.clear()
    settings.PARTNER_SUBJECTS.clear()
    settings.HOLIDAY_SUBJECTS.clear()
    settings.ALL_SUBJECTS.clear()
    settings.PROSPECT_TEMPLATES.clear()
    settings.QUOTED_TEMPLATES.clear()
    settings.CUSTOMER_TEMPLATES.clear()
    settings.TARGET_TEMPLATES.clear()
    settings.PARTNER_TEMPLATES.clear()
    settings.HOLIDAY_TEMPLATES.clear()
    settings.ALL_TEMPLATES.clear()
    settings.FOOTER.clear()
    settings.LIMIT.clear()
