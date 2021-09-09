CONTENTS OF THIS FILE
---------------------

 * Introduction *
This program is a gui program to allow users to send marketing emails to customers or contacts.

 * Requirements *
-current python
-tkinter module
-pytz (for proper time conversion of date header)

 * Installation *
No installation required. Simply place all files in single directory, open terminal and ensure you are in the directory. Depending on your OS, use python command and file name with extension (example linux terminal "python3 main.py").

 * Configuration *
As the program stands, users can populate respective customer_list_test.csv file, and upload it using the "Upload customers" button in the program. Or they can choose to input customers manually. Program requires user to have access to smtp server for sending email (yahoo, Gmail, etc.). If using proprietary email server, must ensure dkim, dmarc, PTR (reverse domain), and spf records are valid. This will ensure highest probability of emails being received and not marked as spam. https://www.mail-tester.com/ is another site users can use to increase receive rate, and avoid being marked as spam. A score of 10 is the goal. User settings, email subjects, templates, footers, and domain checks are all maintained as separate tables in respective SQLite database. Email templates are sent in plain text format, with newlines (\n) to create the necessary line breaks. HTML emails and adding attachments features may be added in future releases.

* Use *
Program is functional and autoupdates last_contact column as emails are sent. "Export customers" feature allows contents of the Customer table to be saved to respective csv with date stamp. Create, update, and delete functionality have been provided for all tables. Most efficient way to update large numbers of customers quickly is to update exported csv file and reload that file. The removed customer status ensures emails will not be sent to those not wishing to be contacted. For best performance, all tables should have at least one data object created to ensure emails are sent correctly.

 * Troubleshooting *
Use debug server in order to troubleshoot format or email issues (python3 -m smtpd -c DebuggingServer -n localhost:1025). Test, test, test! Use the debug server to get your email templates just right, before sending live emails. Program has been tested on Debian Buster OS, and Windows 10.

* File Directory *
-create_sqlite_db.py (for creating Sqlite DB from user data input)
-customer_list_test.csv (template for user upload of data)
-email_controller.py (email control functions)
-load_settings.py (load settings from SQLite DB chosen)
-main.py (main controller)
-objects.py (all class objects for DB control)
-settings.py (global settings/variables)
-sqlite_db_controller.py (controller for DB actions)

 * Notes *
-tables in SQLite DB
User,Customer,Subject,EmailBody,Footer,EmailCheck
? pyinstaller for executable ?

 * Maintainers *
- Ron Stephenson
- and anyone else interested in contributing

 * License notes *
Users are free to use code for legitimate business or personal usage. Not intended to be used for criminal activity.
