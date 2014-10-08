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
STOPLINE = '===========AGENDA ITEMS ABOVE THIS LINE==========='
TESTFILE = '''

Meeting: Mobile Web Meeting Compatibility
Date: September 30, 2014 - 13:00 UTC
Minutes: https://wiki.mozilla.org/Compatibility/Mobile/2014-09-30


##　川 for example.com (arthur)
We have an issue about example.com.
It would be cool to be able to solve it quickly: See: blah
http://www.example.com/
arthur: fish is not fresh.
What about whales?
Do We need more?
chloe: catch more fish not whales.

## Holiday (あきら)

amir: life is too short.
But we never know. We might learn something.
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
    CONTENTFLAG = False
    # removing the blank lines at the start and the bottom
    raw_content = raw_content.strip()
    # going through the text
    for line in raw_content.split('\n'):
        # We stop when reaching the stopline
        if line == STOPLINE:
            break
        # Processing meta
        if line != '' and not CONTENTFLAG:
            metaname, metacontent = re.findall(metadata, line)[0]
            content[metaname] = metacontent
        # reached the blank line in between meta and content
        elif line == '' and not CONTENTFLAG:
            CONTENTFLAG = True
        elif CONTENTFLAG:
            textlines.append(line)
    # Aggregate the text and remove leading and trailing spaces
    content['text'] = '\n'.join(textlines).strip()
    return content


def parse_minutes(raw_minutes):
    '''Parse the minutes and structure them to be ready to export.

    It will return a structured format ready to be converted.
    '''
    # Initializing
    FIRSTLINE = False
    DESCRIPTION = False
    parsed_minutes = {}
    topicmatch = re.compile(ur'^##\s*(.*)\s*\((.*)\)\s*')
    personmatch = re.compile(ur'^([^: .]+):\s(.*)')
    # removing leading and trailing spaces
    raw_minutes = raw_minutes.strip()
    # going through the text
    for line in raw_minutes.split('\n'):
        m = re.match(topicmatch, line)
        if m:
            print('-'*80)
            topic, owner = m.group(1).strip(), m.group(2).strip()
            print '> topic: %s\n> owner: %s' % (topic, owner)
            description = ''
            FIRSTLINE = True
            DESCRIPTION = True
        else:
            m = re.match(personmatch, line)
            if not m and DESCRIPTION:
                description += line
                print '[ ', line
            elif m and FIRSTLINE:
                speaker_text = ''
                speaker_name, speaker_text = m.group(1), m.group(2)
                print 'speaker(%s): %s' % (speaker_name, speaker_text)
                FIRSTLINE = False
                DESCRIPTION = False
            else:
                speaker_text += line
                print '... %s' % (line)
                FIRSTLINE = True
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
    parse_minutes(md_content['text'])

if __name__ == "__main__":
    sys.exit(main())
