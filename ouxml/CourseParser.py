import sys
import urllib2
from urllib2 import HTTPError, URLError
from xml.etree import ElementTree

import os
import re

import ContentPreprocessor
import settings
from model import Course, Section, Session
from utils.URLUtils import URLUtils


class CourseParser:

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

        self.course = Course()

    def retrieve_course(self):
        """ Obtains all the course contents and pre-process it"""

        print('Getting course from file ' + self.input_path)
        file = open(self.input_path, "r")

        print '\n========== COURSE PARSER ================='
        for section_idx, url in enumerate(file, start=1):
            if "glossary" not in url:
                print '\nSection %d:' % section_idx

                self.get_contents(url)
                self.get_images(url)
            else:
                print '\n"Glossary" Section:'

        file.close()

        cp = ContentPreprocessor.ContentPreprocessor(settings.XSL_FILE, self.course)
        cp.preprocess_course()

        return self.course

    def get_contents(self, url):
        """ Get the course contents from a .txt that contains the URLs to the course sections.
            The contents are get from the XML files of the course."""

        xml_url = URLUtils.get_file_url(url).rstrip()
        try:
            print '  > Downloading XML file... ',
            response = urllib2.urlopen(xml_url)
            section_xml = response.read()
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            print 'Done.'
            self.parse_xml(section_xml)
            response.close()

    def parse_xml(self, content):
        """ Parse the xml file and build the course"""
        element = ElementTree.fromstring(content)

        if not self.course.title_full:
            self.course.title_full = ElementTree.tostring(element.find('CourseTitle'), 'utf8', 'text')
        if not self.course.title_short:
            self.course.title_short = ElementTree.tostring(element.find('CourseCode'), 'utf8', 'text')

        section_title = ElementTree.tostring(element.find('ItemTitle'), 'utf8', 'xml')

        sessions = []
        session_count = len(element.findall('.//Session'))
        references_count = len(element.findall('.//Reference'))

        if references_count != 0:
            for i, reference in enumerate(element.iter('Session'), start=1):
                progress = str(i * 100 / references_count) + '%'
                print '\r  > Parsing References (' + str(i) + '/' + str(references_count) + ' - ' + progress + ').',
                sys.stdout.flush()
                references_title = '<Title>References</Title>'
                content = ElementTree.tostring(reference, 'utf8', 'xml')
                sessions.append(Session(references_title, content))

        elif session_count != 0:
            for i, session in enumerate(element.iter('Session'), start=1):
                progress = str(i * 100 / session_count) + '%'
                print '\r  > Parsing Sessions (' + str(i) + '/' + str(session_count) + ' - ' + progress + ').',
                sys.stdout.flush()
                session_title = ElementTree.tostring(session.find('Title'), 'utf8', 'xml')
                session.remove(session.find('Title'))
                content = ElementTree.tostring(session, 'utf8', 'xml')
                sessions.append(Session(session_title, content))


        self.course.sections.append(Section(section_title, sessions))
        print 'Done.'

    def get_images(self, url):
        """ Get the course images from a .t xt that contains the URLs to the course sections.
            The images are get from the RSS files of the course."""

        print '  > Getting RSS link from url...',
        rss_url = URLUtils.get_file_url(url, 'rss')
        if rss_url is None:
            print 'RSS link not found in URL.'
            return
        else:
            print 'Done.'

        try:
            # print('Requesting file ' + str(i) + '(' + rss_url.rstrip() + ')')
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
            print "Done. Processing each section images:"
            self.download_images(rss_file)
            response.close()

    def download_images(self, content):
        element = ElementTree.fromstring(content)

        images_dir = os.path.join(self.output_path, 'temp', 'images')
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        for i, session in enumerate(element.iter('item'), start=1):
            try:
                print '    * Session ' + str(i) + ":",
                description = ElementTree.tostring(session.find('description'), 'utf8', 'xml')
                # print description.text
                images_list = re.findall('http[s]?://[^\s]*\.(?:jpg|JPG|png|PNG|jpeg|JPEG)', description)
                if len(images_list) == 0:
                    print 'No images to download.'
                    i += 1
                    continue
                else:
                    print '\n      > Getting images from RSS file content... '

                    j = 0
                    for image_url in images_list:
                        progress = str(j * 100 / len(images_list)) + '%'
                        print '\r      > Downloading images (' + progress + ')',
                        sys.stdout.flush()
                        filename = image_url.split("/")[-1].replace(".small", "")
                        response = urllib2.urlopen(image_url)

                        f = open(os.path.join(images_dir, filename), "wb+")
                        f.write(response.read())
                        f.close()

                        j += 1
                    print '\r      > Downloading images (100%). Done.'

            except AttributeError:
                return
