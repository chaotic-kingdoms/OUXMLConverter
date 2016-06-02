import urllib2
import Course
import CheckUsedTags
from xml.etree import ElementTree
from Tkinter import Tk
from tkFileDialog import askopenfilename
import lxml.etree as ET


class ParseXML:

    course_title = ""
    sections = []

    def __init__(self):
        #Select a File
        Tk().withdraw()
        path = askopenfilename()
        self.tohtml(path)
        CheckUsedTags.CheckUsedTags(path)
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

    def tohtml(self, path):
        file = open(path, "r")
        for line in file:
            if "glossary" not in line:
                dom = ET.parse(urllib2.urlopen(line))
                xslt = ET.parse("coursetemplate.xsl")
                transform = ET.XSLT(xslt)
                newdom = transform(dom)
                print(ET.tostring(newdom, pretty_print=True))
ParseXML()
