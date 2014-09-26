#!/usr/bin/env python
# encoding: utf-8
"""
minutes.py

Created by Karl Dubost on 2014-09-25.
Copyright (c) 2014 La Grange. All rights reserved.
MIT License

We want:

1. Import
https://etherpad.mozilla.org/ep/pad/export/webcompat/latest?format=txt
2. Extract the effective minutes from the text
3. Extract the date
4. Convert the text to the appropriate format
"""

import re
import sys

import requests

WIKI_TEMPLATE = '''== Minutes =='''
URL = 'https://etherpad.mozilla.org/ep/pad/export/webcompat/latest?format=txt'
SERVER_URL = 'https://etherpad.mozilla.org'
STOPLINE = '===========DO NOT REMOVE THIS LINE==========='
TESTFILE = '''

Meeting: Mobile Web Meeting Compatibility
Date: September 30, 2014 - 13:00 UTC
Minutes: https://wiki.mozilla.org/Compatibility/Mobile/2014-09-30


##　川 for example.com (arthur)
We have an issue about example.com.
arthur: fish is not fresh.
chloe: catch more.

## Holiday (あきら)

amir: life is too short.
akira: Let's make it big.

===========DO NOT REMOVE THIS LINE===========

we do not want that.

'''


def etherpad_content(server_uri, pad_name, pad_format='txt'):
    '''Fetch the text version of the etherpad.'''
    url = '{0}/ep/pad/export/{1}/latest?format={2}'.format(server_uri,
                                                           pad_name,
                                                           pad_format)
    content = requests.get(url)
    return content.text, content.encoding


def extract_minutes(raw_content):
    '''Separate the metadata and the minutes from the raw content.

    It creates a dictionary of metanames and text.
    '''
    # Initializing
    content = {}
    textlines = []
    metadata = re.compile(ur'^([^ .]+): (.*)$', re.IGNORECASE)
    METAFLAG = False
    CONTENTFLAG = False
    # going through the text
    for line in raw_content.split('\n'):
        # We stop when reaching the stopline
        if line == STOPLINE:
            break
        # Ignoring eventual blank lines at the start
        if line == '' and not METAFLAG and not CONTENTFLAG:
            pass
        # Processing meta
        elif line != '' and not CONTENTFLAG:
            METAFLAG = True
            metaname, metacontent = re.findall(metadata, line)[0]
            content[metaname] = metacontent
        # reached the blank line in between meta and content
        elif line == '' and not CONTENTFLAG:
            METAFLAG = False
            CONTENTFLAG = True
        elif CONTENTFLAG:
            textlines.append(line)
    content['text'] = '\n'.join(textlines)
    return content


def parse_minutes(raw_minutes):
    '''Parse the minutes and structure them to be ready to export.

    It will return a structured format ready to be converted.
    '''
    parsed_minutes = {}
    return parsed_minutes


def convert_minutes(content, txt_format='mw'):
    '''Convert the minutes in the appropriate format.

    Input is Multimarkdown
    * mw is MediaWiki (available and default)
    * html for HTML (reserved)
    * pdf for PDF (reserved)
    '''
    pass


def main():
    '''core program'''
    # Fetch the content online
    # raw_content, encoding = etherpad_content(SERVER_URL, 'webcompat', 'txt')
    # Extract the Multimarkdon part of the body
    md_content = extract_minutes(TESTFILE)
    print md_content

if __name__ == "__main__":
    sys.exit(main())
