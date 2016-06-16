
from lxml import html
import requests

#Possible parseable contents and their labels in the page
content_types = {
    'rss'   : 'RSS',
    'scorm' : 'SCORM',
    'imscc' : 'IMS Common Cartridge'
}

class URLUtils(object):

    @staticmethod
    def get_file_url(url, format='xml'):

        if format is 'xml':
            return URLUtils.url_for_xml(url)
        elif format in content_types:
            return URLUtils.url_for_scrappable_format(url, format)
        else:
            return None


    @staticmethod
    def url_for_xml(url):
        return  url.strip() + ('&' if '?' in url else '?') + 'content=scxml'

    @staticmethod
    def url_for_scrappable_format(url, format):
        page = requests.get(url)
        content = html.fromstring(page.content)

        files = content.cssselect('div.oucontent-files li')

        for list_item in files:
            content_type = list_item.cssselect('.oucontent-typeandsize')
            if not content_type: #the list item has no content description
                continue

            contenttype_description = content_type[0].text
            if content_types[format] in contenttype_description:
                file_link = list_item.cssselect('a')
                if file_link:
                    return file_link[0].get('href')

        return None