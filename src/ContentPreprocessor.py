
import lxml.etree as ET
from PIL import Image
import os
import settings
from os import listdir
import sys


class ContentPreprocessor:

    def __init__(self, xsl_file, course, output_path):
        self.xsl_file = xsl_file
        self.course = course
        self.output_path = output_path

    def preprocess_course(self):
        """ Perform the course preprocessing. This include converting the course contents to HTML and optimize the
            course images"""
        self.course_to_html()
        self.optimize_images(self.output_path)

    def course_to_html(self):

        self.course.title = self.content_to_html(self.course.title)
        i = 1
        for section in self.course.sections:
            section.title = self.content_to_html(section.title)
            for session in section.sessions:
                progress = str(i * 100 / len(section.sessions)) + '%'
                print '\r> Applying XSLT to the course (' + progress + ')',
                sys.stdout.flush()
                session.title = self.content_to_html(session.title)
                session.content = self.content_to_html(session.content)
                i += 1
        print '\r> Applying XSLT to the course (100%). Done.'

    def content_to_html(self, content):
        """Apply XSLT to the content of the course and returns the converted HTML text"""
        dom = ET.XML(content, ET.XMLParser(target=ET.TreeBuilder()))
        xslt = ET.parse(self.xsl_file)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return ET.tostring(newdom, pretty_print=True)

    def optimize_images(self, output_path):
        print '\nBegining image optimization'
        images_dir = os.path.join(os.path.join(output_path, 'temp'), 'images')
        size_saved = 0
        i = 1
        for image_file in listdir(images_dir):
            image_path = os.path.join(images_dir, image_file)
            initial_size = os.stat(image_path).st_size
            progress = str(i * 100 / len(listdir(images_dir))) + '%'
            print '\r  > Optimizing images (' + progress + ')',
            sys.stdout.flush()
            image = Image.open(image_path)
            new_width = 300
            width_percent = (new_width / float(image.size[0]))
            new_height = int((float(image.size[1]) * float(width_percent)))
            image.thumbnail((new_width, new_height), Image.ANTIALIAS)
            extension = image_file.split(".")[-1]
            if extension == 'jpg':
                image.save(image_path, optimize=True, quality=90)
            else:
                image.save(image_path)
            final_size = os.stat(image_path).st_size
            size_saved += initial_size - final_size
            i += 1
        print '\r  > Optimizing images (100%). Done. ' + str(size_saved/1024) + 'KB saved.'
