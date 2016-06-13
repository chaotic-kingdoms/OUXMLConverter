
import lxml.etree as ET


class ContentPreprocessor:

    xslfile = ""

    def __init__(self, xslfile):
        self.xslfile = xslfile

    def contenttohtml(self, content):
        """Apply XSLT to the content of the course and returns the converted HTML text"""
        dom = ET.XML(content, ET.XMLParser(target=ET.TreeBuilder()))
        xslt = ET.parse(self.xslfile)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return ET.tostring(newdom, pretty_print=True)

    def coursetohtml(self, course):

        print('Applying XSLT to the course...')
        course.title = self.contenttohtml(course.title)

        for section in course.sections:
            section.title = self.contenttohtml(section.title)
            for session in section.sessions:
                session.title = self.contenttohtml(session.title)
                session.content = self.contenttohtml(session.content)

        return course
