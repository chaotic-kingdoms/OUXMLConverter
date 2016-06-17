import re
from collections import OrderedDict
import pystache
import os
import settings

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
        renderer = pystache.Renderer()
        sessions = []

        for key, value in self.glossary_items.iteritems():

            items = []
            for item in value:
                items.append({'concept': item.concept, 'definition': item.definition})

            content = renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'glossary.mustache'), {'items': items})
            session_title = renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'title.mustache'), {'value': key})
            sessions.append(Session(session_title, content))

        section_title = renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'title.mustache'), {'value': 'Glossary'})
        return Section(section_title, sessions)


class GlossaryItem:

    def __init__(self, concept, definition):
        self.concept = concept
        self.definition = definition
