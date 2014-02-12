import smtplib
import os

import imaplib
from gmail_imap import gmail_imap


def connect(username='barangeraward', password='PASSWORD_GOES_HERE'):
    global gmail
    gmail = gmail_imap.gmail_imap(username, password)
    gmail.login()
    gmail.mailboxes.load()
    
def disconnect():
    global gmail
    gmail.logout()

def folder_exists(folder):
    global gmail
    return folder in gmail.mailboxes

def get_emails(folder):
    global gmail
    
    gmail.messages.process(folder)
    
    messages = []
    for msg in gmail.messages:
        message = gmail.messages.getMessage(msg.uid)
        if 'barangeraward@gmail.com' in message.From: continue
        messages.append(message)
    
    return messages

if __name__ == '__main__':
    connect()
    
    msgs = get_emails('2013-Karimi')
    for m in msgs:
        print m.date
        print m.timestamp
    
    disconnect()
