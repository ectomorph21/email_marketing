CONTENTS OF THIS FILE
---------------------

 * Introduction *
This program is the start of a gui program to allow users to send marketing emails to known clients or prospect clients.

 * Requirements *
-current python
-tkinter module
-pytz (for proper time conversion of date header)

 * Installation *
No installation required. Simply place all files in single directory, open terminal and ensure you are in the directory. Depending on your OS, use python command and file name with extension (example linux terminal "python3 main.py").

 * Configuration *
As the program stands, users must populate respective customer_list_test.csv file, and upload it using the Create SQLite DB button in the program. Program requires user to have access to smtp server for sending email (yahoo, Gmail, etc.). If using proprietary email server, must ensure dkim, dmarc, PTR (reverse domain), and spf records are valid. This will ensure highest probability of emails being received and not marked as spam. https://www.mail-tester.com/ is another site users can use to increase receive rate, and avoid being marked as spam. A score of 10 is the goal. User settings, and email templates reside in user_settings.json file.

 * Troubleshooting *
Use debug server in order to troubleshoot format or email issues (python3 -m smtpd -c DebuggingServer -n localhost:1025). Test, test, test! Use the debug server to get your email templates just right, before sending live emails.  

* File Directory *
-create_sqlite_db.py (for creating Sqlite DB from user upload of csv)
-customer_list_test.csv (template for user upload of data)
-main.py (main controller)
-objects.py (customer and email classes)
-README.txt
-sqlite_db_controller.py (controller for DB actions)
-user_settings.json (for user settings)

 * Notes *
-tables in SQLite DB
Customer
-future schema changes
User_Setting
Customer (FK - User_Setting)
Email_Template (FK - User_Setting)
Signature_Template ? (FK - User_Setting)
Email_Check ? (FK - User_Setting)

 * Maintainers *
- Ron Stephenson
- and anyone else interested in contributing
