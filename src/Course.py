
import lxml.etree as ET


class Course:

    title = ""
    meta = ""
    sections = []

    def __init__(self, title, meta, sections):
        self.title = title
        self.meta = meta
        self.sections = sections


    def coursetofile(self):
        """Write the complete course to a file named testcourse.txt"""
        file = open("testcourse.txt", "w+")
        file.write(self.coursetohtml(self.title) + "\n")
        for section in self.sections:
            file.write(self.coursetohtml(section.title) + "\n")
            for session in section.sessions:
                file.write(self.coursetohtml(session.title + "\n"))
                file.write(self.coursetohtml(session.content + "\n"))
        file.close()

    def coursetohtml(self, content):
        """Apply XSLT to a course and returns the converted HTML text"""
        dom = ET.XML(content, ET.XMLParser(target=ET.TreeBuilder()))
        xslt = ET.parse("coursetemplate.xsl")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        return ET.tostring(newdom, pretty_print=True)


class Section:

    title = ""
    sessions = []

    def __init__(self, title, sessions):
        self.title = title
        self.sessions = sessions


class Session:

    title = ""
    content = ""

    def __init__(self, title, content):
        self.title = title
        self.content = content
