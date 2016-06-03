import urllib2
from xml.etree import ElementTree


class CheckUsedTags:

    used_tags = {}

    def __init__(self, path):
        file = open(path, "r")
        for line in file:
            if "glossary" not in line:
                extra = "&content=scxml"
                if extra not in line:
                    line = line.rstrip() + extra
                self.getusedtags(urllib2.urlopen(line).read())
        file.close()
        print "Total tags:" + str(len(self.used_tags))
        print self.used_tags

    def getusedtags(self, content):
        """Returns the used tags in OU courses"""
        element = ElementTree.fromstring(content)
        for e in element.iter():
            if e.tag in self.used_tags:
                self.used_tags[e.tag] += 1
            else:
                self.used_tags[e.tag] = 1



