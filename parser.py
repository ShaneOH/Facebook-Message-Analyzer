#!/usr/bin/python3
import logging, sqlite3
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# parser.py - parse messages.htm and store the messages in a database

from html.parser import HTMLParser

#connect to SQLite database
messageDB = sqlite3.connect('testMessages.db')
db = messageDB.cursor()

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.useless = True
        self.timestamp = ""
        self.tsFlag = False
        self.thread = ""
        self.thFlag = False
        self.name = ""
        self.nFlag = False
        self.message = ""
        self.mFlag = False
        self.threadList = []

    def handle_starttag(self, tag, attrs):
       
        if tag == "html" or tag == "head" or tag == "meta" or tag == "li" or tag == "title" or tag == "link" or tag == "img" or tag == "body" or tag == "a" or tag == "h1" or tag == "h2": #junk html 
            self.useless = True

        if tag == "div":
            for name, value in attrs:
                if name == "class":
                    if value == "message" or value == "message_header": #beginning of messages but unimportant
                        self.useless = False
                    if value == "thread": #new thread
                        self.useless = False
                        self.thFlag = True

        if tag == "span":
            for name, value in attrs:
                if name == "class":
                    if value == "user": #name of person sending message
                        self.useless = False
                        self.nFlag = True
                    if value == "meta": #timestamp attached to message
                        self.useless = False
                        self.tsFlag = True
                    
        if tag == "p": #actual message
            self.useless = False
            self.mFlag = True

    def handle_endtag(self, tag):
        self.useless = True

    def handle_data(self, data):
        if self.useless == False:
            
            if self.thFlag == True:
                self.thread = data
                logging.debug("We hit a thread, setting self.thread to: " + str(self.thread))
                if self.thread not in self.threadList:
                    #create new table for thread
                    db.execute('''CREATE TABLE "'''+self.thread+'''" (name text, time text, message text)''') #NOTE: not best practice, in real-world use string constructor opens up SQL Injection vulnerability. Would have to scrub string input. 
                    self.threadList.append(self.thread)
                self.thFlag = False
            if self.nFlag == True:
                self.name = data
                self.nFlag = False
            if self.tsFlag == True:
                self.timestamp = data
                self.tsFlag = False
            if self.mFlag == True:
                self.message = data
                self.mFlag = False

        if self.name and self.timestamp and self.message: #we've got a full message object
            self.list = [self.name, self.timestamp, self.message]
            self.name, self.timestamp, self.message = "","",""
            #insert message into table
            db.execute('''INSERT INTO "'''+self.thread+'''" VALUES (?,?,?)''', self.list)

testMessages = open('/home/shane/Documents/FacebookProject/FacebookData/html/testMessages.htm')
data = testMessages.read()
parser = MyHTMLParser()
parser.feed(data)
messageDB.commit()
messageDB.close()
