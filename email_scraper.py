import os, sys
import imaplib
import datetime

def email_scraper(server, uname, pwd):
    username = uname
    password = pwd
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select('folder_name')
    try:
        result, data = mail.uid('search', None, '(UNSEEN)')#new email
        inbox_item_list = data[0].split()
        most_recent = inbox_item_list[-1]
        result2, email_data = mail.uid('fetch', most_recent, '(RFC822)')#recent email
        raw_email = email_data[0][1].decode("UTF-8")
        email_message = email.message_from_string(raw_email)
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        i = data[0].split()[-1]
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

        if email_message.is_multipart():
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" % (str(local_date.strftime("%d/%m/%Y %H:%M:%S")))
            email_from = str(email_message['From'])
            email_to = str(email_message['To'])
            subject = str(email_message['Subject'])
            Index = str(i)

            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)

            file_name = "email_" + str(i) + ".txt"
            output_file = open(file_name, 'w', encoding='utf-8', errors='ignore')
            output_file.write("\n '%s' \n  '%s' \n\n \n\n'%s'" % (subject, local_message_date, body.decode('utf-8')))
            output_file.close()
    except IndexError:
        print("no new emails")

while True:
    email_scraper("email_provider(eg. gmail, outlook)", "username", "password")
    schedule.run_pending()
    time.sleep(60)