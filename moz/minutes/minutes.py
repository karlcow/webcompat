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
arthur: but that could be an issue.

## Holiday (あきら)

amir: life is too short.
But we never know. We might learn something.
akira: Let's make it big.

===========AGENDA ITEMS ABOVE THIS LINE===========

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


def parse_minutes(raw_minutes, txt_format):
    '''Parse the minutes and structure them to be ready to export.

    It will return a structured format ready to be converted.
    '''
    # Initializing
    FIRSTLINE = False
    DESCRIPTION = False
    SPEAKER = False
    converted_text = ''
    speaker_text = ''
    topicmatch = re.compile(ur'^##\s*(.*)\s*\((.*)\)\s*')
    personmatch = re.compile(ur'^([^: .]+):\s(.*)')
    # removing leading and trailing spaces
    raw_minutes = raw_minutes.strip()
    # going through the text
    for line in raw_minutes.split('\n'):
        m = re.match(topicmatch, line)
        if m:
            print "match topic 1"
            if not SPEAKER:
                converted_text += close_speaker(speaker_text, txt_format)
            topic = m.group(1).strip(), m.group(2).strip()
            converted_text += make_topic(topic, txt_format)
            description = ''
            DESCRIPTION = True
        else:
            print "DO NOT match topic 2"
            m = re.match(personmatch, line)
            if not m and DESCRIPTION:
                description += '{0} '.format(line)
                print description
            elif m:
                print "match topic 3"
                if not FIRSTLINE:
                    converted_text += close_speaker(speaker_text, txt_format)
                # match on the name + line
                FIRSTLINE = True
                SPEAKER = True
                speaker_text = ''
                speaker_name = ''
                # We add the text description for the topic
                if DESCRIPTION and (description.strip() != ''):
                    converted_text += make_description(description, txt_format)
                    DESCRIPTION = False
                else:
                    DESCRIPTION = False
                speaker_name, speaker_text = m.group(1), m.group(2)
                converted_text += make_firstline(speaker_name, txt_format)
                # We are out of the first line into the lines of SPEAKERS
                FIRSTLINE = False
            elif not m and not DESCRIPTION:
                print "DO NOT match topic 4"
                if SPEAKER:
                    converted_text += '{0} '.format(speaker_text)
                    speaker_text = ''
                    SPEAKER = False
                converted_text += '{0} '.format(line)
    # We need to add the trailing speaker text before returning.
    converted_text += close_speaker(speaker_text, txt_format)
    return converted_text


def make_topic(topic, txt_format='mw'):
    '''Convert the topic with the text format of choice.'''
    if txt_format == 'mw':
        formatted_topic = '\n\n=== {0} ({1}) ==='.format(topic[0], topic[1])
    elif txt_format == 'html':
        formatted_topic = '''
<h2>{0} (<span class="owner">{1}</span>)</h2>'''.format(topic[0],
                                                        topic[1])
    elif txt_format == 'email':
        formatted_topic = '### {0} ({1})\n'.format(topic[0], topic[1])
    return formatted_topic


def make_description(description, txt_format='mw'):
    '''Convert the description with the text format of choice.'''
    if txt_format == 'mw':
        formatted_description = "\n'''{0}'''\n".format(description)
    elif txt_format == 'html':
        formatted_description = '''
<p class="description">{0}</p>'''.format(description)
    elif txt_format == 'email':
        formatted_description = '{0}\n'.format(description)
    return formatted_description


def make_firstline(speaker_name, txt_format='mw'):
    '''Convert the firstline with the text format of choice.'''
    if txt_format == 'mw':
        formatted_firstline = "\n* '''{0}''': ".format(speaker_name)
    elif txt_format == 'html':
        formatted_firstline = '''
<p class="speaker">
    <span class="speaker_name>{0}<span>:'''.format(speaker_name)
    elif txt_format == 'email':
        formatted_firstline = ''
    return formatted_firstline


def close_speaker(speaker_text, txt_format='mw'):
    '''Convert the speakers line and close them.'''
    if txt_format == 'mw':
        return speaker_text
    elif txt_format == 'html':
        return " {0}</p>".format(speaker_text)
    elif txt_format == 'email':
        return ''


def main():
    '''core program'''
    # Fetch the content online
    # raw_content, encoding = etherpad_content(SERVER_URL, 'webcompat', 'txt')
    raw_content = TESTFILE
    # Extract the Multimarkdon part of the body
    md_content = extract_minutes(raw_content)
    final_text = parse_minutes(md_content['text'], 'email')
    # return final_text.encode('utf-8')
    return final_text

if __name__ == "__main__":
    sys.exit(main())
