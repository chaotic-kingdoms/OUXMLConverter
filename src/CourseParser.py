import urllib2
import Course
import CheckUsedTags
import CourseExporter
from xml.etree import ElementTree
from Tkinter import Tk
from tkFileDialog import askopenfilename
import ContentPreprocessor as CP
from urllib2 import HTTPError, URLError


class ParseXML:

    course_title = ""
    sections = []

    def __init__(self):
        Tk().withdraw()
        path = askopenfilename()    #File Selection
        #CheckUsedTags.CheckUsedTags(path)
        print('Getting course from file ' + path)
        course = self.getcourse(path)
        course.coursetofile("CourseOU.txt")
        CP.ContentPreprocessor("coursetemplate.xsl").coursetohtml(course)
        CourseExporter.CourseExporter(course)
        course.coursetofile("CourseOppia.txt")


    def getcourse(self, path):
        """ Get the course from a .txt that contains the URLs to the xml files of the course sections"""
        file = open(path, "r")

        i = 1
        for xml_url in file:
            if "glossary" not in xml_url:
                try:
                    print('Requesting file ' + str(i) + '(' + xml_url.rstrip() + ')' + '...')
                    response = urllib2.urlopen(xml_url)
                    section_xml = response.read()
                except HTTPError as e:
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                except URLError as e:
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                else:
                    print('Parsing file ' + str(i))
                    self.parsexml(section_xml)
                    response.close()
            i += 1

        file.close()
        return Course.Course(self.course_title, "", self.sections)

    def parsexml(self, content):
        """ Parse the xml file and build the course"""
        element = ElementTree.fromstring(content)

        self.course_title = ElementTree.tostring(element.find('CourseTitle'), 'utf8', 'xml')
        section_title = ElementTree.tostring(element.find('ItemTitle'), 'utf8', 'xml')

        sessions = []
        for session in element.iter('Session'):
            session_title = ElementTree.tostring(session.find('Title'), 'utf8', 'xml')
            session.remove(session.find('Title'))
            content = ElementTree.tostring(session, 'utf8', 'xml')
            sessions.append(Course.Session(session_title, content))

        self.sections.append(Course.Section(section_title, sessions))
        print("Success parsing file!\n")

ParseXML()
