import sys
import re
import urllib2
import Course
from xml.etree import ElementTree 
import traceback
from Tkinter import Tk
from tkFileDialog import askopenfilename
from itertools import chain
from lxml.etree import tostring


class ParseXML:

    course_title = ""
    sections = []

    def __init__(self):
        Tk().withdraw()
        path = askopenfilename()
        self.getcourse(path)
        Course.Course(self.course_title, "", self.sections)

    ### Get the course from a .txt that contains the URLs to the xml files of the course sections
    def getcourse(self, path):
        file = open(path, "r")
        for line in file:
            if "glossary" not in line:
                extra = "&content=scxml"
                if extra not in line:
                    line = line.rstrip() + extra
                self.parsexml(urllib2.urlopen(line).read())
                #self.parsexml(re.sub(r'<(b|i)>(.*?)<\/(b|i)>', "&gt;\g<1>&lt;\g<2>&gt;\g<3>&lt;", urllib2.urlopen(line).read()))
        file.close()

    ### Parse the xml file and build the course
    def parsexml(self, content):
        element = ElementTree.fromstring(content)

        self.course_title = ElementTree.tostring(element.find('CourseTitle'), 'utf8', 'html')

        section_title = ElementTree.tostring(element.find('ItemTitle'), 'utf8', 'html')

        sessions = []
        for session in element.iter('Session'):
            session_title = ElementTree.tostring(session.find('Title'), 'utf8', 'html')
            session.remove(session.find('Title'))
            content = ElementTree.tostring(session, 'utf8', 'html')

            sessions.append(Course.Session(session_title, content))

        self.sections.append(Course.Section(section_title, sessions))

ParseXML()
