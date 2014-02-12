#!/usr/bin/env python


import csv
import random
import sys

HAS_HEADER = False #is the first row a header for the data? (True = yes, False = no)

#Column A is 0, B is 1, C is 2, ...
READYTOSENDCOLUMN = 0 #A
NAMECOLUMN = 1 #B
EMAILCOLUMN = 2 #C
DEPARTMENTCOLUMN = 3 #D

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
    sourceFile = 'no_dups_nominations.csv'

reader = csv.reader(open(sourceFile, 'rb'))

try:
    outFile = sys.argv[2]
except IndexError:    
    outFile = 'application_listing.csv'

writer = csv.writer(open(outFile, 'w'))

writer.writerow(['ready to send','appID','First Name:','Last Name:', 'Pitt Email', 'Department', 'Phone Number', 'Personal Application URL'])

if HAS_HEADER:
    header = reader.next()

for row in reader:
    appID = makeAppID()
    
    readytosend = (row[READYTOSENDCOLUMN] in ['TRUE', '1'])
    
    name = simpleEscape(row[NAMECOLUMN])
    name = name.split(None, 1)
    firstName = name[0]
    lastName = name[1]
    
    pittUsername = simpleEscape(row[EMAILCOLUMN])
    #Do they have an @ in their username? If so, do nothing. Otherwise, assume
    #it is a Pitt username and add the suffix.
    if '@' not in pittUsername:
        pittUsername += "@pitt.edu"

    department = simpleEscape(row[DEPARTMENTCOLUMN])
    phonenumber = ''
    
    #url = 'http://stage.asgso.pitt.edu/doku.php/teaching_award_application2013?appID='+appID
    url = 'http://asgso.pitt.edu/doku.php/teaching_award_application2013?appID='+appID
    #print 'INSERT INTO `asgso`.`teachingAwardStudent` (`appID`, `firstName`, `lastName`, `pittUsername`, `department`, `onCampusAddress`, `offCampusAddress`, `phoneNumber`, `letterOfSupportSenderName1`, `letterOfSupportSenderEmail1`, `letterOfSupportSenderRelationship1`, `letterOfSupportSenderName2`, `letterOfSupportSenderEmail2`, `letterOfSupportSenderRelationship2`, `letterOfSupportSenderName3`, `letterOfSupportSenderEmail3`, `letterOfSupportSenderRelationship3`, `courseDepartment1`, `courseNumber1`, `courseStudentCount1`, `courseLabsRecitationsStudentWasResponsibleFor1`, `courseRole1`, `courseOmet1`, `courseDepartment2`, `courseNumber2`, `courseStudentCount2`, `courseLabsRecitationsStudentWasResponsibleFor2`, `courseRole2`, `courseOmet2`, `courseDepartment3`, `courseNumber3`, `courseStudentCount3`, `courseLabsRecitationsStudentWasResponsibleFor3`, `courseRole3`, `courseOmet3`, `courseDepartment4`, `courseNumber4`, `courseStudentCount4`, `courseLabsRecitationsStudentWasResponsibleFor4`, `courseRole4`, `courseOmet4`, `courseDepartment5`, `courseNumber5`, `courseStudentCount5`, `courseLabsRecitationsStudentWasResponsibleFor5`, `courseRole5`, `courseOmet5`, `courseDepartment6`, `courseNumber6`, `courseStudentCount6`, `courseLabsRecitationsStudentWasResponsibleFor6`, `courseRole6`, `courseOmet6`, `teachingPhilosophy`, `teachingChallenge`, `teachingReflection`, `submitted`) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', \'\', NULL, NULL, NULL, \'0\');' % (appID, firstName, lastName, pittUsername, department)
    print 'INSERT INTO `asgso`.`teachingAwardStudent` (`appID`, `firstName`, `lastName`, `pittUsername`, `department`, `phoneNumber`) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' % (appID, firstName, lastName, pittUsername, department, phonenumber)
    writer.writerow([readytosend, appID, firstName, lastName, pittUsername, department, phonenumber, url])


