import urllib2
from urllib2 import HTTPError, URLError

from lxml import html

# Possible parseable contents and their labels in the page
content_types = {
    'rss': 'RSS',
    'scorm': 'SCORM',
    'imscc': 'IMS Common Cartridge'
}


class URLUtils(object):

    @staticmethod
    def get_format_url(url, ouformat='xml'):

        if ouformat is 'xml':
            return URLUtils.url_for_xml(url)
        elif ouformat in content_types:
            return URLUtils.url_for_scrappable_format(url, ouformat)
        else:
            return None


    @staticmethod
    def url_for_xml(url):
        return  url.strip() + ('&' if '?' in url else '?') + 'content=scxml'

    @staticmethod
    def url_for_scrappable_format(url, ouformat):
        err, page = URLUtils.get(url)
        if err:
            return None

        content = html.fromstring(page)
        files = content.cssselect('div.oucontent-files li')

        for list_item in files:
            content_type = list_item.cssselect('.oucontent-typeandsize')
            if not content_type:  # the list item has no content description
                continue

            contenttype_description = content_type[0].text
            if content_types[ouformat] in contenttype_description:
                file_link = list_item.cssselect('a')
                if file_link:
                    return file_link[0].get('href')

        return None

    @staticmethod
    def get(url):

        response = None
        result = None
        try:
            response = urllib2.urlopen(url)
            content = response.read()
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            result = e, None
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            result = e, None
        else:
            result = None, content
        finally:
            if response is not None:
                response.close()
            return result