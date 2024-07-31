#author: Sang Do connect to mailbox and send the data to webhook
import imaplib
import email
import smtplib
import requests

def forward_yahoo_to_http(yahoo_email, yahoo_password, http_endpoint):
    # IMAP connection
    imap = imaplib.IMAP4_SSL("imap.mail.yahoo.com", 993)
    imap.login(yahoo_email, yahoo_password)
    imap.select("INBOX")

    # Fetch emails (replace with your desired criteria)
    status, data = imap.search(None, 'FROM', 'hello@yyy.org')
    mail_ids = data[0].split()
#     print('-----')
#     print(mail_ids)
#     print('-----')
    for num in mail_ids:
        status, data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        # Extract email data (sender, recipient, subject, body, attachments)
        sender = msg['From']
        subject = msg['Subject']
        body = msg.get_payload(decode=True) #.decode('utf-8')
        email_data = {
            'from': msg['From'],
            'subject': msg['Subject']
        }
        print(email_data)
        # Send data to HTTP endpoint
        response = requests.post(http_endpoint, data=email_data)
        print(response.status_code)

        # Mark email as read (optional)
        imap.store(num, '+FLAGS', '\\Seen')

    imap.close()
    imap.logout()

if __name__ == "__main__":
    yahoo_email = "xxx@yahoo.com"
    yahoo_password = "" #generated in Yahoo mail setting
    http_endpoint = "https://fb-test.knorex.com/cron/health-check"

    forward_yahoo_to_http(yahoo_email, yahoo_password, http_endpoint)
