import sys
from xml.etree import ElementTree

import os
import re
from lxml import html

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
        sections_list = open(self.input_path, "r")

        print '\n========== COURSE PARSER ================='
        for section_idx, url in enumerate(sections_list, start=1):
            if "glossary" not in url:
                print '\nSection %d:' % section_idx

                self.get_contents(url)
                self.get_images(url)
            else:
                print '\n"Glossary" Section:'
                self.get_glossary(url)

        sections_list.close()

        cp = ContentPreprocessor.ContentPreprocessor(settings.XSL_FILE, self.course)
        cp.preprocess_course()

        return self.course

    def get_contents(self, url):
        """ Get the course contents from a .txt that contains the URLs to the course sections.
            The contents are get from the XML files of the course."""
        xml_url = URLUtils.get_format_url(url)
        print '  > Downloading XML file... ',
        err, section_xml = URLUtils.get(xml_url)
        if not err:
            print 'Done.'
            self.parse_xml(section_xml)

    def parse_xml(self, content):
        """ Parse the xml file and build the course"""
        element = ElementTree.fromstring(content)

        if not self.course.title_full:
            self.course.title_full = ElementTree.tostring(element.find('CourseTitle'), 'utf8', 'text')
        if not self.course.title_short:
            self.course.title_short = ElementTree.tostring(element.find('CourseCode'), 'utf8', 'text')

        section_title = ElementTree.tostring(element.find('ItemTitle'), 'utf-8', 'xml')
        #section_title = re.sub('^([0-9]+\.?)+\s*', '', section_title)

        sessions = []
        session_count = len(element.findall('.//Session'))

        for i, session in enumerate(element.iter('Session'), start=1):
            progress = str(i * 100 / session_count) + '%'
            print '\r  > Parsing Sessions (' + str(i) + '/' + str(session_count) + ' - ' + progress + ').',
            session_title = ElementTree.tostring(session.find('Title'), 'utf-8', 'xml')
            #session_title = re.sub('^([0-9]+\.?)+\s*', '', session_title)
            session.remove(session.find('Title'))
            content = ElementTree.tostring(session, 'utf8', 'xml')
            sessions.append(Session(session_title, content))

        self.course.sections.append(Section(section_title, sessions))
        print 'Done.'

    def get_images(self, url):
        """ Get the course images from a .t xt that contains the URLs to the course sections.
            The images are get from the RSS files of the course."""

        print '  > Getting RSS link from url...',
        rss_url = URLUtils.get_format_url(url, 'rss')
        if rss_url is None:
            print 'RSS link not found in URL.'
            return
        else:
            print 'Done.'

        print '  > Downloading RSS file...',
        err, rss_file = URLUtils.get(rss_url)
        if not err:
            print "Done. Processing each section images:"
            self.download_images(rss_file)

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
                    continue
                else:
                    print '\n      > Getting images from RSS file content... '

                    for idx, image_url in enumerate(images_list):
                        progress = str(idx * 100 / len(images_list)) + '%'
                        print '\r      > Downloading images (' + progress + ')',
                        sys.stdout.flush()

                        err, image = URLUtils.get(image_url)
                        if not err:
                            filename = image_url.split("/")[-1].replace(".small", "")
                            f = open(os.path.join(images_dir, filename), "wb+")
                            f.write(image)
                            f.close()

                    print '\r      > Downloading images (100%). Done.'

            except AttributeError:
                return

    def get_glossary(self, url):

        glossary_url = URLUtils.replace_qs_param(url, {'page':'-1'})
        err, page = URLUtils.get(glossary_url)
        if not err:
            entries = html.fromstring(page).cssselect('.glossarypost td.entry')
            for entry in entries:
                concept = entry.cssselect('.concept')
                definition = entry.cssselect('.no-overflow')

                if not concept or not definition:
                    continue

                print concept[0].text_content()
                print definition[0].text_content()
                print
