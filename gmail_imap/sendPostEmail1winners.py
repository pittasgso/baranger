#!/usr/bin/env python

import csv
import smtplib
import sys
import getpass

TESTING_EMAIL = 'timparenti+test@cs.pitt.edu'

password = ''

def sendPostNotificationEmail(applicantName, email, department):


    """ Based on http://segfault.in/2010/12/sending-gmail-from-python/ """
 
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
     
    sender = 'barangeraward@gmail.com'

    #Comment out this line to use the passed in recipient's email address.

    realEmail = email
    #email = TESTING_EMAIL
    subject = '2015 Elizabeth Baranger Excellence in Teaching Award'
    body = """Dear %s,

We are tremendously pleased to inform you that you have earned one of this
year's Elizabeth Baranger Excellence in Teaching Awards and a $250 prize
that will be added to your paycheck. Your commitment to teaching and
undergraduate education was evident through recommendations and student
evaluations, while your teaching materials offered superior principles of
pedagogy and methods of instruction. The entire Baranger Award committee
heartily congratulates you. We had many nominations this year for just seven
awards, so the competition was fierce, but your teaching materials were top
notch. Keep up the good work! It is clear that your students are learning a
lot, and enjoying it.
 
We also invite you to an awards luncheon to be held in your honor on Friday,
April 10, 2015 at 3:00pm at Lucca Ristorante, 317 S Craig St in Oakland.
Please let us know if you will be unable to attend. 
 
Again... our congratulations!
 
Sincerely,
 
The Elizabeth Baranger Excellence in Teaching Award Committee, 2014-2015
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

    try:
        sourceFile = sys.argv[1]
    except IndexError:
        sourceFile = 'applicants-winners.csv'

    csvIn = csv.reader(open(sourceFile, 'r'))

    #Skip first row
    header = csvIn.next()

    count = 0

    password = getpass.getpass()

    for row in csvIn:
        if len(row) == 0: continue
        
        if (row[READYTOSENDCOLUMN] in ['True','TRUE','1']):
            sendPostNotificationEmail(row[FIRSTNAMECOLUMN] + " " + row[LASTNAMECOLUMN], row[EMAILCOLUMN], row[DEPARTMENTCOLUMN])
        else:
            print 'Skipped: ', row[FIRSTNAMECOLUMN] + " " + row[LASTNAMECOLUMN]
        count = count + 1

#        if (count == 2):
#            sys.exit(0)

