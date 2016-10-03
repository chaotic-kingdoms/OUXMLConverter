import urllib2
from xml.etree import ElementTree
from pprint import pprint


class CheckUsedTags:

    used_tags = []

    def __init__(self, path):
        f = open(path, "r")
        for line in f:
            if "glossary" not in line:
                extra = "&content=scxml"
                if extra not in line:
                    line = line.rstrip() + extra
                self.getusedtags(urllib2.urlopen(line).read())
        f.close()
        print "Total tags:" + str(len(self.used_tags))
        pprint(self.used_tags)

    def getusedtags(self, content, tags=None, show_location=False):
        """Returns the used tags in OU courses"""
        element = ElementTree.fromstring(content)
        section = None
        session = None
        for e in element.iter():
            if(show_location):
                if e.tag == "ItemTitle":
                    section = e.text

                if(e.tag == "Title"):
                    session = e.text

            if tags is None or e.tag in tags:
                value = next((d for i, d in enumerate(self.used_tags) if e.tag == d["TagName"]), None)

                if value:
                    value["TotalCount"] += 1
                    if show_location:
                        value["Sections"].append({"Section" : section, "Session" : session})

                else:
                    if show_location:
                        self.used_tags.append({"TagName": e.tag, "TotalCount": 1, "Sections": [{"Section" :section, "Session": session}]})
                    else:
                        self.used_tags.append( {"TagName": e.tag, "TotalCount": 1})

