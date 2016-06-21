import re
import sys

import lxml.etree as ET
import os
from os import listdir
from utils.ImageUtils import ImageUtils
import settings


class ContentPreprocessor:

    def __init__(self, xsl_file, course, keepnums):
        self.xsl_file = xsl_file
        self.course = course
        self.keepnums = keepnums    # Keep numbering on section titles

    def preprocess_course(self):
        """ Perform the course pre-processing. This include converting the course contents to HTML and optimize the
            course images"""

        print '\n========== COURSE PREPROCESSING =================\n'
        self.course_to_html()
        self.optimize_images()

    def course_to_html(self):

        for i, section in enumerate(self.course.sections):

            section.title = self.content_to_html(section.title)
            section.title = "".join(ET.fromstring(section.title).itertext())
            #section.title = html.fromstring(section.title).text_content()  # clean up tags
            if not self.keepnums:
                section.remove_title_numbering()

            progress = str(i * 100 / len(self.course.sections)) + '%'
            print '\r  > Applying XSLT to the course (' + progress + ')',
            sys.stdout.flush()

            for session in section.sessions:
                session.title = self.content_to_html(session.title)
                session.content = self.content_to_html(session.content)

        print '\r  > Applying XSLT to the course (100%). Done.'

    def content_to_html(self, content):
        """Apply XSLT to the content of the course and returns the converted HTML text"""

        dom = ET.XML(content, ET.XMLParser())
        xslt = ET.parse(self.xsl_file)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return re.sub('(&#160;)+', ' ', ET.tostring(newdom, pretty_print=True))

    def optimize_images(self):
        images_dir = os.path.join(settings.OUTPUT_PATH, 'temp', 'images')
        images = listdir(images_dir)
        size_saved = 0

        for i, image_file in enumerate(images):
            image_path = os.path.join(images_dir, image_file)

            progress = str(i * 100 / len(images)) + '%'
            print '\r  > Optimizing images (' + progress + ')',
            sys.stdout.flush()

            size_saved += ImageUtils.save_optimized_image(image_path)

        print '\r  > Optimizing images (100%). Done. ' + str(size_saved/1024) + 'KB saved.'
