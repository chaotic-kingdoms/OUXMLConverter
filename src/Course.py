

class Course:

    title = ""
    meta = ""
    sections = []

    def __init__(self, title, meta, sections):
        self.title = title
        self.meta = meta
        self.sections = sections
        print title
        for section in sections:
            print section.title
            for session in section.sessions:
                print session.title
                for content in session.content:
                    print content


class Section:

    title = ""
    sessions = []

    def __init__(self, title, sessions):
        self.title = title
        self.sessions = sessions


class Session:

    title = ""
    content = []

    def __init__(self, title, content):
        self.title = title
        self.content = content
