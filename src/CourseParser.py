
import urllib2
import Course
import re
import os
import CourseExporter
from xml.etree import ElementTree
from Tkinter import Tk
from tkFileDialog import askopenfilename
import ContentPreprocessor as CP
from urllib2 import HTTPError, URLError
import settings

from utils.URLUtils import URLUtils


class ParseXML:

    course_title = ""
    sections = []

    def __init__(self):
        Tk().withdraw()
        path = askopenfilename()
        print('Getting course from file ' + path)
        print('\nGetting images from RSS files')
        self.getimages(path)
        print('\nGetting contents from XML files')
        course = self.getcourse(path)
        #course.coursetofile("CourseOU.txt")
        CP.ContentPreprocessor(settings.XSL_FILE).coursetohtml(course)
        CourseExporter.CourseExporter(course)
        #course.coursetofile("CourseOppia.txt")

        print ('\nCourse created successfully!')


    def getcourse(self, path):
        """ Get the course from a .txt that contains the URLs to the xml files of the course sections"""
        file = open(path, "r")

        i = 1
        for url in file:
            if "glossary" not in url:
                xml_url = URLUtils.get_file_url(url, format='xml')
                try:
                    print('Requesting file ' + str(i) + '(' + xml_url.rstrip() + ')')
                    response = urllib2.urlopen(xml_url)
                    section_xml = response.read()
                except HTTPError as e:
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                except URLError as e:
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                else:
                    print('Parsing file ' + str(i) + '...')
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

    def getimages(self, path):
        file = open(path, "r")

        i = 1
        for url in file:
            if "glossary" not in url:
                rss_url = URLUtils.get_file_url(url, 'rss')
                try:
                    print('Requesting file ' + str(i) + '(' + rss_url.rstrip() + ')')
                    response = urllib2.urlopen(rss_url)
                    rss_file = response.read()
                except HTTPError as e:
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                except URLError as e:
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                else:
                    print('Getting images from file ' + str(i) + '...')
                    self.downloadimages(rss_file)
                    response.close()
            i += 1

    def downloadimages(self, content):

        if not os.path.exists('images'):
            os.makedirs('images')

        try:
            images_list = re.findall('http[s]?://[^\s]*\.jpg', content)
            for image_url in images_list:

                filename = image_url.split("/")[-1]
                response = urllib2.urlopen(image_url)

                f = open("images/" + filename, "wb+")
                f.write(response.read())
                f.close()
        except AttributeError:
            return


ParseXML()
