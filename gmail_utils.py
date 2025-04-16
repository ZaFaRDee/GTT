# gmail_utils.py

from imapclient import IMAPClient
import pyzmail
from config import GMAIL_USERNAME, GMAIL_PASSWORD, GMAIL_FOLDER
from parser import parse_subject

def get_new_alerts():
    alerts = []
    with IMAPClient('imap.gmail.com', ssl=True) as server:
        server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        server.select_folder(GMAIL_FOLDER, readonly=False)
        messages = server.search(['UNSEEN', 'FROM', 'alerts@thinkorswim.com'])

        for uid, message_data in server.fetch(messages, ['RFC822']).items():
            email_message = pyzmail.PyzMessage.factory(message_data[b'RFC822'])
            subject = email_message.get_subject()
            tickers, algo_name = parse_subject(subject)
            if tickers and algo_name:
                alerts.append({'tickers': tickers, 'algo': algo_name})
            else:
                print(f"❌ Subject parsing failed: {subject}")
            server.add_flags(uid, ['\\Seen'])
    return alerts
