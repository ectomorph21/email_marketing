CONTENTS OF THIS FILE
---------------------

 * Introduction *
This program is the start of a gui program to allow users to send marketing emails to known clients or prospect clients.

 * Requirements *
-current python
-tkinter module
-pytz (for proper time conversion of date header)
Time zone set to US/Eastern in MarketingEmail class. Will have to change to user's respective time zone.

 * Installation *
No installation required. Simply place all files in single directory, open terminal and ensure you are in the directory. Depending on your OS, use python command and file name with extension (example linux terminal "python3 main.py").

 * Configuration *
As the program stands, users must populate respective customer_list_test.csv file, and upload it using the Create SQLite DB button in the program. Program requires user to have access to smtp server for sending email (yahoo, Gmail, etc.). If using proprietary email server, must ensure dkim, dmarc, PTR (reverse domain), and spf records are valid. This will ensure highest probability of emails being received and not marked as spam. https://www.mail-tester.com/ is another site users can use to increase receive rate, and avoid being marked as spam. A score of 10 is the goal. User settings, and email templates reside in user_settings.json file. Email templates are sent in plain text format, with newlines (\n) to create the necessary line breaks. HTML emails and adding attachments features may be added in future releases.

* Use *
Program is functional and autoupdates last_contact column as emails are sent. "Export DB to CSV" feature allows contents of the database to be saved to respective csv with date stamp. Create, update, and delete functionality are in development. Most efficient way to update large amounts of data quickly is to update exported csv file and reload or create DB from that updated csv file. The notes column in the customers table is used as a boolean to prevent emails being sent to customers who have opted out.

 * Troubleshooting *
Use debug server in order to troubleshoot format or email issues (python3 -m smtpd -c DebuggingServer -n localhost:1025). Test, test, test! Use the debug server to get your email templates just right, before sending live emails. Program has been tested on Debian Buster OS, and Windows 10.

* File Directory *
-alt_main.py (used for secondary type of recipient or mailing list)
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
-potential future schema changes
User_Setting
Customer (FK - User_Setting)
Email_Template (FK - User_Setting)
Signature_Template ? (FK - User_Setting)
Email_Check ? (FK - User_Setting)
-pyinstaller for executable?

 * Maintainers *
- Ron Stephenson
- and anyone else interested in contributing

 * License notes *
Users are free to use code for legitimate business or personal usage. Not intended to be used for criminal activity.
