#!/usr/bin/env python

import csv
import smtplib
import sys

TESTING_EMAIL = 'timparenti+test@cs.pitt.edu'

def sendNominationEmail(applicantName, email, department, link):


    """ Based on http://segfault.in/2010/12/sending-gmail-from-python/ """
 
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
     
    sender = 'barangeraward@gmail.com'
    password = 'PASSWORD_GOES_HERE'

    #Comment out this line to use the passed in recipient's email address.

    realEmail = email
    #email = TESTING_EMAIL
    subject = 'Nomination: Elizabeth Baranger Excellence in Teaching Award'
    body = """Dear %s,

Congratulations! You have been nominated to compete for the 2014
Elizabeth Baranger Excellence in Teaching Award for your teaching during
the 2013 calendar year. This annual award, sponsored by the University
of Pittsburgh's Arts & Sciences Graduate Student Organization, was
created to acknowledge and promote outstanding teaching by graduate
students at Pitt. Up to six awards of $250 each will be given out; two
each from the Natural Sciences, Social Sciences, and Arts and
Humanities. Your nomination is in itself an honor. It indicates that
your teaching has had a positive impact on students and/or colleagues
and you should be proud.

This award honors University of Pittsburgh Vice-Provost for Graduate
Studies and Professor of Physics Elizabeth Baranger. Throughout her
distinguished career, Professor Baranger worked tirelessly to improve
graduate education here at the University of Pittsburgh. We are a
crucial component of this work. Whether leading a recitation, lab, or
stand alone course, teaching provides our most public role in our
graduate education and academic career. This award allows the A&S GSO to
highlight & reward those graduate students who demonstrate excellence
and commitment to this important aspect of our academic system.

Each applicant has been assigned a unique online application page and
access code.  Your personal application page can be found by following
this link:

%s

Details of the application and required materials can be found on the
webpage listed above.  All application materials, including letters of
support, must be received by the end of the day on Friday, March 7,
2014.  Award announcements will be made on or about April 1. 

General information about the award can be found at:

http://asgso.pitt.edu/teachingawards/

If you have any questions or concerns about the application, please
contact barangeraward@gmail.com.  Congratulations again on your
nomination!

Sincerely,

The Elizabeth Baranger Excellence in Teaching Awards Committee
""" % (applicantName, link)
     
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

    for row in csvIn:
        if len(row) == 0: continue
        
        if (row[READYTOSENDCOLUMN] in ['True','TRUE','1']):
            sendNominationEmail(row[FIRSTNAMECOLUMN] + " " + row[LASTNAMECOLUMN], row[EMAILCOLUMN], row[DEPARTMENTCOLUMN], row[LINKCOLUMN])
        else:
            print 'Skipped: ', row[FIRSTNAMECOLUMN] + " " + row[LASTNAMECOLUMN]
        count = count + 1

#        if (count == 2):
#            sys.exit(0)

