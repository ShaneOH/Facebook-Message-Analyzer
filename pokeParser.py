#!/usr/bin/python3
import logging, sqlite3
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# parser.py - parse HTML

import os
from html.parser import HTMLParser

table = {}
list = []

pokeDB = sqlite3.connect('poke.db')
db = pokeDB.cursor()

#create table
db.execute('''CREATE TABLE pokes (poke text, time text)''')

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
       
        if tag == "html" or tag == "head" or tag == "meta" or tag == "title" or tag == "link" or tag == "img" or tag == "body" or tag == "a" or tag == "h1" or tag == "h2": #junk html 
            self.useless = True

        if tag == "div":
            for name, value in attrs:
                if name == "class":
                    if value == "meta": #timestamp
                        self.useless = False
                        self.tsFlag = True
           
        if tag == "li": #poke
            if not attrs:
                self.useless = False
                self.nFlag = True

    def handle_endtag(self, tag):
        self.useless = True

    def handle_data(self, data):
        if self.useless == False:
            logging.debug("We encountered some useful data: " + str(data))

            if self.nFlag == True:
                self.name = data
                logging.debug("We're setting self.name to " + str(data))
                self.nFlag = False
            
            if self.tsFlag == True:
                self.timestamp = data
                logging.debug("We're setting self.timestamp to " + str(data))
                self.tsFlag = False
       
        if self.name and self.timestamp:
            logging.debug("We're now setting " + str(self.name) + " = " + str(self.timestamp))
            list = [self.name, self.timestamp]
            print(list)
            table[self.name] = self.timestamp
            self.name = ""
            self.timestamp = ""
            #insert a row of data
            db.execute("INSERT INTO pokes VALUES (?,?)", list)

pokes = open('/home/shane/Documents/FacebookProject/FacebookData/html/pokes.htm')
data = pokes.read()
parser = MyHTMLParser()
parser.feed(data)
print(table)
pokeDB.commit()
pokeDB.close()
