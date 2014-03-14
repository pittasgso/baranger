#!/bin/bash
import MySQLdb as mdb
import sys, os
import argparse
from string import Template
from time import sleep
try:
    from python_tools import beep
except:
    def beep():
        pass

import get_letters

SHOW_CONTACT = False
GMAIL_LABEL_FORMAT = '2014/%(lastName)s'

con = None

html_index = '''<html>
<head>
    <title>Index Page for Review Material</title>
</head>
<body>
    <ol>
    %(list)s
    </ol>
</body>
</html>
'''
html_index_entry = '%(firstName)s %(lastName)s (%(department)s)'

html_page = '''<html>
<head>
    <title>Review Material for $firstName $lastName</title>
    <style type='text/css'>
        div.header { margin-bottom:0.5ex; font-size:large; font-weight:bold; }
    </style>
</head>
<body>
    <div style='padding-bottom:1ex;padding-top:1ex;'>
        <div class='header'>Basic Information</div>
        <div>Name: $firstName $lastName</div>
        <div>Department: $department</div>
        <div>Years of study: $yearsOfStudy</div>
        %(contactInfo)s
    </div>
    <hr/>
    <div style='padding-bottom:1ex;padding-top:1ex;'>
        <div class='header'>Teaching Philosophy</div>
        <div>$teachingPhilosophy</div>
    </div>
    <hr/>
    <div style='padding-bottom:1ex;padding-top:1ex;'>
        <div class='header'>Teaching Challenge</div>
        <div>$teachingChallenge</div>
    </div>
    <hr/>
    <div style='padding-bottom:1ex;padding-top:1ex;'>
        <div class='header'>Example of Teaching Material and Reflection on it</div>
        <div>Teaching Material: $exampleOfWrittenTeachingMaterialContent</div>
        <div>$teachingReflection</div>
    </div>
    <hr/>
    <div style='padding-bottom:1ex;padding-top:1ex;'>
        <div class='header'>OMET Evaluations</div>
        <div>First Evaluation: $ometEvaluation1Content</div>
        <div>Second Evaluation: $ometEvaluation2Content (optional)</div>
    </div>
    <hr/>
    <div style='padding-bottom:1ex;padding-top:1ex;'>
        <div class='header'>Course Information</div>
        $courseInfo
    </div>
    <hr/>
    <div style='padding-bottom:1ex;padding-top:1ex;'>
        <div class='header'>Letters of Support</div>
        <div>Writer 1: $writer1Info</div>
        <div>Writer 2: $writer2Info</div>
        <div>Writer 3 (optional): $writer3Info</div>
        $letters
    </div>
</body>
</html>
'''

html_contact='''<div>Email address: <a href='mailto:$pittUsername'>$pittUsername</a></div>
        <div>On Campus Address: <pre>$onCampusAddress</pre></div>
        <div>Off Campus Address: <pre>$offCampusAddress</pre></div>
        <div>Phone Number: <pre>$phoneNumber</pre></div>'''

html_courseinfo = '''<div style='font-weight:bold;'>Course #%(count)s</div>
        <ol>
            <li>Department: %(dept)s</li>
            <li>Course Number: %(num)s</li>
            <li>Course Role: %(role)s</li>
            <li>Number of sections responsible for: %(sections)s</li>
            <li>Number of Students: %(stucount)s</li>
            <li>OMET Score: %(omet)s</li>
        </ol>'''

html_email = '''<html>
<head>
</head>
<body>
    <div><b>From:</b> %(from)s</div>
    <div><b>Subject:</b> %(subject)s</div>
    <div><b>Time:</b> %(timestamp)s</div>
    <hr/>
    <div>%(body)s</div>
    <hr/>
    %(attachments)s
</body>
</html>
'''

