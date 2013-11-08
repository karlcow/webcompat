#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
→ ./link-rel-icon.py --uri http://wikipedia.org/
[('apple-touch-icon', '', '//en.wikipedia.org/apple-touch-icon.png'), ('shortcut icon', '', '//en.wikipedia.org/favicon.ico')]
"""

import argparse
from lxml.html import html5parser
import requests

# Probably to get on the CLI in the future
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Mobile; rv:25.0) Gecko/25.0 Firefox/25.0',
    'Accept-Encoding': 'gzip, deflate'}

XHTML_NAMESPACE = 'http://www.w3.org/1999/xhtml'
icons = []


def normalize_uri(uri):
    """Making a URI more canonical"""
    if not uri.startswith('http://'):
        uri = "http://%s" % (uri)
    return uri


def cli():
    """Parsing arguments"""
    parser = argparse.ArgumentParser(description="link rel icon")
    parser.add_argument('-u', '--uri', help='Website URI', required=True)
    args = vars(parser.parse_args())
    return args['uri']


def grab_iconlink(html):
    """Parsing an HTML document and return a list of rel icon links"""
    htmlparsed = html5parser.fromstring(html)
    html_links = htmlparsed.xpath('//h:link[@rel]',
        namespaces={'h': 'http://www.w3.org/1999/xhtml'})
    for html_link in html_links:
        attributes = html_link.attrib
        relvalues = attributes['rel'].lower()
        if 'icon' in relvalues:
            if 'href' in attributes:
                iconlink = attributes['href']
            else:
                iconlink = ''
            if 'sizes' in attributes:
                sizevalues = attributes['sizes']
            else:
                sizevalues = ''
            icons.append((relvalues, sizevalues, iconlink))
    return icons


def main():
    uri = cli()
    normalized_uri = normalize_uri(uri)
    r = requests.get(normalized_uri, headers=headers)
    htmlcontent = r.text
    icons = grab_iconlink(htmlcontent)
    print icons

if __name__ == '__main__':
    main()
