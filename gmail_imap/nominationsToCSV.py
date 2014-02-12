#!/usr/bin/env python

import csv

def FetchOneAssoc(cursor) :
    
    """ Return an associative array from an SQL query result.
    
    http://www.mouldy.org/a-quick-guide-to-using-mysql-in-python """

    data = cursor.fetchone()
    if data == None :
        return None
    desc = cursor.description

    dict = {}

    for (name, value) in zip(desc, data) :
        dict[name[0]] = value

    return dict

def getCSVRowFromEntry(entry):

    neededFields = ["NomineeFirstName", "NomineeLastName", "NomineeEmail", "NomineePhone", "NomineeDepartment", "ClassSemester", "ClassNumber", "ClassCRN", "ClassTitle", "ClassLab", "ClassStandAlone", "ClassOtherComments", "ContactAffliation", "OtherComments" ]

    return [entry[f] for f in neededFields]
   

def identicalFields(fieldName, entry1, entry2):
    entry1 = entry1[fieldName].strip()
    entry2 = entry2[fieldName].strip()

    return (entry1 != "" and entry2 != "" and entry1 == entry2)

def isDuplicate(entry, existingEntries):

    """ Return whether the entry already exists in the list of existing
    entries.  Entries with duplicate (non-empty) email addresses, and entries
    with the exact same name and department are considered as duplicates. """

    entryEmail = entry['NomineeEmail'].strip()

    for p in existingEntries:
        existingEmail = p['NomineeEmail'].strip()
        if (existingEmail == entryEmail and entryEmail != ""):
            return True

        if (identicalFields('NomineeFirstName', entry, p) and
            identicalFields('NomineeLastName', entry, p) and
            identicalFields('NomineeDepartment', entry, p)):

            if (entry["NomineeFirstName"] == "Beach"):
                pass
                print "Duplicate:",getCSVRowFromEntry(entry)
                pass

            return True

    return False

def processPublicitySources(entry,publicitySources):
    source = entry["NomineePublicitySource"]
    publicitySources.setdefault(source, 0)
    publicitySources[source] += 1

if __name__ == '__main__':
    import os

    try:
        if (os.environ['DEBUG'] == '1'):
            import pdb; pdb.set_trace()
    except KeyError:
        pass

    validNominationSources = ['database','csv']

    try:
        nominationSource = os.environ['source']
    except KeyError:
        nominationSource = 'database'

    assert(nominationSource in validNominationSources)

    desiredFields = ['First Name:','Last Name:', 'Email:', 'Phone Number:', 'Department:', 'Semester:', 'Number:', 'CRN:','Title:','Lab/Recitation:','ClassType:', 'Stand Alone:', 'Other:', 'Comment:', 'Nomination:', 'Comments:', 'Affiliation:' ]

    csvout = csv.writer(open('nominations.csv', 'wb'))
    csvout.writerow(desiredFields)

    if (nominationSource == "database"):

        existingEntries = []
        publicitySources = {}

        import MySQLdb

        db=MySQLdb.connect(host="mysql.cs.pitt.edu",user="pdillon",
            passwd="pd-gso",db="gso")

        cursor = db.cursor()

        query = cursor.execute("SELECT * FROM teachingAwardNomination")

        row = FetchOneAssoc(cursor)
        while (row != None):
            processPublicitySources(row, publicitySources)
            if (not isDuplicate(row, existingEntries)):
                existingEntries.append(row)

            row = FetchOneAssoc(cursor)

        for entry in existingEntries:
            csvout.writerow(getCSVRowFromEntry(entry))

        print 'Publicity Sources:'
        for k in sorted(publicitySources.keys()):
            print "%20s -> %5d" % (k,publicitySources[k])

    elif (nominationSource == "csv"):

        #Based on
        #http://verpa.wordpress.com/2010/01/23/python-gmail-imap-part-4/

        from gmail_imap import *

        headers = []
        needsHeaders = True
        
        gmail = gmail_imap('barangeraward@gmail.com','PASSWORD_GOES_HERE')

        gmail.mailboxes.load()
        #print gmail.mailboxes

        gmail.messages.process("[Gmail]/All Mail")
        #print gmail.messages

        for message_stub in gmail.messages:
            message = gmail.messages.getMessage(message_stub.uid)
        #	  print message
            if (message.Subject.find('Teaching Award') != -1): #A teaching award!
                row = []
                for line in message.Body.split("\n"):
                    for field in desiredFields:
                        if (line.find(field) == 0):
                            row.append(line[len(field):].strip())
                            if (needsHeaders):
                                headers.append(field.strip(":"))
                if (needsHeaders):
                    needsHeaders = False
                    csvout.writerow(headers)
                csvout.writerow(row)

        gmail.logout()

