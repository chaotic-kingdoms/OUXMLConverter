
import ContentPreprocessor as CP

class Course:

    title = ""
    meta = ""
    sections = []

    def __init__(self, title, meta, sections):
        self.title = title
        self.meta = meta
        self.sections = sections
        print ('Course created successfully!\n')

    def coursetofile(self, filename):
        """Write the complete course to a file"""
        print('Writing course to the file ' + filename)
        file = open(filename, "w+")
        file.write(self.title + "\n")
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
        print ('Section created successfully!')

class Session:

    title = ""
    content = ""

    def __init__(self, title, content):
        print ('Creating session...')
        self.title = title
        self.content = content
