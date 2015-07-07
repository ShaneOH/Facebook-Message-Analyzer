#!/usr/bin/python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# parser.py - parse HTML

import os
from html.parser import HTMLParser

#table = {}

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.finished = False
        self.useless = True
        self.timestamp = ""
        self.tsFlag = False
        self.thread = ""
        self.thFlag = False
        self.name = ""
        self.nFlag = False
        self.message = ""
        self.mFlag = False
       
    def handle_starttag(self, tag, attrs):
       
        if tag == "html" or tag == "head" or tag == "meta" or tag == "li" or tag == "title" or tag == "link" or tag == "img" or tag == "body" or tag == "a" or tag == "h1" or tag == "h2": #junk html 
            self.useless = True

        if tag == "div":
            for name, value in attrs:
                if name == "class":
                    if value == "message" or value == "message_header": #beginning of messages but unimportant
                        self.useless = False
       
        if tag == "span":
            for name, value in attrs:
                if name == "class":
                    if value == "user": #name of person sending message
                        self.useless = False
                        self.nFlag = True
                    if value == "meta": #timestamp attached to message
                        self.useless = False
                        self.tsFlag = True
                    if value == "thread": #new thread
                        self.useless = False
                        self.thFlag = True
                    
        if tag == "p": #actual message
            self.useless = False
            self.mFlag = True

    def handle_endtag(self, tag):
        self.useless = True

    def handle_data(self, data):
        if self.useless == False:
            logging.debug("We encountered some useful data: " + str(data))
"""
            if self.nFlag == True:
                self.name = data
                #logging.debug("We're setting self.name to " + str(data))
                self.nFlag = False
            if self.tsFlag == True:
                self.timestamp = data
                #logging.debug("We're setting self.timestamp to " + str(data))
                self.tsFlag = False
"""
messages = open('/home/shane/Documents/FacebookProject/FacebookData/html/messages.htm')
data = messages.read()
parser = MyHTMLParser()
parser.feed(data)
#print(table)
