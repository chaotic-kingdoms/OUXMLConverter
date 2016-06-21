import re
from collections import OrderedDict
import pystache
import os
import sys
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
        self.title = re.sub('^([0-9]+\.?[^-]\s*)+', '', self.title)
        self.title = re.sub('^Study Session [0-9]+\s*', '', self.title)


class Session:

    title = ""
    content = ""

    def __init__(self, title, content, description=''):
        self.title = title
        self.content = content
        self.description = description

    def remove_title_numbering(self):
        self.title = re.sub('^([0-9]+\.?[^-]\s*)+', '', self.title)

    def remove_subsection_numbering(self):
        self.content = re.sub(r'(<h3 class="subsection">)(?:[0-9]+\.?[^-]\s*)+', r'\g<1>', self.content)

class Glossary:

    def __init__(self, glossary_items={}):
        self.glossary_items = glossary_items or {}

    def group(self):
        grouped_items = {}
        index = ''
        for i, key in enumerate(sorted(self.glossary_items)):
            progress = str(i * 100 / len(self.glossary_items.keys())) + '%'
            print '\r  > Grouping glossary items (' + progress + ').',
            sys.stdout.flush()

            if key.isdigit():
                if '0-9' in grouped_items:
                    grouped_items['0-9'].extend(self.glossary_items[key])

                else:
                    grouped_items['0-9'] = self.glossary_items[key]

            else:
                if not index:
                    index = key + '-' + key

                if index in grouped_items:
                    actual_count = len(grouped_items[index])
                    new_count = actual_count + len(self.glossary_items[key])
                    if new_count > 20:
                        if index[0] == index[2]:
                            grouped_items[index[0]] = grouped_items.pop(index)

                        index = key + '-' + key
                        grouped_items[index] = self.glossary_items[key]
                    else:
                        new_index = index[:-1] + key
                        grouped_items[new_index] = grouped_items.pop(index)
                        grouped_items[new_index].extend(self.glossary_items[key])
                        index = new_index
                else:
                    grouped_items[index] = self.glossary_items[key]

        print '\r  > Grouping glossary items (100%). Done.'
        self.glossary_items = OrderedDict(sorted(grouped_items.items()))

    def to_section(self):
        renderer = pystache.Renderer()
        sessions = []

        for i, key in enumerate(self.glossary_items):
            value = self.glossary_items[key]
            progress = str(i * 100 / len(self.glossary_items.keys())) + '%'
            print '\r  > Creating glossary sessions (' + progress + ').',
            sys.stdout.flush()
            items = []
            for item in value:
                items.append({'concept': item.concept, 'definition': item.definition})

            content = renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'glossary.mustache'), {'items': items})
            session_title = renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'title.mustache'), {'value': key})
            thumbnail_title = key + '.jpg'
            session_description = renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'description.mustache'), {'thumbnail': thumbnail_title})
            sessions.append(Session(session_title, content, session_description))

        print '\r  > Creating glossary sessions (100%). Done.'

        section_title = renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'title.mustache'), {'value': 'Glossary'})
        return Section(section_title, sessions)


class GlossaryItem:

    def __init__(self, concept, definition):
        self.concept = concept
        self.definition = definition
