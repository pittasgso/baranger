import email,string
import gmail_imap
from datetime import datetime
import time

class gmail_message:

    def __init__(self):
    
        self.id = None
        self.uid = None
        self.flags = None
        self.mailbox = None
        self.__date = None
        self.__timestamp = None
        
        self.From = None
        self.Subject = '( no subject )'
        self.Body = None
        
        self.attachments = []
    
    def set_date(self, date):
        self.__date = date
        try:
            date = date.rsplit(None, 1)[0] #remove utc offset
            date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S')
            self.__timestamp = int(time.mktime(date.timetuple()))
        except:
            self.__timestamp = None
    def get_date(self): return self.__date
    date = property(get_date, set_date)
    
    @property
    def timestamp(self): return self.__timestamp
    
    @property
    def FromEmail(self):
        if '<' not in self.From: return self.From
        
        start = self.From.find('<')+1
        end = self.From.find('>', start)
        return self.From[start:end]
    
    @property
    def FromLabel(self):
        if '<' not in self.From: return ''
        
        start = self.From.find('<')
        end = self.From.find('>', start)+1
        return (self.From[:start] + self.From[end:]).strip()
    
    def __repr__(self):
        str = "<gmail_message:  ID: %s  UID: %s Flags: %s Date: %s \n" % (self.id,self.uid,self.flags,self.date)
        str += "from: %s subject: %s >" % (self.From,self.Subject)
        return str
    
    
