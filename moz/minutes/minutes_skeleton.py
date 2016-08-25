#!/usr/bin/env python
# encoding: utf-8
"""
minutes_skeleton.py
Will generate the minutes for the week.


Created by Karl Dubost on 2014-09-02.
Copyright (c) 2014 La Grange. All rights reserved.
MIT License
"""

from datetime import date, timedelta
import sys

import requests

import bugsweeksummary
import extractfeedtitle
import minutes

MEETINGS_URI = 'https://wiki.mozilla.org/Compatibility/Meetings?action=raw'
MINUTES_TEMPLATE = '''
* [[Compatibility|Web Compatibility]] Meeting - {meeting_date}
* [[Compatibility/Meetings|Minutes]]: [[Compatibility/Meetings/{previous_week}|Previous {previous_week}]]

== Minutes ==
{minutes}

== Broken Voices of the Web ==
{broken_voices}
{bugs_summary}
'''  # nopep8


def wiki_page(uri):
    '''Fetch the raw text version of the wiki markup.'''
    content = requests.get(uri)
    return content.text, content.encoding


def previous_meeting(wiki_content):
    '''Extract the latest meeting date.'''
    iso_date = None
    for line in wiki_content.split('\n'):
        if line.startswith('* Tuesday'):
            iso_date = line.partition('Meetings/')[2].partition('|Minutes')[0]
            return iso_date
    # in case we didn't find any date
    return iso_date


def meeting_date(mdate=None):
    '''return the meeting date if not given'''
    if not mdate:
        return date.today()


def meeting_minutes():
    '''Create the meeting minutes'''
    minutes_txt = minutes.main()
    return minutes_txt


def wiki_markup(previous_date):
    '''return the final wiki markup'''
    mtoday = meeting_date()
    today_iso = mtoday.isoformat()
    print('Preparing Meeting Minutes')
    meet_minutes = meeting_minutes()
    print('Preparing blogs summary')
    blogs = extractfeedtitle.broken_voices()
    print('Preparing bugs summary')
    bugs = bugsweeksummary.summary()
    return MINUTES_TEMPLATE.format(
        meeting_date=today_iso,
        previous_week=previous_date,
        minutes=meet_minutes,
        broken_voices=blogs,
        bugs_summary=bugs)


def main():
    '''core program'''
    wiki_content, wiki_encoding = wiki_page(MEETINGS_URI)
    previous_date = previous_meeting(wiki_content)
    print(wiki_markup(previous_date))


if __name__ == "__main__":
    sys.exit(main())
