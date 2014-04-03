#!/usr/bin/env python

import csv
import smtplib
import sys
import getpass

TESTING_EMAIL = 'timparenti+test@cs.pitt.edu'

password = ''

def sendNominationEmail(applicantName, email, department, link):


    """ Based on http://segfault.in/2010/12/sending-gmail-from-python/ """
 
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
     
    sender = 'barangeraward@gmail.com'

    #Comment out this line to use the passed in recipient's email address.

    realEmail = email
    #email = TESTING_EMAIL
    subject = '2013-2014 Elizabeth Baranger Excellence in Teaching Award'
    body = """Dear %s,

Thank you for submitting your application for the 2013-2014 Elizabeth 
Baranger Excellence in Teaching Award. Your nomination for the award is an 
honor in itself, indicating your dedication to the advancement of 
undergraduate education at the University of Pittsburgh. The graduate 
students nominated for this year's award represent a wide range of 
departments within Arts and Sciences and a diversity of roles held by 
graduate students including recitation leaders, teaching assistants and 
independent instructors.

With many nominees and after weeks of deliberation among both faculty 
members and graduate students, we regret to inform you that you were not 
among the few selected winners of this year's Baranger Teaching Award. Your 
dedication to teaching and your ability to create the passionate learning 
environment that we all desire for the University of Pittsburgh is highly 
admirable. We thank you for your excellent teaching, which has clearly made 
an impact. Keep up the good work, and we'll keep an eye out for your name 
next time nominations come around!

Please accept the Award Committee's best wishes for your continued success 
in research and teaching.

Sincerely,
 
The Elizabeth Baranger Excellence in Teaching Award Committee, 2013-2014
""" % (applicantName)
     
    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + email,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    headers = "\r\n".join(headers)
     
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
     
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, password)

    contents = headers + "\r\n\r\n" + body
     
    session.sendmail(sender, email, contents)
    print "session.sendmail(%s, %s, %s)" % (sender, email, "[...]")

    #print contents
    #print

    session.quit()

if __name__ == '__main__':
    import os

    READYTOSENDCOLUMN = 0
    FIRSTNAMECOLUMN = 2
    LASTNAMECOLUMN = 3
    EMAILCOLUMN = 4
    DEPARTMENTCOLUMN = 5

    LINKCOLUMN = 7

    try:
        sourceFile = sys.argv[1]
    except IndexError:
        sourceFile = 'nominations.csv'

    csvIn = csv.reader(open(sourceFile, 'r'))

    #Skip first row
    header = csvIn.next()

    count = 0

    password = getpass.getpass()

    for row in csvIn:
        if len(row) == 0: continue
        
        if (row[READYTOSENDCOLUMN] in ['True','TRUE','1']):
            sendNominationEmail(row[FIRSTNAMECOLUMN] + " " + row[LASTNAMECOLUMN], row[EMAILCOLUMN], row[DEPARTMENTCOLUMN], row[LINKCOLUMN])
        else:
            print 'Skipped: ', row[FIRSTNAMECOLUMN] + " " + row[LASTNAMECOLUMN]
        count = count + 1

#        if (count == 2):
#            sys.exit(0)