def generate_content(row, top_output_dir, skip_if_exists=False):
    #create the output directory
    username = row['pittUsername'].split('@')[0]
    output_dir = os.path.join(top_output_dir, username)
    relative_dir = os.path.join(username)
    if not os.path.exists(output_dir):
        print 'making', output_dir
        os.mkdir(output_dir)
    elif skip_if_exists:
        return os.path.join(relative_dir, 'index.html')
    
    #properly format the free-response area
    for field in ('teachingPhilosophy', 'teachingChallenge', 'teachingReflection'):
        if row[field] is not None:
            value = row[field].decode('utf-8')
            value = value.splitlines()
            value = '<br/>'.join(value)
            value = value.encode('ascii', 'xmlcharrefreplace')
            row[field] = value
    
    #save each of the uploaded files
    for field in ('exampleOfWrittenTeachingMaterial', 'ometEvaluation1', 'ometEvaluation2'):
        if row[field] is None:
            row[field+'Content'] = "Not submitted"
            continue
        
        #save file:
        content = row[field]
        header, content = content.split('\n', 1)
        size, mimetype, filename = header.split('|')
        output_filename = os.path.join(output_dir, filename)
        outfile = open(output_filename, 'w')
        outfile.write(content)
        outfile.close()
        
        row[field+'Content'] = "<a href='"+filename+"'>"+filename+"</a>"
    
    #Letters of Support
    letter_writers = {}
    for i in ('1', '2', '3'):
        row['writer'+i+'Info'] = '%s, %s' % (row['letterOfSupportSenderName'+i], row['letterOfSupportSenderRelationship'+i])
        letter_writers[i] = (row['letterOfSupportSenderName'+i], row['letterOfSupportSenderEmail'+i])
    row['otherEmails'] = ''
    
    letters = []
    label = GMAIL_LABEL_FORMAT % row
    if not get_letters.folder_exists(label):
        if row['letterOfSupportSenderEmail1'] + row['letterOfSupportSenderEmail2'] + row['letterOfSupportSenderEmail3'] == '':
            #no letter writers entered
            label = ''
        else:
            #they entered letter writers
            beep()
            label = raw_input('Folder not found for '+row['firstName']+' '+row['lastName']+' (appID='+row['appID']+').\nPlease enter true label: ')
    if label == '':
        emails = []
    else:
        emails = get_letters.get_emails(label)
    for email in emails:
        if email.From == row['pittUsername']: continue
        email_output_dir = os.path.join(output_dir, str(email.timestamp))
        if not os.path.exists(email_output_dir):
            #create the email's folder if it doesn't exist
            os.mkdir(email_output_dir)
        email_rel_dir = str(email.timestamp)
        
        attachments = []
        for a in email.attachments:
            afn = os.path.join(email_output_dir, a[0])
            outfile = open(afn, 'w')
            outfile.write(a[1])
            outfile.close()
            attachments.append(a[0])
        
        if len(attachments) == 0:
            attachments = ''
        else:
            attachments = ['<li><a href="%s">%s</a></li>' % (a, a) for a in attachments]
            attachments = '\n'.join(attachments)
            attachments = 'Attachments:<ul>' + attachments + '</ul>'
        
        content = html_email % {'from' : email.From, 'subject' : email.Subject, 'body' : email.Body, 'timestamp' : email.date, 'attachments' : attachments}
        
        output_filename = os.path.join(email_output_dir, 'index.html')
        
        outfile = open(output_filename, 'w')
        outfile.write(content)
        outfile.close()
        letters.append('<li><a href="'+os.path.join(email_rel_dir, 'index.html')+'">'+email.From+', '+email.date+'</a></li>')
    row['letters'] = '\n'.join(letters)
    
    #Course Info.
    cur = con.cursor()
    courseinfo = []
    for i in range(1, 7):
        sql = 'SELECT courseDepartment%(i)d, courseNumber%(i)d, courseStudentCount%(i)d, courseLabsRecitationsStudentWasResponsibleFor%(i)d, courseRole%(i)d, courseOmet%(i)d FROM teachingawardstudent WHERE appID="%(appID)s"' % {'i' : i, 'appID' : row['appID']}
        cur.execute(sql)
        cirow = cur.fetchone()
        
        if cirow[0] == '' and cirow[1] == '': break
        
        html_ci = html_courseinfo % {'count' : i, 'dept' : cirow[0], 'num' : cirow[1], 'role' : cirow[4], 'sections' : cirow[3], 'stucount' : cirow[2], 'omet' : cirow[5]}
        courseinfo.append(html_ci)
    row['courseInfo'] = '\n<br/>\n'.join(courseinfo)
    
    
    #generate index.html
    if SHOW_CONTACT: html = html_page % {'contactInfo' : html_contact}
    else: html = html_page % {'contactInfo' : ''}
    
    html = Template(html)
    output = html.safe_substitute(**row)
    
    #write the html file
    output_filename = os.path.join(output_dir, 'index.html')
    outfile = open(output_filename, 'w')
    outfile.write(output)
    outfile.close()
    
    #return the index file (relative to the main index.html)
    return os.path.join(relative_dir, 'index.html')

