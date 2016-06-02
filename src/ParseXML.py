import sys  
import urllib2
import Course
from xml.etree import ElementTree 
import traceback
from Tkinter import Tk
from tkFileDialog import askopenfilename


class ParseXML:

    course_title = ""
    sections = []

    def __init__(self):
        Tk().withdraw()
        path = askopenfilename()
        self.getxml(path)
        Course.Course(self.course_title, "", self.sections)

    def getxml(self, path):
        file = open(path, "r")
        for line in file:
            print line
            if "glossary" not in line:
                extra = "&content=scxml"
                if extra not in line:
                    line = line.rstrip() + extra
                self.parsexml(urllib2.urlopen(line).read())
        file.close()

    def parsexml(self, content):
        e = ElementTree.fromstring(content)

        self.course_title = e.find('CourseTitle').text

        section_title = e.find('ItemTitle').text

        sessions = []
        content = []
        for session in e.iter('Session'):
            session_title = session.find('Title').text
            for paragraph in session.iter('Paragraph'):
                content.append(paragraph.text)
            sessions.append(Course.Session(session_title, content))

        self.sections.append(Course.Section(section_title, sessions))

ParseXML()
