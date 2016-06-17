

class Course:

    def __init__(self, title_full="", title_short="", sections=[], glossary={}):
        self.title_full = title_full or ""
        self.title_short = title_short or ""
        self.sections = sections or []
        self.glossary = glossary or {}
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

    def __init__(self, title, sessions):
        self.title = title
        self.sessions = sessions


class Session:

    def __init__(self, title, content):
        self.title = title
        self.content = content

from collections import OrderedDict
class Glossary:

    def __init__(self, glossary_items={}):
        self.glossary_items = glossary_items or {}

    def group(self):
        grouped_items = {}
        index = 'A-A'
        for key in sorted(self.glossary_items.keys()):
            if key.isdigit():
                if 'Special' in grouped_items:
                    grouped_items['Special'].extend(self.glossary_items[key])
                else:
                    grouped_items['Special'] = self.glossary_items[key]

            else:
                if index in grouped_items:
                    actual_count = len(grouped_items[index])
                    new_count = actual_count + len(self.glossary_items[key])
                    if new_count > 20:
                        index = key + '-' + key
                        grouped_items[index] = self.glossary_items[key]
                    else:
                        new_index = index[:-1] + key
                        grouped_items[new_index] = grouped_items.pop(index)
                        grouped_items[new_index].extend(self.glossary_items[key])
                        index = new_index
                else:
                    grouped_items[index] = self.glossary_items[key]

        self.glossary_items = OrderedDict(sorted(grouped_items.items()))

    def to_section(self):
        sessions = []
        for key, value in self.glossary_items.iteritems():
            content = '<Paragraph>'
            for item in value:
                content += '<Paragraph><h1>' + item.concept + ':</h1><Paragraph>' + item.definition + '</Paragraph></Paragraph>'
            session_title = '<Title>' + key + '</Title>'
            content += '</Paragraph>'
            sessions.append(Session(session_title, content))

        section_title = '<Title>Glossary</Title>'
        return Section(section_title, sessions)

class GlossaryItem:

    def __init__(self, concept, definition):
        self.concept = concept
        self.definition = definition