def main(db_hostname, db_username, db_password, database, email_username, email_password, top_output_dir='review'):
    skip_student_if_exists=False
    global con
    con = mdb.connect(db_hostname, db_username, db_password, database)
    cur = con.cursor(mdb.cursors.DictCursor)
    
    get_letters.connect(email_username, email_password)
    
    if not os.path.exists(top_output_dir):
        print 'making', top_output_dir
        os.mkdir(top_output_dir)
    
    cur.execute("SELECT appID, firstName, lastName, pittUsername, department, yearsOfStudy, onCampusAddress, offCampusAddress, phoneNumber, teachingPhilosophy, teachingChallenge, teachingReflection, exampleOfWrittenTeachingMaterial, ometEvaluation1, ometEvaluation2, letterOfSupportSenderName1, letterOfSupportSenderEmail1, letterOfSupportSenderRelationship1, letterOfSupportSenderName2, letterOfSupportSenderEmail2, letterOfSupportSenderRelationship2, letterOfSupportSenderName3, letterOfSupportSenderEmail3, letterOfSupportSenderRelationship3, submitted FROM teachingawardstudent")
    
    numrows = int(cur.rowcount)
    index_entries = []
    for i in range(numrows):
        row = cur.fetchone()
        print str(i+1)+'/'+str(numrows), row['appID'], row['lastName']
        output_filename = generate_content(row, top_output_dir, skip_if_exists=skip_student_if_exists)
        
        submitted = '' if row['submitted']==1 else '[not submitted]'
        index_entries.append((html_index_entry % row, output_filename, submitted))
    
    index_entries.sort()
    index_entries = ['<li style="padding-bottom:0.5ex;"><a href="%s">%s</a> %s</li>' % (i[1], i[0], i[2]) for i in index_entries]
    index_entries = '\n'.join(index_entries)
    html = html_index % {'list' : index_entries}
    
    outfile = open(os.path.join(top_output_dir, 'index.html'), 'w')
    outfile.write(html)
    outfile.close()
    
    get_letters.disconnect()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--email', '-e', help="Username of the email address the letters of recommendation are sent to.", default="barangeraward")
    parser.add_argument('--password', '-p', help="Password for the email address the letters of recommendation are sent to.", default="PASSWORD_GOES_HERE")
    parser.add_argument('--dbhostname', help="Hostname of the database", default="EWI-MYSQL-02.cssd.pitt.edu")
    parser.add_argument('--dbusername', help="Username for the database", default="asgsouser")
    parser.add_argument('--dbpassword', help="Password for the database", default="@$G$0U$3r")
    parser.add_argument('--dbdatabase', help="Database to use", default="asgso")
    
    
    args = parser.parse_args()
    try:
        print 'main', args
        # UNCOMMENT THE LINE BELOW WHEN READY TO GENERATE THE REVIEW FILES
        #main(args.dbhostname, args.dbusername, args.dbpassword, args.dbdatabase, args.email, args.password)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()
