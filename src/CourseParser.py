
import urllib2

import sys

import Course
import re
import os
import CourseExporter
from xml.etree import ElementTree
import ContentPreprocessor as CP
from urllib2 import HTTPError, URLError
import settings

from utils.URLUtils import URLUtils


class ParseXML:

    course_title = ""
    sections = []

    def __init__(self, input_path, output_path):
        print('Getting course from file ' + input_path)
        print('\nGetting images from RSS files')
        self.getimages(input_path)
        print('\nGetting contents from XML files')
        course = self.getcourse(input_path)
        #course.coursetofile("CourseOU.txt")
        CP.ContentPreprocessor(settings.XSL_FILE).coursetohtml(course)
        CourseExporter.CourseExporter(course, output_path)
        #course.coursetofile("CourseOppia.txt")

        print ('\nCourse created successfully!')


    def getcourse(self, input_path):
        """ Get the course from a .txt that contains the URLs to the xml files of the course sections"""
        file = open(input_path, "r")

        i = 1
        for url in file:
            if "glossary" not in url:
                xml_url = URLUtils.get_file_url(url)
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
                    print('Section ' + str(i) + ':')
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
        i = 1
        session_count = len(element.findall('.//Session'))
        for session in element.iter('Session'):
            if session_count != 0:
                progress = str(i * 100 / session_count) + '%'
                print '\r > Parsing Sessions (' + str(i) + '/' + str(session_count) + ' - ' + progress + ').',
                sys.stdout.flush()
            session_title = ElementTree.tostring(session.find('Title'), 'utf8', 'xml')
            session.remove(session.find('Title'))
            content = ElementTree.tostring(session, 'utf8', 'xml')
            sessions.append(Course.Session(session_title, content))
            i += 1

        self.sections.append(Course.Section(section_title, sessions))
        print 'Done.\n'

    def getimages(self, input_path):
        file = open(input_path, "r")

        i = 1
        for url in file:
            if "glossary" not in url:

                print 'Section '+str(i)+':\n  > Getting RSS link from url...',
                rss_url = URLUtils.get_file_url(url, 'rss')
                if rss_url is None:
                    print 'RSS link not found in URL.'
                    continue
                else:
                    print 'Done.'

                try:
                    #print('Requesting file ' + str(i) + '(' + rss_url.rstrip() + ')')
                    print '  > Downloading RSS file...',
                    response = urllib2.urlopen(rss_url)
                    rss_file = response.read()
                except HTTPError as e:
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                except URLError as e:
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                else:
                    print "Done."
                    contextid = self.downloadimages(rss_file)
                    response.close()
            i += 1

    def downloadimages(self, content):
        element = ElementTree.fromstring(content)

        i = 1
        for session in element.iter('item'):
            try:
                print '  Session ' + str(i) + ":"
                description = session.find('description')
                #print description.text
                images_list = re.findall('http[s]?://[^\s]*\.(?:jpg|JPG|png|PNG|jpeg|JPEG)', ElementTree.tostring(description, 'utf8', 'xml'))
                if len(images_list) == 0:
                    print '  > No images to download.'
                    i += 1
                    continue
                else:

                    if not os.path.exists('images'):
                        os.makedirs('images')

                    print '  > Getting images from RSS file content... '

                j = 0
                for image_url in images_list:
                    progress = str(j * 100 / len(images_list)) + '%'
                    print '\r  > Downloading images (' + progress + ')',
                    sys.stdout.flush()
                    filename = image_url.split("/")[-1].replace(".small", "")
                    response = urllib2.urlopen(image_url)

                    if not os.path.exists('images'):
                        os.makedirs('images')

                    f = open("images/" + filename, "wb+")
                    f.write(response.read())
                    f.close()

                    j += 1
                print '\r  > Downloading images (100%). Done.'
                i += 1
            except AttributeError:
                return

print str(len(sys.argv))
if len(sys.argv) != 3:
    print 'Wrong number of arguments.'
    print 'Usage: TO-DO'
else:
    ParseXML(str(sys.argv[1]), str(sys.argv[2]))
