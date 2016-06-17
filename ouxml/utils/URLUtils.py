import urllib

import requests
from lxml import html
from urlparse import urlparse, parse_qsl, ParseResult

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
        return URLUtils.replace_qs_param(url.strip(), {'content':'scxml'})

    @staticmethod
    def replace_qs_param(url, params):
        """ Add GET params to provided URL being aware of existing.
        from: http://stackoverflow.com/a/25580545

        :param url: string of target URL
        :param params: dict containing requested params to be added
        :return: string with updated URL
        """

        url = urllib.unquote(url)
        parsed_url = urlparse(url)
        get_args = parsed_url.query

        # Converting URL arguments to dict and update
        parsed_get_args = dict(parse_qsl(get_args))
        parsed_get_args.update(params)

        # Converting URL argument to proper query string
        encoded_get_args = urllib.urlencode(parsed_get_args, doseq=True)
        new_url = ParseResult(
            parsed_url.scheme, parsed_url.netloc, parsed_url.path,
            parsed_url.params, encoded_get_args, parsed_url.fragment
        ).geturl()

        return new_url


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
            response = requests.get(url)
            response.raise_for_status()
            content = response.content
        except requests.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.response.status_code)
            result = e, None
        except requests.exceptions.RequestException as e:
            print('We failed to reach a server.')
            print('Reason: ', e)
            result = e, None
        else:
            result = None, content
        finally:
            if response is not None:
                response.close()
            return result