import re


class Course:

    sections = []

    def __init__(self, title_full="", title_short="", sections=[]):
        self.title_full = title_full or ""
        self.title_short = title_short or ""
        self.sections = sections or []
        print ('Course object created successfully!\n')

    def coursetofile(self, filename):
        """Write the complete course to a file"""
        print('\nWriting course to the file ' + filename)
        f = open(filename, "w+")
        f.write(self.title_full + "\n")
        for section in self.sections:
            f.write(section.title + "\n")
            for session in section.sessions:
                f.write(session.title + "\n")
                f.write(session.content + "\n")
        f.close()


class Section:

    title = ""
    sessions = []

    def __init__(self, title, sessions):
        self.title = title
        self.sessions = sessions

    def remove_title_numbering(self):
        self.title = re.sub('^([0-9]+\.?)+\s*', '', self.title)
        self.title = re.sub('^Study Session [0-9]+\s*', '', self.title)


class Session:

    title = ""
    content = ""

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def remove_title_numbering(self):
        self.title = re.sub('^([0-9]+\.?)+\s*', '', self.title)
