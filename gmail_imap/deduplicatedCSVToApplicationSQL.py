#!/usr/bin/env python


import csv
import random
import sys

# Is the first row a header for the data? (True = yes, False = no)
HAS_HEADER = True

# Column A is 0, B is 1, C is 2, ...
READYTOSENDCOLUMN = 0 #A
FIRSTNAMECOLUMN = 1 #B
LASTNAMECOLUMN = 2 #C
EMAILCOLUMN = 3 #D
DEPARTMENTCOLUMN = 4 #E

YEAR = '2015'

random.seed()

userIDs = []

def makeAppID(numDigits = 16):
    global userIDs
    possible = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    retVal = ''
    for i in range(0,numDigits):
        index = random.randint(0,len(possible)-1)
        retVal = retVal + possible[index:index+1]

    if (retVal in userIDs): #try again
        return makeAppID(numDigits)
    return retVal

def simpleEscape(fieldValue):
    fieldValue = fieldValue.replace('\'', '\\\'')
    return fieldValue

try:
    sourceFile = sys.argv[1]
except IndexError:
    sourceFile = 'data/'+YEAR+'/01-'+YEAR+'-nominations-dedup.csv'

reader = csv.reader(open(sourceFile, 'rb'))

try:
    outFile = sys.argv[2]
except IndexError:    
    outFile = 'data/'+YEAR+'/02-'+YEAR+'-nomination-listing.csv'

writer = csv.writer(open(outFile, 'w'))
writer.writerow(['ready to send','appID','First Name','Last Name', 'Email Address', 'Department', 'Personal Application URL'])


try:
    sqlFile = sys.argv[3]
except IndexError:
    sqlFile = 'data/'+YEAR+'/02-'+YEAR+'-injections.sql'

sql_injection_output = ''

if HAS_HEADER:
    header = reader.next()


for row in reader:
    appID = makeAppID()
    
    readytosend = (row[READYTOSENDCOLUMN] in ['TRUE', '1'])
    
    firstName = simpleEscape(row[FIRSTNAMECOLUMN])
    lastName = simpleEscape(row[LASTNAMECOLUMN])
    
    pittUsername = simpleEscape(row[EMAILCOLUMN])
    #Do they have an @ in their username? If so, do nothing. Otherwise, assume
    #it is a Pitt username and add the suffix.
    if '@' not in pittUsername:
        pittUsername += "@pitt.edu"

    department = simpleEscape(row[DEPARTMENTCOLUMN])
    
    #url = 'http://stage.asgso.pitt.edu/doku.php/teaching_award_application?appID='+appID
    url = 'http://asgso.pitt.edu/doku.php/teaching_award_application?appID='+appID
    #print 'INSERT INTO `asgso`.`teachingAwardStudent` (`appID`, `firstName`, `lastName`, `pittUsername`, `department`, `onCampusAddress`, `offCampusAddress`, `phoneNumber`, `letterOfSupportSenderName1`, `letterOfSupportSenderEmail1`, `letterOfSupportSenderRelationship1`, `letterOfSupportSenderName2`, `letterOfSupportSenderEmail2`, `letterOfSupportSenderRelationship2`, `letterOfSupportSenderName3`, `letterOfSupportSenderEmail3`, `letterOfSupportSenderRelationship3`, `courseDepartment1`, `courseNumber1`, `courseStudentCount1`, `courseLabsRecitationsStudentWasResponsibleFor1`, `courseRole1`, `courseOmet1`, `courseDepartment2`, `courseNumber2`, `courseStudentCount2`, `courseLabsRecitationsStudentWasResponsibleFor2`, `courseRole2`, `courseOmet2`, `courseDepartment3`, `courseNumber3`, `courseStudentCount3`, `courseLabsRecitationsStudentWasResponsibleFor3`, `courseRole3`, `courseOmet3`, `courseDepartment4`, `courseNumber4`, `courseStudentCount4`, `courseLabsRecitationsStudentWasResponsibleFor4`, `courseRole4`, `courseOmet4`, `courseDepartment5`, `courseNumber5`, `courseStudentCount5`, `courseLabsRecitationsStudentWasResponsibleFor5`, `courseRole5`, `courseOmet5`, `courseDepartment6`, `courseNumber6`, `courseStudentCount6`, `courseLabsRecitationsStudentWasResponsibleFor6`, `courseRole6`, `courseOmet6`, `teachingPhilosophy`, `teachingChallenge`, `teachingReflection`, `submitted`) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', NULL, NULL, NULL, \'0\');' % (appID, firstName, lastName, pittUsername, department)
    sql_injection_output += 'INSERT INTO `asgso`.`teachingAwardStudent` (`appID`, `firstName`, `lastName`, `pittUsername`, `department`) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\');\n' % (appID, firstName, lastName, pittUsername, department)
    #print 'INSERT INTO `asgso`.`teachingAwardStudent` (`appID`, `firstName`, `lastName`, `pittUsername`, `department`) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' % (appID, firstName, lastName, pittUsername, department)
    writer.writerow([readytosend, appID, firstName, lastName, pittUsername, department, url])

fout = open(sqlFile, 'w')
fout.write(sql_injection_output)
fout.close()
