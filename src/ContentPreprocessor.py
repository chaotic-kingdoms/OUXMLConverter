
import lxml.etree as ET
from PIL import Image
import os
import settings
from os import listdir
import sys


class ContentPreprocessor(object):

    @staticmethod
    def contenttohtml(content, xslfile):
        """Apply XSLT to the content of the course and returns the converted HTML text"""
        dom = ET.XML(content, ET.XMLParser(target=ET.TreeBuilder()))
        xslt = ET.parse(xslfile)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return ET.tostring(newdom, pretty_print=True)

    @staticmethod
    def course_to_html(course, xslfile):


        course.title = ContentPreprocessor.contenttohtml(course.title, xslfile)
        i = 1
        for section in course.sections:
            section.title = ContentPreprocessor.contenttohtml(section.title, xslfile)
            for session in section.sessions:
                progress = str(i * 100 / len(section.sessions)) + '%'
                print '\r> Applying XSLT to the course (' + progress + ')',
                sys.stdout.flush()
                session.title = ContentPreprocessor.contenttohtml(session.title, xslfile)
                session.content = ContentPreprocessor.contenttohtml(session.content, xslfile)
                i += 1
        print '\r> Applying XSLT to the course (100%). Done.'
        return course

    @staticmethod
    def optimize_images():
        print '\nBegining image optimization'
        images_folder = os.path.join(settings.PROJECT_ROOT, 'images')
        size_saved = 0
        i = 1
        for image_file in listdir(images_folder):
            image_path = os.path.join(images_folder, image_file)
            initial_size = os.stat(image_path).st_size
            progress = str(i * 100 / len(listdir(images_folder))) + '%'
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
