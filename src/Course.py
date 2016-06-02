

class Course:

    title = ""
    meta = ""
    sections = []

    def __init__(self, title, meta, sections):
        self.title = title
        self.meta = meta
        self.sections = sections

        name = "curso1.txt"
        file = open(name, "w+")
        file.write(title.encode('utf-8') + "\n")
        for section in sections:
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
