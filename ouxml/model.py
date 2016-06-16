

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
        file = open(filename, "w+")
        file.write(self.title_full + "\n")
        for section in self.sections:
            file.write(section.title + "\n")
            for session in section.sessions:
                file.write(session.title + "\n")
                file.write(session.content + "\n")
        file.close()


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
