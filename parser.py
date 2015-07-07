#!/usr/bin/python3
# parser.py - parse HTML

import os
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.finished = False
        self.uselss = False
        self.timeStamp = False
        self.thread = False
        self.Name = False
        self.Message = False
       
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data :", data)

friends = open('/home/shane/Documents/FacebookProject/FacebookData/html/friends.htm')
data = friends.read()
parser = MyHTMLParser()
parser.feed(data)
